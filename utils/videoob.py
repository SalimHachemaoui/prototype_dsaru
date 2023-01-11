import os
import subprocess
from glob import glob
from datetime import datetime
import shutil


"""
def detected():
    video_path = glob("utils/yolov5/tmp/*")[0]
    weights = "yolov5s.pt"

    subprocess.run(["env/Scripts/python", "model/yolov5/detect.py", "--source", video_path, "--weights", weights])

    name = video_path.split(os.sep)[-1]

    results_name = f"model/yolov5/tmp/results.mp4"
    os.replace(f"model/yolov5/runs/detect/exp/{name}", results_name)

    os.rmdir("model/yolov5/runs/detect/exp")


    return results_name


"""


def create_dir(name):
    try:
        os.mkdir(name)
    except Exception as e:
        pass


def run_video(model_weights, file):
    # generate name from datetime
    dirname = os.path.join("storage_runs", "video_" +
                           datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    # create dir
    create_dir(dirname)
    # save file
    video_path = os.path.join(dirname, file.filename)
    print("video_path", video_path)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # run model
    weights = f"yolov5{model_weights}.pt"
    subprocess.run(["env/Scripts/python", "utils/yolov5/detect.py",
                   "--source", video_path, "--weights", weights])
#    os.replace(f"utils/yolov5/runs/detect/exp/{file.filename}", f"{dirname}/results.mp4")
    shutil.move(
        f"utils/yolov5/runs/detect/exp/{file.filename}", f"{dirname}/results.mp4")

    shutil.rmtree("utils/yolov5/runs/")

    return os.path.join(dirname, "results.mp4")


def run_tracking(file):
    # generate name from datetime
    dirname = os.path.join("storage_runs", "tracking_" +
                           datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    # create dir
    create_dir(dirname)
    # save file
    video_path = os.path.join(dirname, file.filename)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # run model
    # subprocess.run(["env/Scripts/python", "utils/Yolov5_StrongSORT_OSNet/track.py", "--source", video_path,
    #                "--yolo-weights", "utils/Yolov5_StrongSORT_OSNet/yolov5/crowdhuman_yolov5m.pt", "--save-vid"])
    
    subprocess.run(["env/Scripts/python", "utils/Yolov5_StrongSORT_OSNet/track.py", "--source", video_path, "--save-vid"])
    

    shutil.move(
        f"utils/Yolov5_StrongSORT_OSNet/runs/track/exp/{file.filename}", f"{dirname}/results.mp4")
    shutil.rmtree("utils/Yolov5_StrongSORT_OSNet/runs/")

    return os.path.join(dirname, "results.mp4")
