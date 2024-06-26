# curl -X POST "http://portal.tensorguru.com:8000/translate/" -H "Content-Type: application/json" -d '{"text": "Hello World", "apikey" : "LST1234", "dest" : "th"}'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from os import environ
from main_correct import LSTSpellChecker

checker = LSTSpellChecker()

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) configuration
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class SpellCheckRequest(BaseModel):
    text: str
    apikey: str

class SpellCheckResponse(BaseModel):
    incorrect: list

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/api/spellcheck", response_model=SpellCheckResponse)
async def translate_text(request: SpellCheckRequest):
    # Here you would have your translation logic (dummy example)
    if request.apikey != "LST-SPGDKBIELDKFKeoDE":
        return {"incorrect": ["API Key Error !"]}

    incorrect = checker.process(request.text)

    return {"incorrect" : incorrect}
