from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from num2words import num2words
import uvicorn
from typing import Union, Optional
import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ['API_URL']
PORT = os.environ['PORT']
os.environ["OPENAI_API_KEY"] = os.environ['OPENAI_KEY']

client = openai.OpenAI()
app = FastAPI()

class ParamsInput(BaseModel):
    number: Union[int, str]
    lang: Optional[str] = 'en'

class NumberOutput(BaseModel):
    status: str
    num_in_english: str

@app.get("/num_to_english")
async def get_num_to_english(number: Union[int, str] = Query(..., description="The number to convert"), lang: str = 'en')-> NumberOutput:
    return convert_number_to_english(number, lang)

@app.post("/num_to_english")
async def post_num_to_english(params_input: ParamsInput)-> NumberOutput:
    return convert_number_to_english(params_input.number, params_input.lang)

@app.post("/num_to_english_gpt")
async def post_num_to_english_gpt(params_input: ParamsInput)-> NumberOutput:
    return convert_number_to_english_gpt(params_input.number, params_input.lang)

def convert_number_to_english(number, language):
    try:
        num_in_english = num2words(number, lang=language).replace('-', ' ')
        return {"status": "ok", "num_in_english": num_in_english}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)} ")
    
def convert_number_to_english_gpt(number, language):
    try:
        num_txt_prompt = f'write this number in text: {number}, in this language: {language}'
        chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":f"{num_txt_prompt}==>"}],
        temperature=0.3,
        )
        reply = chat_completion.choices[0].message.content
        return  {"status": "ok", "num_in_english": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)} ")
    
if __name__ == "__main__":
    uvicorn.run(app, host=API_URL, port=int(PORT))