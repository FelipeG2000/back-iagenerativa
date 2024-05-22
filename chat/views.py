import json
import os
import requests
import fitz
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import QuestionSerializer
from decouple import config

api_key=config('OPENAI_API_KEY')


URL = "https://api.openai.com/v1/chat/completions"


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text


def extract_text_from_docx(file_path):
    from docx import Document
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_text(file):
    file_extension = os.path.splitext(file)[1]
    if file_extension == '.pdf':
        return extract_text_from_pdf(file)

    elif file_extension == '.docx':
        return extract_text_from_docx(file)
    else:
        return "File type not supported"


class Answer(generics.CreateAPIView):

    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        texto1 = extract_text('/home/felipe/Documentos/TalentoB/generativeAI/chat/root/El_lobo_solitario.docx')
        texto2 = extract_text('/home/felipe/Documentos/TalentoB/generativeAI/chat/root/La_inteligencia_artificial.pdf')
        texto3 = extract_text('/home/felipe/Documentos/TalentoB/generativeAI/chat/root/La_liebre_y_la_tortuga.pdf')
        question = request.data['question']
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an assistan that helps with information extraction."},
                {"role": "user", "content": f"Context:{texto1}\n\n{texto2 if texto2 else '-'}\n\n{texto3} \n\nQuestion: {question}?"}],
            "temperature": 1.0,
            "top_p": 1.0,
            "n": 1,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 0,

        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.post(URL, headers=headers, json=payload, stream=False)
        print(response.content.decode('utf-8'))
        response_json = json.loads(response.content.decode('utf-8'))
        answer = response_json["choices"][0]["message"]["content"]


        serializer = QuestionSerializer(data={'question': question, 'respuesta': answer})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
