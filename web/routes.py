import os

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from timelapse.controller import TimelapseController

templates = Jinja2Templates(directory="web/templates")


def create_routes(controller: TimelapseController) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @router.post("/start_timelapse")
    async def start_timelapse():
        controller.start()
        return {"status": "started"}

    @router.post("/stop_timelapse")
    async def stop_timelapse():
        controller.stop()
        return {"status": "stopped"}

    @router.get("/latest_photo")
    async def latest_photo():
        path = controller.get_latest_photo_path()
        if path and os.path.exists(path):
            return FileResponse(path)
        return JSONResponse({"error": "No photo yet"}, status_code=404)

    @router.get("/timelapse_video")
    async def get_timelapse_video():
        path = controller.get_video_path()
        if path and os.path.exists(path):
            return FileResponse(path, media_type="video/mp4", filename="timelapse.mp4")
        return JSONResponse({"error": "Video not found"}, status_code=404)

    return router
