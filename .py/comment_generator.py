import os
import sys

from helpers import get_root_dir

translation_unit: dict[int, list[str]] = {}


def ensure_dir() -> str:
  is_valid_file_instance: bool = False
  while not is_valid_file_instance:
    valid_file_instances: list[str] = os.listdir(os.path.join(get_root_dir(), ".txt"))

    if not valid_file_instances:
      raise FileNotFoundError
    
    input_str: str = "\nEnter target ASCII filename:\n"
    for valid_file_instance in valid_file_instances:
      input_str += " |- " + valid_file_instance + "\n"
    
    filename: str = input(input_str)

    root_dir: str = get_root_dir()
    file_implied_txt:  str = os.path.join(root_dir, ".txt", filename)
    file_no_txt:       str = os.path.join(root_dir, ".txt", filename + ".txt")

    is_valid_file_instance = os.path.isfile(file_implied_txt) or os.path.isfile(file_no_txt)

  return filename


def check_language() -> int:
  while 1:
    language: int = int(input(
        "\nWhich language are you using?\n"
      + " [1]: C-Style    (/*    ...    */)\n"
      + " [2]: Python     (\"\"\"   ...   \"\"\")\n"
      + " [3]: HTML/XML   (<!--  ...   -->)\n"
      + " [4]: Lua        (--[[  ...    ]])\n"
      + " [5]: Delphi     ({     ...     })\n"
      + " [6]: Old Pascal ((*    ...    *))\n"
      + " [---[ "
    ))

    if language > 0 and language < 7:
      return language - 1
    
    print("Choose a valid language, please! ([1] - [6])", end="")    

  
  # how did you even get here?
  sys.exit(-1)


def check_separator() -> tuple[str, int]:
  retstr: str = ""
  retint: int = -1

  while 1:
    separator: int = int(input(
        "\nWhich line separator would you prefer?\n"
      + " [1]: *\n"
      + " [2]: -\n"
      + " [3]: #\n"
      + " [4]: +\n"
      + " [5]: (empty space)\n"
      + " [6]: Custom separator\n"
      + " [---[ "
    ))

    if separator == 6:
      retstr = input("What would you like to use as a separator? (press enter when finished): ")
      break
    
    match separator:
      case 1:
        retstr = "*"
        break
      case 2:
        retstr = "-"
        break
      case 3:
        retstr = "#"
        break
      case 4:
        retstr = "+"
        break
      case 5:
        retstr = " "
        break
      case _:
        print("Choose a valid separator, please! ([1] - [5])", end="")

  while 1:
    retint: int = int(input("\nHow many lines of separator characters would you like between your comment characters and the comment itself? (+int): "))
    
    if retint >= 0:
      return retstr, retint
    
    print("Read this time.", end="")
  
  # how did you even get here?
  sys.exit(-1)


def biggify_comment(filename: str, language: int, separator: tuple[str, int]) -> None:
  spacing:         int  = get_proper_spacing(filename=filename)
  done_biggifying: bool = False

  while not done_biggifying:
    user_input:      str       = input("Enter comment text to biggify: ")
    biggified_input: list[str] = biggify_str(input_str=user_input, spacing=spacing)

    print_comment(language, separator, biggified_input)

    done_biggifying = input("Would you like to make another with the same font? (y/n): ") != 'y'
  

def print_comment(language: int, separator: tuple[str, int], comment: list[str]) -> None:
  language_bits:  list[str] = get_language_string(language=language)
  separator_bits: list[str] = get_separator_string(separator=separator, length=len(comment[0]))

  if not language_bits or not separator_bits:
    print("Something went wrong with your language or separator choice, exiting...")
    sys.exit(-1)
  
  print(language_bits[0] + separator_bits[0], end="")
  
  for line in comment:
    if line.strip():
      print(separator_bits[1] + line)

  print(separator_bits[2] + language_bits[1])
    

def get_language_string(language: int) -> list[str]:
  match language:
    case 0:
      return ["/*\n", " */\n"]
    case 1:
      return ["\"\"\"\n", "\"\"\"\n"]
    case 2:
      return ["<!--\n", "-->\n"]
    case 3:
      return ["--[[\n", "]]\n"]
    case 4:
      return ["{\n", "}\n"]
    case 5:
      return ["(*\n", "*)\n"]
    case _:
      return []


def get_separator_string(separator: tuple[str, int], length: int) -> list[str]:
  match separator[0]:
    case "*":
      return [(" " + "*" * (length + 2) + "\n") * separator[1] + " *\n", " * ", " *\n" + (" " + "*" * (length + 2) + "\n") * separator[1]]
    case "#":
      return [(" " + "#" * (length + 2) + "\n") * separator[1] + " #\n", " # ", " #\n" + (" " + "#" * (length + 2) + "\n") * separator[1]]
    case "-":
      return [(" " + "-" * (length + 2) + "\n") * separator[1] + " -\n", " - ", " -\n" + (" " + "-" * (length + 2) + "\n") * separator[1]]
    case "+":
      return [(" " + "+" * (length + 2) + "\n") * separator[1] + " +\n", " + ", " +\n" + (" " + "+" * (length + 2) + "\n") * separator[1]]
    case " ":
      return [(" " + " " * (length + 2) + "\n") * separator[1] + "  \n", "   ", "  \n" + (" " + " " * (length + 2) + "\n") * separator[1]]
    case _:
      return  [
                (" " + f"{separator[0]}" * (round((length + 2) / len(separator[0])) + 1) + "\n") * separator[1] + f" {separator[0]}\n", 
                f" {separator[0]} ", 
                f" {separator[0]}\n" + (" " + f"{separator[0]}" * (round((length + 2) / len(separator[0])) + 1) + "\n") * separator[1]
              ]


def get_proper_spacing(filename: str) -> int:
  spacing: int = check_spacing_file(filename=filename)
  if spacing != -1:
    read_ascii_into_tunit(filename=filename, spacing=spacing)
    return spacing
   
  is_properly_spaced: bool      = False
  input_check:        set[int]  = {0x41, 0x42, 0x43}
  spacing                       = 3

  while not is_properly_spaced:
    if not filename:
      read_ascii_into_tunit(spacing=spacing)
    else:
      read_ascii_into_tunit(filename=filename, spacing=spacing)
    
    if not input_check <= translation_unit.keys():
      print("Proper spacing somehow unachievable... Exiting...")
      sys.exit(-1)
    
    print(f"Attempting spacing at {spacing} lines...")

    check: list[str] = []
    key_a, key_b, key_c = sorted(list(input_check))

    for line_a, line_b, line_c in zip(translation_unit[key_a], translation_unit[key_b], translation_unit[key_c]):
      check.append(f"| {line_a.center(spacing * 2)} | {line_b.center(spacing * 2)} | {line_c.center(spacing * 2)} |")
    line = "-" * len(check[0])

    print(line)
    for check_line in check:
      print(check_line)
    print(line)

    is_properly_spaced = input("\nConfirm spacing appears correct (should look like [A][B][C]?) (y/n): ") == "y"
    spacing += 1

  if input("Would you like to save this spacing for future use? (y/n): ") == 'y':
    save_spacing(filename=filename, spacing=spacing - 1)

  return spacing


def save_spacing(filename: str, spacing: int) -> None:
  if not filename:
    return
  if filename[-4:] == ".txt":
    filename = filename[:-4]
  
  try:
    with open(os.path.join(get_root_dir(), "_internal", "res", "spacings.txt"), "a", encoding="utf-8") as file:
      file.write(f"\n{filename}={spacing}")
        
  except FileNotFoundError:
    print("--WARNING--: Missing \"spacings.txt\" file in \".py/\"! Exiting...")
    sys.exit(-1)


def check_spacing_file(filename: str) -> int:
  if not filename:
    return -1
  if filename[-4:] == ".txt":
    filename = filename[:-4]
  
  try:
    with open(os.path.join(get_root_dir(), "_internal", "res", "spacings.txt"), "r", encoding="utf-8") as file:
      for line in file:
        if line.strip():
          font, spacing = line.split("=")

          if font == filename:
            return int(spacing)
        
  except FileNotFoundError:
    print("--WARNING--: Missing \"spacings.txt\" file in \".py/\"! Exiting...")
    sys.exit(-1)

  return -1

def read_ascii_into_tunit(filename: str = "ascii.txt", spacing: int = 11) -> None:
  root_dir: str = get_root_dir()
  if filename[-4:] == ".txt":
    filename = os.path.join(root_dir, ".txt", filename)
  else:
    filename = os.path.join(root_dir, ".txt", filename + ".txt")

  current_giant_char: list[str] = [""] * spacing
  count: int = 0
  
  while count < 2:
    try:
      with open(filename, "r", encoding="utf-8") as file:
        line_count: int = 0
        char_count: int = 0

        for line in file:
          if line_count == spacing:
            translation_unit[char_count + 0x20] = current_giant_char
            current_giant_char                  = [""] * spacing

            line_count = 0
            char_count += 1

          line = line.replace("\n", "")
          current_giant_char[line_count] = line
          line_count += 1

      count += 2

    except FileNotFoundError:
        if (filename[-4:] != ".txt"):
          filename += ".txt"
          count += 1
        else:
          count += 2
    except Exception as e:
        print(f"Encountered an error: {e}")


def biggify_str(input_str: str, spacing: int) -> list[str]:
  biggified_list: list[str] = [""] * spacing

  for character in input_str:
    for ix, line in enumerate(translation_unit[ord(character)]):
      biggified_list[ix] += line
  
  return biggified_list


if __name__ == "__main__":
  filename:  str             = ensure_dir()
  language:  int             = check_language()
  separator: tuple[str, int] = check_separator()

  biggify_comment(filename, language, separator)
