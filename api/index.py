from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(debug=False)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and setup database models
try:
    from app.database import engine
    from app import models
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database setup error: {e}")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the landing page at the root URL
@app.get("/", response_class=FileResponse)
def read_index():
    return FileResponse(os.path.join("static", "nexrift-theme.html"))

# Include API routers
try:
    from app.routers import users
    app.include_router(users.router)
    from app.routers import contact
    app.include_router(contact.router)
    from app.routers import excel
    app.include_router(excel.router)
except Exception as e:
    print(f"Router import error: {e}")

# Vercel handler
from mangum import Adapter
handler = Adapter(app) 