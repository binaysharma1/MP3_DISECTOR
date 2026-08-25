from fastapi import FastAPI

app= FastAPI(
    title="MusicSplit Studio API",
    description="An API for MusicSplit Studio, an AI-powered audio separation tool that allows users to isolate vocals, extract instruments, and separate audio tracks from full mixes.",
    version="1.0,0")


#function that take mp3 file and then send it to a endpoint called /mp3forward
@app.post("/upload")
async def upload_mp3(file: bytes = None):
    """
    Endpoint to receive an MP3 file and forward it to the /mp3forward endpoint.
    """
    if file is None:
        return {"error": "No file uploaded."}

    # Forward the file to the /mp3forward endpoint
    response = await mp3_forward(file)
    return response





#it accepts mp3 file and then pr
@app.get("/mp3forward")
def brain()