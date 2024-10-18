import app.func as nexcli
import argparse
import subprocess

parser = argparse.ArgumentParser(description='NexCLI Command Line Tool')

parser.add_argument('-c', '--command', type=str, help='Enter your command')
args = parser.parse_args()

if args.command:
    response = nexcli.nexcli_response(args.command)
    response_list = response.split(',')
    for command in response_list:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        except Exception as e:
            nexcli.print_red("Some error occured with the command `{command}`:\n{e}")
    print(response_list)
    print(f'NexCLI: {nexcli.nexcli_response(args.command)}')
else:
    print("No command")



