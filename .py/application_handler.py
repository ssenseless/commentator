from new_ascii_generator import *
from comment_generator   import *
from helpers import get_root_dir, delete_font_file
  

def handle() -> None:
  while 1:
      user_input: int = int(input(
          "\nWould you like to...\n"
        + " [1]: Generate a comment?\n"
        + " [2]: Import a new ASCII font?\n"
        + " [3]: Delete a font file?\n"
        + " [4]: Quit?\n"
        + " [---[ "
      ))

      match user_input:
        case 1:
          run_comment_generator()
        case 2:
          run_ascii_import()
        case 3:
          delete_font_file()
        case 4:
          print("Thank you!")
          sys.exit(0)
        case _:
          print("Choose a valid option, please! ([1] - [3])")

  
def run_ascii_import() -> None:
  happened_before: bool = False
  print("Welcome! I'm going to copy information to your clipboard and open your browser for you.\n" \
        "Once it's open, feel free to select a font from the drop down menu, paste your clipboard into the text box,\n" \
        "and select-copy ([Ctrl] + [A], [Ctrl] + [C]), all the ASCII text in the resultant box (DO NOT CLICK THE COPY BUTTON).\n")

  while 1:
    if happened_before:
      print("\nConsider your browser opened and your clipboard copied to. :D")

    copy_to_clipboard()
    open_ascii_browser()
    mirror_browser_interaction()

    if input("Would you like to import another ASCII font? (y/n): ") != "y":
      break

    happened_before = True

  
def run_comment_generator() -> None:
  while 1:
    try:
      filename:  str = ensure_dir()
    except FileNotFoundError:
      print("You don't have any font files! You need to import at least one to start.")
      return
    
    language:  int             = check_language()
    separator: tuple[str, int] = check_separator()

    biggify_comment(filename, language, separator)

    if input("Would you like to generate comments using a different font/separator or for another language? (y/n): ") != "y":
      break


if __name__ == "__main__":
  txt_path: str = os.path.join(get_root_dir(), "_internal", ".txt")
  if not os.path.exists(txt_path):
    os.mkdir(txt_path)
  
  handle()