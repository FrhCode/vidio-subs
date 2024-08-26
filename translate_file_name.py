from deep_translator import GoogleTranslator
import logging
import os
import sys
import argparse

# Initialize the translator

def parseargs(args):
  logging.info("parseargs()")
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", help="Input video file which needs subtitles", required=True)
  return parser.parse_args(args)

def translate_file_name(file_name):

  # Split the file path into directory, base name, and extension
  dir_name, file_name_with_ext = os.path.split(file_name)
  base_name, ext = os.path.splitext(file_name_with_ext)

  # Construct the subtitles file name
  subs_name = os.path.join(dir_name, f"{base_name}.srt")
  en_subs_name = os.path.join(dir_name, f"{base_name} en.srt")

  try:
    # Translate the base name of the file to Indonesian
    translated_base_name = GoogleTranslator(source='auto', target='id').translate(base_name) 

    # Construct new file names
    translated_file_name = os.path.join(dir_name, f"{translated_base_name}{ext}")
    translated_subs_name = os.path.join(dir_name, f"{translated_base_name}.srt")
    # translated en srt file
    translated_en_subs_name = os.path.join(dir_name, f"{translated_base_name} en.srt")

    # Rename the video file
    os.rename(file_name, translated_file_name)
    logging.info(f"Renamed video file to {translated_file_name}")

    # Rename the subtitles file if it exists
    if os.path.exists(subs_name):
      os.rename(subs_name, translated_subs_name)
      logging.info(f"Renamed subtitles file to {translated_subs_name}")
    else:
      logging.warning(f"Subtitles file {subs_name} does not exist")
      
    if os.path.exists(f"{en_subs_name}"):
      os.rename(f"{en_subs_name}", translated_en_subs_name)
      logging.info(f"Renamed subtitles file to {translated_en_subs_name}")
    else:
      logging.warning(f"Subtitles file {subs_name}_en does not exist")

  except Exception as e:
    logging.error(f"An error occurred: {e}")

def remove_forbidden_characters(args):
  logging.info(f"remove_forbidden_characters({args.input})")
  
  forbidden_characters = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.','-','_']
  file_name_with_path = args.input
  
  dir_name, file_name_with_ext = os.path.split(file_name_with_path)
  base_name, ext = os.path.splitext(file_name_with_ext)
  
  # Remove forbidden characters from the base name
  sanitized_base_name = base_name
  for char in forbidden_characters:
    if char in sanitized_base_name:
      sanitized_base_name = sanitized_base_name.replace(char, ' ')
  
  # Construct the new file name
  new_file_name_with_ext = sanitized_base_name + ext
  new_file_name_with_path = os.path.join(dir_name, new_file_name_with_ext)
  
  # Rename the original file
  try:
    os.rename(file_name_with_path, new_file_name_with_path)
    logging.info(f"File renamed to {new_file_name_with_path}")
  except OSError as e:
    logging.error(f"Error renaming file: {e}")
    raise
  
  # Rename associated .srt and _en.srt files
  srt_files = [
    os.path.join(dir_name, f"{base_name}.srt"),
    os.path.join(dir_name, f"{base_name}_en.srt")
  ]
  
  for srt_file in srt_files:
    if os.path.exists(srt_file):
      srt_base_name, srt_ext = os.path.splitext(os.path.basename(srt_file))
      sanitized_srt_base_name = srt_base_name
      
      for char in forbidden_characters:
        if char in sanitized_srt_base_name:
          sanitized_srt_base_name = sanitized_srt_base_name.replace(char, ' ')
      
      new_srt_file_name = sanitized_srt_base_name + srt_ext
      new_srt_file_path = os.path.join(dir_name, new_srt_file_name)
      
      try:
        os.rename(srt_file, new_srt_file_path)
        logging.info(f"Subtitle file renamed to {new_srt_file_path}")
      except OSError as e:
        logging.error(f"Error renaming subtitle file {srt_file}: {e}")
        raise
  
  return new_file_name_with_path
  

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  logging.info("Watch out! Program started...")

  sys_args = parseargs(sys.argv[1:])
  valid_file_name = remove_forbidden_characters(sys_args)
  translate_file_name(valid_file_name)
