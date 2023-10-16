from fastapi import FastAPI

app = FastAPI(
    title="Book & Live"
)


@app.get("/")
async def root():
    return {"message": "Hello"}
