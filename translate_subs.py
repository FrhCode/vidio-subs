import logging
import os
import sys
import argparse
import re
from deep_translator import GoogleTranslator
import time


# Regular expressions for timestamps and numbers
timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
number_pattern = re.compile(r'^\d+$')

from_code = "en"
to_code = "id"

def parseargs(args):
    logging.info("parseargs()")
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="Input video file which needs subtitles")
    return parser.parse_args(args)

def generate_file_name(input_file):
    # Log the input filename
    logging.info(f"generate_file_name({input_file})")
    
    # Split the file path into directory, base name, and extension
    dir_name, file_name = os.path.split(input_file)
    base_name, ext = os.path.splitext(file_name)
    
    # Replace '_en' with an empty string in the base name
    new_base_name = base_name.replace('_en', '')
    
    # Reconstruct the file path with the new base name
    new_file_name = os.path.join(dir_name, new_base_name + ext)
    
    return new_file_name
    

def main(args):
  with open(args.input, 'r') as file:
      subs = file.readlines()

  
  total_lines = len(subs)

  with open(generate_file_name(args.input), 'w') as file:
    for i, line in enumerate(subs):
      
      line = line.strip()  # Remove any surrounding whitespace or newline characters

      # Check if the line is empty, a timestamp, or a number
      if not line or timestamp_pattern.match(line) or number_pattern.match(line):
        file.write(line + '\n')
      else:
        translated_line = GoogleTranslator(source='auto', target='id').translate(line) 
        file.write(translated_line + '\n')
      
      progress_percentage = (i + 1) / total_lines * 100
      logging.info(f"Progress: {progress_percentage:.2f}%")
      
      time.sleep(0.2)
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format=f'translating: {sys.argv[2]} %(asctime)s - %(levelname)s - %(message)s')
  logging.info("Watch out! Program started...")

  log_file = 'translation.log'
  file_handler = logging.FileHandler(log_file)
  file_handler.setLevel(logging.INFO)
  
  formatter = logging.Formatter(f'translating: {sys.argv[2]} %(asctime)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)
  
  logging.getLogger().addHandler(file_handler)

  sys_args = parseargs(sys.argv[1:])
  main(sys_args)