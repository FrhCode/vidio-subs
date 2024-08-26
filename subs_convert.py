import sys
import logging
import argparse
import csv
from utils import extract_file_name

def generatesrt(csv_file):
    rows = []
    count = 0
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count += 1
            txt = f"{count}\n{row['start']} --> {row['end']}\n{row['text'].strip()}\n\n"
            rows.append(txt)

    return rows

def parseargs(args):
    logging.info("parseargs()")
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="Input video file which needs subtitles")
    parser.add_argument("--output", help="Output csv file with subtitles and timestamp")

    return parser.parse_args(args)

def main(args):
    logging.info(f"main({args.input}, {args.output}")
    srt_data = generatesrt(args.input)

    with open(f"{args.output}/{extract_file_name(args.input)}_en.srt", "w") as srt_file:
        for row in srt_data:
            srt_file.write(row)

    sys.exit(0)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Watch out! Program started...")

    sys_args = parseargs(sys.argv[1:])
    main(sys_args)