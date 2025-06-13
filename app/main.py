from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from camera.camera import Camera
from timelapse.controller import TimelapseController
from web.routes import create_routes

PHOTO_DIR = "photos"
camera = Camera(PHOTO_DIR)
controller = TimelapseController(camera)

app = FastAPI()
app.mount("/photos", StaticFiles(directory=PHOTO_DIR), name="photos")


routes = create_routes(controller)
app.include_router(routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
