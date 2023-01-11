import asyncio
import io
import json
import logging
import os
import ssl
import time
import uuid
import argparse
import asyncio
import json
import logging
import os
import base64
from io import BytesIO
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import uuid
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay

from fastapi import FastAPI, Request, Response, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from aiohttp import web 
from utils.videoProcessor import VideoTransformTrack
from utils.photoProcessor import processPhoto

from utils.videoob import run_video, run_tracking

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()
relay = MediaRelay()

#function pour réexuction du server
def keep_alive():
    while True:
        time.sleep(60)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

async def javascript(request):
    content = open(os.path.join(ROOT, "/static/js/client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)
    

@app.post("/photo")
async def photo(request: Request):
    form = await request.form()
    print('je suis forme',form)
    transform = list(form.keys())
    transformation = form [transform[0]]
    transforms = transform[1]
    contents = await form[transforms].read()
    image: bytes = processPhoto(contents, transformation)
    base64_str = base64.b64encode(image).decode()
    #print(base64_str)
    #base64_str = base64.b64encode(StreamingResponse(io.BytesIO(image), media_type="image/png")).decode()
    #return StreamingResponse(io.BytesIO(image), media_type="image/png")
    return f"data:image/png;base64,{base64_str}"

@app.post("/video/")
async def video(model_weights: str = "s", file: UploadFile = None):
    results_path = run_video(model_weights, file)
    return {"results_path": results_path}

@app.post("/track/")
async def video(file: UploadFile = None):
    results_path = run_tracking(file)
    return {"results_path": results_path}

@app.post("/offer")
async def offer(request: Request):
    params = await request.json()
    print(json.dumps(params, indent=4, sort_keys=True))
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.client)

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        log_info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(
                    relay.subscribe(track), transform=params["video_transform"]
                )
            )
        
        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)

    # handle offer
    await pc.setRemoteDescription(offer)

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return Response(
        content=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
        media_type="application/json",
    )

if __name__ == "__main__":
    #uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
   
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for HTTP server (default: 8000)"
    )
    parser.add_argument("--record-to", help="Write received media to a file."),
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/static/js/client.js", javascript)
    app.router.add_post("/offer", offer)
    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )



