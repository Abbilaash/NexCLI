import google.generativeai as genai
import os
from dotenv import load_dotenv
from termcolor import colored


load_dotenv()
GEMINI_API = os.getenv('GEMINI_API')
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel(model_name='gemini-1.5-pro', tools='code_execution')
chat = model.start_chat()


def nexcli_response(query):
    response = chat.send_message((
    query, '''give the windows command alone for the given query without any extra texts like I can help you with... and extra quotes. 
    Just give the commands seperated by commas and remove the newline from the last'''))

    return response.text

def print_red(text):
    print(colored(text,'red'))