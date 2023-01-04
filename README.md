# recog_prototype

Video streaming FastAPI app using WebRTC (using [aiortc](https://github.com/aiortc/aiortc)) and openCV for realtime video processing.

Implemented the code in https://github.com/aiortc/aiortc/tree/main/examples/server into a FastAPI app and added face detection option.

STUN servers are not needed in local networks.

## Requirements

Python 3.9+

Webcam

## Dev server startup

Using a python virtual environment like virtualenv or pipenv is recommended to avoid package conflicts

- pip install virtualenv

- git clone https://github.com/RumbleFiend/recog_prototype.git

- cd prototype_dsaru

- virtualenv venv

- venv/Scripts/Activate.ps1
 
- pip install -r requirements.txt

- uvicorn server:app --reload

