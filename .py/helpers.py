import os
import sys
import time

clear: str = 'cls'

def get_root_dir() -> str:
  if getattr(sys, "frozen", False):
    return os.path.dirname(sys.executable)
  else:
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  

def remove_spacing(valid_file_instance: str):
  file_content:    list[str]
  filename_no_ext: str       = valid_file_instance[:-4]

  with open(os.path.join(get_root_dir(), "_internal", "res", "spacings.txt"), "r", encoding="utf-8") as file:
    file_content = file.readlines()

  with open(os.path.join(get_root_dir(), "_internal", "res", "spacings.txt"), "w", encoding="utf-8") as file:
    for line in file_content:
      if filename_no_ext not in line.split("="):
        file.write(line)


def delete_font_file() -> None:
  clear_terminal()
  happened_before: bool = False

  try:
    while 1:
      if happened_before:
        clear_terminal()
        print("Invalid file choice! Please try again (use numbers not filenames).")
        
      valid_file_instances: list[str] = os.listdir(os.path.join(get_root_dir(), "_internal", ".txt"))

      if not valid_file_instances:
        raise FileNotFoundError
        
      input_str: str = "\nEnter target ASCII file (number):\n"
      for idx, valid_file_instance in enumerate(valid_file_instances):
        input_str += f" ({idx + 1}) |- {valid_file_instance}\n"
      
      filenum: int = int(input(input_str))
      if filenum > 0 and filenum <= len(valid_file_instances):
        os.remove(os.path.join(get_root_dir(), "_internal", ".txt", valid_file_instances[filenum - 1]))
        remove_spacing(valid_file_instance=valid_file_instances[filenum - 1])
        
        clear_terminal()
        print(f"\"{valid_file_instance}\" removed from system.")
        time.sleep(2)
        
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


if __name__ == "__main__":
  delete_font_file()