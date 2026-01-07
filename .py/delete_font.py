import os
from helpers import get_root_dir

def delete_font_file() -> None:
    while 1:
        valid_file_instances: list[str] = os.listdir(os.path.join(get_root_dir(), "_internal", ".txt"))

        if not valid_file_instances:
            raise FileNotFoundError
        
        input_str: str = "\nEnter target ASCII filename:\n"
        for valid_file_instance in valid_file_instances:
            input_str += " |- " + valid_file_instance + "\n"
        
        filename: str = input(input_str)
        for valid_file_instance in valid_file_instances:
            if valid_file_instance in {filename, filename + ".txt"}:
                os.remove(valid_file_instance)
                break

        