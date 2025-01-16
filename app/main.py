from config import Log_Requests
from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Bonphyre API",
    description="A backend server for a simple crowdfunding platform where users can create, view, and contribute to projects.",
    version="0.1.0",
)
app.include_router(router, prefix="/api/v1")
app.add_middleware(Log_Requests)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
