import google.generativeai as genai
import os
from dotenv import load_dotenv
from termcolor import colored
import json

load_dotenv()
# Load environment variables
GEMINI_API = os.getenv('GEMINI_API')
GIT_AUTH = os.getenv('GIT_AUTH')

# Initialize the Generative AI model
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def nexcli_response(query, system_info):
    system_info['git_auth_token'] = GIT_AUTH   # Add git authentication token to system info
    system_info_json = json.dumps(system_info)   # Convert directory info to JSON

    # Creating the prompt for the model
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": f"""You are a Gemini model integrated into NexCLI. Interpret the user's natural language
            input and provide only the relevant long-form Windows OS commands. Output the commands exactly as they should be
            executed, separated by commas, with no extra text, explanations, or symbols. Use full-length commands wherever
            applicable, and ensure there are no newlines at the end.

            When handling file operations:
            1. Always use correct path separators (/ or \)
            2. For creating files inside new directories, ensure the file path includes the directory
               Example: For "create folder test and file test.py in it"
               Output should be: md test, type nul > test/test.py
            3. Use relative paths unless absolute paths are specifically requested
            4. Ensure nested file operations use the correct directory structure

            Here's the current system information:
            {system_info_json}

            Consider this information when generating commands. For example:
            - Use absolute paths when necessary
            - Check if directories or files exist before creating or deleting them
            - Use environment variables when appropriate
            - Consider the current working directory for relative paths
            - If the command is related to github authentication and works, use the git_auth_token to authenticate github commands

            Provide alternative commands or checks when appropriate to handle potential errors or existing resources.
            If a task requires multiple commands, provide them all, separated by commas.
            
            
            """},
            {"role": "model", "parts": "Understood. I will provide smart, context-aware commands with correct path handling, separated by commas."},
        ]
    )
    response = chat.send_message(query)
    return response.text

def get_command_explanation(command):
    """Get a natural language explanation of what a command will do."""
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": """You are a command interpreter for NexCLI. Given a Windows command, 
            explain what it will do in clear, natural language. Focus on the actual effects of the command. 
            Be concise but specific. Don't explain syntax - explain effects. Output should be a single sentence 
            starting with 'This will'. For file operations, be explicit about the full path. Examples:
            'mkdir test' → 'This will create a new directory named "test" in the current location.'
            'type nul > test/file.txt' → 'This will create an empty file named "file.txt" inside the test directory.'
            'copy file1.txt file2.txt' → 'This will create a copy of "file1.txt" named "file2.txt".'"""},
            {"role": "model", "parts": "Understood. I will provide concise, effect-focused explanations of commands starting with 'This will'."},
        ]
    )
    response = chat.send_message(command)
    explanation = response.text.strip()
    
    # Ensure explanation starts with "This will"
    if not explanation.startswith("This will"):
        explanation = "This will " + explanation.lower()
    
    # Remove any period at the end and add one
    explanation = explanation.rstrip('.') + '.'
    
    return explanation

def print_colored(text, color):
    print(colored(text, color))

def print_red(text):
    print_colored(text, 'red')

def print_green(text):
    print_colored(text, 'green')

def print_yellow(text):
    print_colored(text, 'yellow')