import argparse
from dotenv import load_dotenv
import os
from anthropic import Anthropic
from tqdm import tqdm
from utils import encode_image_to_base64

load_dotenv()

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_base_url = os.getenv('ANTHROPIC_BASE_URL')

client = Anthropic(
    base_url=anthropic_base_url,
    api_key=anthropic_api_key,
)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="claude-opus-4-0", help="Select model (e.g., 'claude-opus-4-0', 'claude-sonnet-4-0', etc)")
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

                try:
                    response = client.messages.create(
                        model=model,
                        max_tokens=1024,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": mime,
                                            "data": b64
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": prompt
                                    }
                                ]
                            }
                        ]
                    )
                    print(f"[Image: {imagename}]\n")
                    print(response.content[0].text)
                    print(f"\n")
                except Exception as e:
                    print(f"Error processing image {imagename}: {e}")