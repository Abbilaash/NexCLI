# NexCLI

**NexCLI** is an intelligent, natural language command-line interpreter that allows users to run advanced OS commands with ease. Using Google’s Gemini model for prompt engineering, NexCLI translates natural-language requests into precise Windows OS commands and executes them. This tool offers flexibility, automation, and ease of use, whether you’re managing files, directories, or remote repositories.

## Features
- AI-based command generation from natural language inputs
- Context-aware command adaptation based on system information
- GitHub repository initialization and configuration using stored auth tokens
- Customizable command explanations and system information integration

## Installation
1. Clone the repository
   ```
   git clone https://github.com/Abbilaash/NexCLI.git
   cd NexCLI
   ```
2. Install Dependencies
   ```
   pip install -r requirements.txt
   ```
3. Google Gemini API key setup
   - Sign up and obtain you API key from the [Google Gemini API page](https://ai.google.dev/gemini-api)
   - Store the key in the ```.env``` file as follows:
     ```
     GEMINI_API=your_gemini_api_here
     ```

## Usage
Run NexCLI using the command
```
python <path_to_NexCLI/main.py> -c "<your_command>"
```
You can even add your GitHub authentication key
```
python <path_to_NexCLI/main.py> -gitauth "<your_git_auth_code_here>"
```

## Help Command
```-c``` or ```--command``` To execute the specified command
```-y``` or ```--yes``` Skips confirmation before command execution
```-gitauth``` Adds GitHub auth token to ```.env``` file


## Screenshots
![image](https://github.com/user-attachments/assets/b55e919c-2ea7-49ca-bf1e-2976e033fb9c)




      
