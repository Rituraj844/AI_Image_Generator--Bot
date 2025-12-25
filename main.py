import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

app = FastAPI()

# --- API KEY SETTING ---
# এখানে আপনার OpenAI API Key বসান।
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE" 
client = OpenAI(api_key=OPENAI_API_KEY)

# 'static' ফোল্ডার মাউন্ট করা
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found!</h1><p>Please place index.html inside the 'static' folder.</p>", status_code=404)

@app.post("/generate-image")
async def generate_image(prompt: str = Form(...), style: str = Form("photorealistic")):
    if "YOUR_OPENAI_API_KEY" in OPENAI_API_KEY:
        return {"error": "API Key বসানো হয়নি। কোডের ১০ নম্বর লাইনে কি (Key) বসান।"}

    try:
        full_prompt = f"{prompt}, {style} style, high quality, 4k resolution."
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            n=1
        )
        return {"image_url": response.data[0].url}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)