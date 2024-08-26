import os
import logging

def get_file_name_for_translate_subs(input_file):
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
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG, format='index %(asctime)s - %(levelname)s - %(message)s')
  logging.info("Watch out! Program started...")
  
  video_extensions = (".mp4", ".avi", ".mkv", ".mov")
  
  for root, dirs, files in os.walk("resources"): 
    for file in files:
      if file.endswith(video_extensions):  
        input_file = os.path.join(root, file)
                
        input_file = input_file.replace("\\", "/")
        root = root.replace("\\", "/")
        
        files_to_skip = []
        
        base_name, ext = os.path.splitext(input_file)
        if file in files_to_skip:
          continue
        
        input_args_video_subs = input_file
        input_args_subs_convert = base_name + ".csv"
        input_args_translate_subs = base_name + "_en.srt"
        output_args = root 
        
        logging.info(f"input_args: {input_args_video_subs}")
        logging.info(f"output_args: {output_args}")
        
        # Use properly quoted arguments to handle spaces
        os.system(f'python video_subs.py --input "{input_args_video_subs}" --output "{output_args}"')
        os.system(f'python subs_convert.py --input "{input_args_subs_convert}" --output "{output_args}"')
        os.system(f'python translate_subs.py --input "{input_args_translate_subs}"')
        os.system(f'python delete_unused_file.py --input "{input_args_video_subs}"')
        os.system(f'python translate_file_name.py --input "{input_args_video_subs}"')
        
        


