from dotenv import load_dotenv

load_dotenv()

from controller.controller import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("controller.controller:app", host="0.0.0.0", port=8000, reload=True)
