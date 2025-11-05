from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="simple timelapse server",
    description="simple timelapse server",
    version="0.0.1",
)

# Global state variable
is_running = False
save_path = ""


@app.post("/start")
def start():
    global is_running
    if is_running:
        print("error is already running")
        return {}
    is_running = True
    print("starting")
    # creazione cartella
    global save_path
    return {}


@app.post("/photo")
def photo():
    global is_running
    if is_running:
        print("photo")
        # fai foto e salvala
    return {}


@app.post("/end")
def end():
    global is_running
    if not is_running:
        print("Erorr was not running")
        return {}
    is_running = False
    print("ending")
    # creazione timelpase
    return {}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8085, reload=True)


if __name__ == "__main__":
    main()
