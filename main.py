from fastapi import FastAPI
import uvicorn
from datetime import datetime
import subprocess
import os
import shutil
from pathlib import Path
import time

app = FastAPI(
    title="simple timelapse server",
    description="simple timelapse server",
    version="0.0.1",
)

# Global state variable
is_running = False
save_path = "/data/data/com.termux/files/home/timelapse"
frame = 0
FPS = 24
photo_dir = Path.home() / "storage" / "shared" / "DCIM" / "timelapse"


@app.post("/start")
def start():
    global is_running
    if is_running:
        print("error is already running")
        return {}
    global frame
    frame = 0
    is_running = True
    print("starting")
    global save_path
    global time_of_start
    now = datetime.now()
    save_path = save_path + "/" + now.strftime("%Y_%m_%d-%H_%M_%S")
    print(f"the savepath is {save_path}")
    print(f"mkdir {save_path}")
    subprocess.Popen(["mkdir", f"{save_path}"])
    return {}


@app.post("/photo")
def photo():
    global is_running
    global frame
    if not is_running:
        print("timelpase is not running")
    if is_running:
        frame += 1
        print(f"photo number {frame}")
        subprocess.Popen(
            [
                "am",
                "broadcast",
                "-a",
                "net.dinglisch.android.tasker.ACTION_TASK",
                "--es",
                "task_name",
                "Take_photo",
            ]
        )
        time.sleep(10)
        jpgs = list(photo_dir.glob("*.jpg"))
        latest = max(jpgs, key=os.path.getmtime)
        shutil.copy2(latest, f"{save_path}/{frame:04d}.jpg")
        # subprocess.Popen(["termux-torch", "on"])
        # print(f"termux-camera-photo -c 0 {save_path}/{frame:04d}.jpg")
        # subprocess.Popen(
        #     ["termux-camera-photo", "-c", "0", f"{save_path}/{frame:04d}.jpg"]
        # )
        # print("termux-torch off")
        # subprocess.Popen(["termux-torch", "off"])
    return {}


@app.post("/end")
def end():
    global is_running
    if not is_running:
        print("Erorr was not running")
        return {}
    global frame
    if frame == 0:
        print("no photo")
        return {}
    is_running = False
    print("ending")
    global save_path
    # creazione timelpase
    print(
        f"ffmpeg -framerate 24 -i {save_path}/%04d.jpg -c:v libx264 -pix_fmt yuv420p output.mp4 && rm {save_path}/*.jpg"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-framerate",
            f"{FPS}",
            "-i",
            f"{save_path}/%04d.jpg",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            f"{save_path}.mp4",
        ]
    )
    # shutil.rmtree(save_path)
    save_path = "~/timelapse"
    return {}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8086, reload=True)


if __name__ == "__main__":
    main()
