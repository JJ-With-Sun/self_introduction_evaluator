import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# # JSON 파일에서 API 키를 불러오는 함수
# def load_api_keys(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# API_KEYS_FILE_PATH = "./credentials/api_keys.txt"
# api_keys = load_api_keys(API_KEYS_FILE_PATH)

dotenv_path = '/home/kic/yskids/service/app/credentials/.env'
load_dotenv(dotenv_path)

# # OpenAI와 Gemini API 키 설정
# gemini_api_key = api_keys["gemini"]

genai.configure(api_key=os.getenv('GEMINI'))

# generation_config, safety_settings 설정
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 512
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  }
]

criteria = './instructions/grading_criteria.txt'

grading = './instructions/grading.txt'




class GeminiAPI:
    def __init__(self, 
                 generation_config = generation_config, model:str = "gemini-pro") -> None:
        self.model = genai.GenerativeModel(model_name=model,
                            generation_config=generation_config,
                            safety_settings=safety_settings)
      
    def gradings(self, guideline:str, self_introduction_1:str, self_introduction_2:str):
      with open('./instructions/grading.txt', 'r') as f:
        data = f.read()
        data = data.format(guideline=guideline, self_introduction_1=self_introduction_1, self_introduction_2=self_introduction_2)
        output = self.model.generate_content(data)
        return output.text