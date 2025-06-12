
from random import randint
from PIL import Image
import requests
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {os.getenv('HuggingFaceAPIKey')}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def generate_images(prompt: str):
    if not os.path.exists("Data"):
        os.makedirs("Data")

    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        image_bytes = query(payload)
        if image_bytes:
            try:
                with open(f"Data/{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
                    f.write(image_bytes)
            except IOError as e:
                print(f"Failed to save image {i + 1}: {e}")
        else:
            print(f"Failed to generate image {i + 1}")

def GenerateImages(prompt: str):
    generate_images(prompt)
    open_images(prompt)

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generating Images....")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(5)  # Add a delay to reduce CPU usage
    except Exception as e:
        print(f"An error occurred: {e}")
        sleep(5)