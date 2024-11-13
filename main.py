import os
import openai
import pymupdf

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(file_path):
    with pymupdf.open(file_path) as pdf_file:
        text = ""
        for page_num in range(pdf_file.page_count):
            page = pdf_file[page_num]
            text += page.get_text()
    return text

def main():
  client = OpenAI()

  pdf_text = extract_text_from_pdf("pdf-files/Peluqueria_Pierina.pdf")

  sales_role = """Como experto en ventas con aproximadamente 15 años de experiencia en embudos de ventas y generación de leads, tu tarea es mantener una conversación agradable, responder a las preguntas del cliente sobre nuestros productos. Tus respuestas deben basarse únicamente en el contexto proporcionado:
Para proporcionar respuestas más útiles, puedes utilizar la información proporcionada en la base de datos. El contexto es la única información que tienes. Ignora cualquier cosa que no esté relacionada con el contexto.
### INTRUCCIONES
- Mantén un tono profesional y siempre responde en primera persona.
- NO ofrescas promociones que no existe en la BASE DE DATOS
- Respuestas cortas
- No invites a las personas a agendar una cita.
"""

  messages_buffer = [{"role": "system", "content": sales_role}]

  messages_buffer.append({"role": "user", "content": pdf_text})

  while True:
    user_input = input("User: ")

    if user_input == "q":
      break

    messages_buffer.append({"role": "user", "content": user_input});

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_buffer,
        max_tokens=80,
        temperature=0.9
    )

    print("Assistant: ", response.choices[0].message.content)

main()