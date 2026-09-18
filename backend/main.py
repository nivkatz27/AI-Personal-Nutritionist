from fastapi import FastAPI

app = FastAPI(title="AI Personal Nutritionist API")


@app.get("/")
def read_root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
