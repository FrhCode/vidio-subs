from deep_translator import GoogleTranslator
import logging
import os
import sys
import argparse

def parseargs(args):
    logging.info("parseargs()")
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="Input video file which needs subtitles")
    return parser.parse_args(args)
  

def main(args):
  file_name = args.input
  # delete file with name
  # resouces/c_en.srt
  # resources/c.mp3
  # resources/c.csv
  
  # en_sub = f"{file_name.split('.')[0]}_en.srt"
  en_sub = ''
  delete_files = [en_sub, f"{file_name.split('.')[0]}.mp3", f"{file_name.split('.')[0]}.csv"]
  
  for file in delete_files:
    try:
      os.remove(file)
      logging.info(f"Deleted {file}")
    except FileNotFoundError:
      logging.info(f"{file} not found")

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  logging.info("Watch out! Program started...")

  sys_args = parseargs(sys.argv[1:])
  main(sys_args)