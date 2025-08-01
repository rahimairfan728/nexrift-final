from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(debug=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

# Serve static files (images, CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the landing page at the root URL
@app.get("/", response_class=FileResponse)
def read_index():
    return FileResponse(os.path.join("static", "nexrift-theme.html"))

# (Keep your API routers as before)
from app.routers import users
app.include_router(users.router)
from app.routers import contact
app.include_router(contact.router)
from app.routers import excel
app.include_router(excel.router)

EXCEL_FILE = os.path.join(os.path.dirname(__file__), '../../data.xlsx')
