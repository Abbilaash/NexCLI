import os
import sys

# Determine the parent directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

import app as nexcli
import argparse
import subprocess 
from dotenv import set_key


def get_system_info():
    return {
        "cwd": os.getcwd(),
        "home": os.path.expanduser("~"),
        "env_path": os.environ.get("PATH", ""),
        "os_name": os.name,
        "username": os.getlogin(),
    }

# Normalise path acc to OS
def normalize_path(path):
    return os.path.normpath(path.strip('"').strip("'"))

# Execute command
def execute_command(command):
    # Extract the base command and path/arguments
    parts = command.split(maxsplit=1)
    base_cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # Handle directory creation
    if base_cmd in ["md", "mkdir"]:
        dir_path = normalize_path(args)
        if os.path.exists(dir_path):
            nexcli.print_yellow(f"Directory '{dir_path}' already exists. Skipping creation.")
            return True
        try:
            os.makedirs(dir_path, exist_ok=True)
            nexcli.print_green(f"[+] Created directory '{dir_path}'")
            return True
        except Exception as e:
            nexcli.print_red(f"Error creating directory '{dir_path}': {e}")
            return False

    # Handle file creation
    elif base_cmd == "type" and ">" in args:
        _, file_path = args.split(">", 1)
        file_path = normalize_path(file_path.strip())
        dir_path = os.path.dirname(file_path)
        
        # Create directory if it doesn't exist
        if dir_path and not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                nexcli.print_green(f"[+] Created parent directory '{dir_path}'")
            except Exception as e:
                nexcli.print_red(f"Error creating directory '{dir_path}': {e}")
                return False

        # Create or check file
        if os.path.exists(file_path):
            nexcli.print_yellow(f"File '{file_path}' already exists. Skipping creation.")
            return True
        try:
            with open(file_path, 'w') as f:
                pass
            nexcli.print_green(f"[+] Created file '{file_path}'")
            return True
        except Exception as e:
            nexcli.print_red(f"Error creating file '{file_path}': {e}")
            return False

    # For all other commands, use subprocess
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            nexcli.print_green(f"[+] Command `{command}` executed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            nexcli.print_red(f"Error executing the command `{command}`: {result.stderr}")
            return False
    except Exception as e:
        nexcli.print_red(f"Error occurred with the command `{command}`: {e}")
        return False

def explain_commands(commands):
    """Print a detailed explanation of what each command will do."""
    nexcli.print_yellow("\nThe following actions will be performed:")
    for i, command in enumerate(commands, 1):
        explanation = nexcli.get_command_explanation(command)
        nexcli.print_yellow(f"{i}. {explanation}")

def get_user_confirmation():
    """Get user confirmation before executing commands."""
    while True:
        response = input("\nDo you want to proceed with these actions? (yes/no): ").lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            nexcli.print_yellow("Please answer 'yes' or 'no'")

def execute_command_sequence(commands):
    """Execute a sequence of commands with proper feedback."""
    total_commands = len(commands)
    
    for i, command in enumerate(commands, 1):
        nexcli.print_yellow(f"\nExecuting command {i}/{total_commands}: {command}")
        if not execute_command(command):
            if i < total_commands:
                nexcli.print_red(f"Command sequence aborted at step {i}/{total_commands}")
                return False
        
    nexcli.print_green("\nAll commands executed successfully!")
    return True

def main():
    parser = argparse.ArgumentParser(description='Smart CLI Command Interpreter')
    parser.add_argument('-c', '--command', type=str, help='Enter your natural language command')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation and execute commands directly')
    parser.add_argument('-gitauth', type=str, help='Add GitHub authentication token')

    args = parser.parse_args()

    if args.command:
        # Get system information
        system_info = get_system_info()
        
        # Get command interpretation from nexcli
        response = nexcli.nexcli_response(args.command, system_info)
        commands = [cmd.strip() for cmd in response.split(',')]
        
        # Explain what each command will do
        explain_commands(commands)
        
        # Get user confirmation unless -y flag is used
        if args.yes or get_user_confirmation():
            execute_command_sequence(commands)
        else:
            nexcli.print_yellow("Operation cancelled by user")


    elif args.gitauth:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        set_key(dotenv_path, "GIT_AUTH", args.gitauth)
        print("GitHub authentication token saved successfully.")

    else:
        print("No command provided. Use -c or --command to specify a command.")

if __name__ == "__main__":
    main()