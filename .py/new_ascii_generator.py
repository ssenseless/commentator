import os
import pyperclip
import webbrowser


def mirror_browser_interaction() -> None:
  input("Press [Enter] when you have copied the information from your browser...")
  
  font_text: str = pyperclip.paste().replace("\r", "")
  
  filename: str = input("Choose a name for your ASCII font: ")
  parent_dir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

  if filename[-4:] != ".txt":
    filename = os.path.join(parent_dir, ".txt", filename + ".txt")
  else:
    filename = os.path.join(parent_dir, ".txt", filename)

  try:
    with open(filename, "w", encoding="utf-8") as file:
      file.write(font_text.splitlines()[0] + "\n" + font_text)

  except IOError as e:
    print(f"Encountered an error: {e}")
  except Exception as e:
    print(f"Encountered an error: {e}")


def open_ascii_browser() -> None:
  webbrowser.open("https://www.messletters.com/en/big-text/")


def copy_to_clipboard() -> None:
  parent_dir: str = os.path.dirname(os.path.realpath(__file__))
  filename:   str = os.path.join(parent_dir, "new_ascii_generator.txt")

  try:
    with open(filename, "r", encoding="utf-8") as file:
      clipboard: str = file.read()

  except FileNotFoundError:
      print(f"\"{filename}\" not found in \".txt/\" directory (ask Carson if you don't have it).")
  except Exception as e:
      print(f"Encountered an error: {e}")

  pyperclip.copy(clipboard)

if __name__ == "__main__":
  print("Welcome! I'm going to copy information to your clipboard and open your browser for you.\n" \
        "Once it's open, feel free to select a font from the drop down menu, paste your clipboard into the text box,\n" \
        "and select-copy ([Ctrl] + [A], [Ctrl] + [C]), all the ASCII text in the resultant box (DO NOT CLICK THE COPY BUTTON).\n")

  copy_to_clipboard()
  open_ascii_browser()
  mirror_browser_interaction()