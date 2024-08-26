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
  
  dir_name, file_name_with_ext = os.path.split(file_name)
  base_name, ext = os.path.splitext(file_name_with_ext)
  en_sub = ''
  mp3 = os.path.join(dir_name, f"{base_name}.mp3")
  csv = os.path.join(dir_name, f"{base_name}.csv")
  
  delete_files = [en_sub, mp3, csv]
  
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