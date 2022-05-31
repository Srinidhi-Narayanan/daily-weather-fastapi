import uvicorn as uvicorn
from fastapi import FastAPI
from service import weather

app = FastAPI()
app.include_router(weather.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
