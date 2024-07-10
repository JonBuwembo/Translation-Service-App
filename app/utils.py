import openai
from sqlalchemy.orm import Session
from app.crud import update_translation_task
from dotenv import load_dotenv
load_dotenv()
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}
    for lang in languages:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5",
                messages=[
                    {"role":"system", "content":f"You are a helpful assistant that translates any language. Translate the following text to {language}: "},
                    {"role": "user", "content": text},
                ],
                max_tokens=1000
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Unexpected error: {e}"
    
    update_translation_task(db, task_id, translations)
