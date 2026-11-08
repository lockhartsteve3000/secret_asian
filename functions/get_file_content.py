import os

import config

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the contents of a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abs_working_dir, file_path))
        is_valid = os.path.commonpath([abs_working_dir, target]) == abs_working_dir
        if not is_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(target, "r") as f:
            file_content_str = f.read(config.MAX_CHARS)
            if f.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
            return file_content_str
    except Exception as e:
        return f'Error: reading file "{file_path}": {e}'
