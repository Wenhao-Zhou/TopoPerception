import argparse
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
from tqdm import tqdm

load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')
google_api_endpoint = os.getenv('GOOGLE_API_ENDPOINT')

genai.configure(
    api_key=google_api_key,
    transport="rest",
    client_options={"api_endpoint": google_api_endpoint},
)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="gemini-2.5-pro", help="Select model (e.g., 'gemini-2.5-pro', 'gemini-2.5-flash', etc)")
args = parser.parse_args()

model_name = args.model

root_dir = "data/29"

text = "Based on the image provided, which of the following best describes the topological structure of the white regions?\nOptions:\nA. No closed loops.\nB. A single closed loop.\nC. Two closed loops, neither of which fully contains the other.\nD. Two closed loops, with one completely enclosed inside the other.\nE. Three closed loops.\nPlease select the correct answer from the options above. \n"

model = genai.GenerativeModel(model_name)

for subfolder in tqdm(os.listdir(root_dir), desc="Processing categories"):
    subfolder_path = os.path.join(root_dir, subfolder)
    if os.path.isdir(subfolder_path):
        for imagename in tqdm(os.listdir(subfolder_path), desc=f"Processing images in Category: {subfolder}"):
            if imagename.lower().endswith(".png"):
                image_path = os.path.join(subfolder_path, imagename)

                with Image.open(image_path) as image:
                    prompt = [text, image]
                    try:
                        response = model.generate_content(prompt)
                        print(f"[Image: {imagename}]\n")
                        print(response.text)
                        print(f"\n")
                    except Exception as e:
                        print(f"Error processing image {imagename}: {e}")