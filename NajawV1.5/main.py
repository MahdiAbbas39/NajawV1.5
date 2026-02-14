from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

# السماح بقراءة الملفات (html, css, images)
app.mount("/static", StaticFiles(directory="."), name="static")

# مدير الاتصالات
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str, sender: WebSocket):
        for connection in self.active_connections:
            if connection != sender:
                await connection.send_text(message)

manager = ConnectionManager()

# الصفحة الرئيسية
@app.get("/")
async def get():
    return FileResponse("index.html")

# ملف التصميم
@app.get("/style.css")
async def get_css():
    return FileResponse("style.css")

# ملف الجافاسكربت
@app.get("/script.js")
async def get_js():
    return FileResponse("script.js")

# ملف الصورة (تأكد أن اسم الصورة عندك icon.png)
@app.get("/icon.png")
async def get_icon():
    return FileResponse("icon.png")

# قناة التواصل الحية
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)