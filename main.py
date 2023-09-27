from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import Settings

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = FastAPI()
setting = Settings()

api_key = setting.API_KEY
search_engine_id = setting.SEARCH_ENGINE_ID

origins = ["http://localhost:3000", "https://music-ai.vercel.app"]
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
    fallback = "Sorry, I cannot think of a reply for that."
    result = []

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        response = service.cse().list(cx=search_engine_id, q=request.query).execute()

        for item in response["items"]:
            result.append(
                {
                    "title": item["title"],
                    "link": item["link"],
                    "snippet": item["snippet"],
                }
            )

    except HttpError as e:
        result = fallback
        print("An error occurred:", e.content)

    return {"result": result}
