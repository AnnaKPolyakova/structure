import uvicorn

from src.app.main import create_app

app = create_app(False)

if __name__ == "__main__":
    uvicorn.run(
        "src.app.__main__:app", host="127.0.0.1", port=8000, reload=True
    )
