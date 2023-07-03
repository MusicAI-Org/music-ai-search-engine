from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import Settings
import requests

app = FastAPI()
setting = Settings()

api_key = setting.API_KEY
search_engine_id = setting.SEARCH_ENGINE_ID
search_url = setting.SEARCH_URL

origins = ["http://localhost:3000", "https://music-ai.vercel.app/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"Health_Check": "Ok"}


@app.post("/chatbot_query")
def chatbot_query(request: QueryRequest, index: int = 0):
    # print(request.query)
    fallback = "Sorry, I cannot think of a reply for that."
    result = ""

    try:
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": request.query,
            "num": 1,
            "start": index + 1,
        }

        response = requests.get(search_url, params=params)
        data = response.json()

        if "items" in data:
            first_result = data["items"][0]
            result = first_result["snippet"]
        else:
            result = fallback

    except Exception:
        result = fallback

    return {"result": result}
