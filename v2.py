import subprocess
import os

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=False)
        return output.decode('utf-8')
    except Exception as e:
        return str(e)

def include_file(filename):
    allowed_files = ['file1.txt', 'file2.txt']
    if filename in allowed_files:
        try:
            with open(filename, 'r') as file:
                return file.read()
        except Exception as e:
            return str(e)
    else:
        return "File not found"

def main():
    user_input = input("Enter a command: ")
    print(execute_command(user_input.split()))

    filename = input("Enter a filename: ")
    print(include_file(filename))

if __name__ == "__main__":
    main()
