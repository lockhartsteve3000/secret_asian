import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file within the working directory with optional arguments. Use this tool whenever you need to execute Python scripts or run test suites like tests.py.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to execute",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional arguments to pass to the script",
                },
            },
            "required": ["file_path"]
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abs_working_dir, file_path))
        is_valid = os.path.commonpath([abs_working_dir, target]) == abs_working_dir
        if not is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        _, ext = os.path.splitext(file_path)
        if ext != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target]
        if args:
            command.extend(args)

        result = subprocess.run(command, check=False, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        
        parts = []
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            parts.append("No output produced")
        else:
            if result.stdout:
                parts.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                parts.append(f"STDERR: {result.stderr}")
        return "\n".join(parts)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
            
            
