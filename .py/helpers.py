import os
import sys


def get_root_dir() -> str:
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  else:
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  

def delete_font_file() -> None:
  try:
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
          os.remove(os.path.join(get_root_dir(), "_internal", ".txt", valid_file_instance))
          print(f"\"{valid_file_instance}\" removed from system.")
          return
      
      print("Invalid filename, try again (with or without \".txt\")")
  except FileNotFoundError:
    print("You don't have any font files! Hard to delete files that don't exist.")
