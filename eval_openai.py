import argparse
from dotenv import load_dotenv
import os
from openai import OpenAI
from tqdm import tqdm
from utils import encode_image_to_base64

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_base_url = os.getenv('OPENAI_BASE_URL')

client = OpenAI(
    base_url=openai_base_url,
    api_key=openai_api_key,
)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="o3", help="Select model (e.g., 'o3', 'o4-mini', 'gpt-4o', etc)")
args = parser.parse_args()

model = args.model

root_dir = "data/29"

prompt = (
    "Based on the image provided, which of the following best describes the topological structure of the white regions?\nOptions:\nA. No closed loops.\nB. A single closed loop.\nC. Two closed loops, neither of which fully contains the other.\nD. Two closed loops, with one completely enclosed inside the other.\nE. Three closed loops.\nPlease select the correct answer from the options above. \n"
)

for subfolder in tqdm(os.listdir(root_dir), desc="Processing categories"):
    subfolder_path = os.path.join(root_dir, subfolder)
    if os.path.isdir(subfolder_path):
        for imagename in tqdm(os.listdir(subfolder_path), desc=f"Processing images in Category: {subfolder}"):
            if imagename.lower().endswith(".png"):
                image_path = os.path.join(subfolder_path, imagename)
                
                # Encode image to Base64
                mime, b64 = encode_image_to_base64(image_path)
                
                # Create the image URL (data URI format for OpenAI)
                input_data = f"data:{mime};base64,{b64}"

                try:
                    response = client.chat.completions.create(
                        model=model,                                
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": input_data}}
                                ],
                            }
                        ],
                    )
                    print(f"[Image: {imagename}]\n")
                    print(response.choices[0].message.content)
                    print(f"\n")
                except Exception as e:
                    print(f"Error processing image {imagename}: {e}")