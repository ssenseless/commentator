import os
import sys

clear: str = 'cls'

def get_root_dir() -> str:
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  else:
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  

def delete_font_file() -> None:
  clear_terminal()
  happened_before: bool = False

  try:
    while 1:
      if happened_before:
        clear_terminal()
        print("Invalid filename, try again (with or without \".txt\")")
        
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
      
      happened_before = True

  except FileNotFoundError:
    print("You don't have any font files! Hard to delete files that don't exist.")


def sys_clear_setup():
  if sys.platform in ('linux', 'darwin'):
    clear = 'clear'
  elif sys.platform == 'win32':
    clear = 'cls'
  else:
    print('Platform not supported', file=sys.stderr)
    exit(1)
  

def clear_terminal() -> None:
    os.system(clear)
