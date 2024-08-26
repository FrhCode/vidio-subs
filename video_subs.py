import sys
import logging
import argparse
import os

import time
import ffmpeg
from faster_whisper import WhisperModel
import pandas as pd

from utils import extract_file_name

def formattedtime(seconds):
    logging.info(f"formattedtime({seconds})")
    final_time = time.strftime("%H:%M:%S", time.gmtime(float(seconds)))
    return f"{final_time},{seconds.split('.')[1]}"  

def extract_audio(input_video, output_folder):
  logging.info(f"extract_audio({input_video}, {output_folder})")
  
  # Ensure output folder exists
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  
  extracted_audio = f"{output_folder}/{extract_file_name(input_video)}.mp3"
    
  try:
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    logging.info(f"Audio extracted successfully to {extracted_audio}")
  except ffmpeg.Error as e:
    logging.error(f"ffmpeg error: {e.stderr.decode('utf8')}")
    raise
    
  return extracted_audio

def transcribe(audio):
    logging.info(f"transcribe({audio})")
    model = WhisperModel("base")
    segments, info = model.transcribe(audio, vad_filter=False, vad_parameters=dict(min_silence_duration_ms=100))
    language = info[0]
    print("Transcription language", info[0])
    segments = list(segments)
    return language, segments

def writetocsv(segments, input_video, output_folder):
    output = f"{output_folder}/{extract_file_name(input_video)}.csv"
    cols = ["start", "end", "text"]
    data = []
    for segment in segments:
        start = formattedtime(format(segment.start, ".3f"))
        end = formattedtime(format(segment.end, ".3f"))
        data.append([start, end, segment.text])
        # print("%.2fs --> %.2fs : %s" % (segment.start, segment.end, segment.text))
        # print(f"[{start} --> {end}] : {segment.text}")

    df = pd.DataFrame(data, columns=cols)
    df.to_csv(output, index=False)
    return output

def parseargs(args):
    logging.info("parseargs()")
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="Input video file which needs subtitles")
    parser.add_argument("--output", help="Output csv file with subtitles and timestamp")

    return parser.parse_args(args)



def main(args):
    logging.info(f"main({args.input}, {args.output}")
    extracted_audio = extract_audio(args.input, args.output)
    language, segments = transcribe(audio=extracted_audio)
    writetocsv(segments,args.input, args.output)

    sys.exit(0)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='video_subs %(asctime)s - %(levelname)s - %(message)s')
    logging.info("Watch out! Program started...")

    sys_args = parseargs(sys.argv[1:])
    main(sys_args)

