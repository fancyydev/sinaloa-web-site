from openai import OpenAI, OpenAIError
from django.conf import settings

# Configurar la clave API
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def query_openai(prompt, model="gpt-3.5-turbo", max_tokens=100):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        return response['choices'][0]['message']['content']
    except OpenAIError as e:
        return f"Error al conectarse con OpenAI: {str(e)}"
