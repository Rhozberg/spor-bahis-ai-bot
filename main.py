from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai

app = FastAPI()

# OpenAI API anahtarını buraya ekle
openai.api_key = "OPENAI_API_KEY"

class UserInput(BaseModel):
    message: str

# Basit kök endpoint: sunucu çalışıyor mu kontrol için
@app.get("/")
async def root():
    return {"message": "Spor Bahis AI Bot çalışıyor! POST /chat ile sorularınızı iletin."}

# Prompt şablonu
prompt_template = """
Sen bir spor bahis uzmanısın. Kullanıcı sana bir maç veya bahis ile ilgili soru soracak.
Sen tarafsız ve istatistiksel yorumlarla cevap vereceksin. Garanti verme.

Kullanıcı: {user_message}
Cevap:
"""

@app.post("/chat")
async def chat(input: UserInput):
    # Kullanıcı mesajını prompt'a yerleştir
    prompt = prompt_template.format(user_message=input.message)

    # OpenAI API çağrısı
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sen profesyonel bir spor bahis analistisin."},
            {"role": "user", "content": prompt}
        ]
    )

    # Cevabı döndür
    return {"response": response["choices"][0]["message"]["content"]}
