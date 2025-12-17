import os
import sys

translation_unit: dict[int, list[str]] = {}

def biggify_comment(filename: str) -> None:
  spacing:         int       = get_proper_spacing(filename=filename)
  done_biggifying: bool      = False

  while not done_biggifying:
    user_input:      str       = input("Enter comment text to biggify: ")
    biggified_input: list[str] = biggify_str(input_str=user_input, spacing=spacing)
    asterisks:       str       = "*" * (len(biggified_input[0]) + 2)

    print("/*\n"
        + " " + asterisks + "\n"
        + " " + asterisks + "\n"
        + " *")
    
    for line in biggified_input:
      if line.strip():
        print(" * " + line)

    print(" *\n"
        + " " + asterisks + "\n"
        + " " + asterisks + "\n"
        + " */\n")
    
    done_biggifying = input("Would you like to make another with the same font? (y/n): ") != 'y'
  

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
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "spacings.txt"), "a", encoding="utf-8") as file:
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
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "spacings.txt"), "r", encoding="utf-8") as file:
      for line in file:
        font, spacing = line.split("=")

        if font == filename:
          return int(spacing)
        
  except FileNotFoundError:
    print("--WARNING--: Missing \"spacings.txt\" file in \".py/\"! Exiting...")
    sys.exit(-1)

  return -1

def read_ascii_into_tunit(filename: str = "ascii.txt", spacing: int = 11) -> None:
  parent_dir: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  if filename[-4:] == ".txt":
    filename = os.path.join(parent_dir, ".txt", filename)
  else:
    filename = os.path.join(parent_dir, ".txt", filename + ".txt")

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
  filename: str = input("Enter target ASCII filename: ")

  biggify_comment(filename)