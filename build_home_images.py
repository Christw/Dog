import os
import json
import random
import requests
from io import BytesIO
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"
OUTPUT_FOLDER = "breed_images"
MANIFEST_FILE = "breed_images.json"

MIN_WIDTH = 450
MIN_HEIGHT = 300
OUTPUT_WIDTH = 800
OUTPUT_HEIGHT = 600
MAX_WORKERS = 12
MAX_CANDIDATES = 20

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})


def get_breeds():
    response = session.get(BREEDS_URL, timeout=20)
    response.raise_for_status()
    return response.json()["message"]


def create_breed_list(breeds):
    result = []
    for breed, sub_breeds in breeds.items():
        if not sub_breeds:
            result.append({"id": breed, "breed": breed, "sub_breed": None})
        else:
            for sub_breed in sub_breeds:
                result.append({
                    "id": f"{breed}_{sub_breed}",
                    "breed": breed,
                    "sub_breed": sub_breed,
                })
    return result


def get_image_urls(breed, sub_breed=None):
    if sub_breed:
        url = f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images"
    else:
        url = f"https://dog.ceo/api/breed/{breed}/images"

    response = session.get(url, timeout=15)
    response.raise_for_status()
    urls = response.json()["message"]
    random.shuffle(urls)
    return urls


def download_image(url):
    try:
        response = session.get(url, timeout=8)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception:
        return None


def find_good_image(urls):
    best_image = None
    best_area = 0

    for url in urls[:MAX_CANDIDATES]:
        image = download_image(url)
        if image is None:
            continue

        width, height = image.size
        area = width * height

        if area > best_area:
            best_area = area
            best_image = image.copy()

        if width >= MIN_WIDTH and height >= MIN_HEIGHT:
            return image

    return best_image


def save_breed_image(dog):
    breed_id = dog["id"]
    filename = f"{breed_id}.jpg"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    if os.path.exists(filepath):
        return breed_id, filepath

    try:
        urls = get_image_urls(dog["breed"], dog["sub_breed"])
        if not urls:
            print(f"⚠ No images: {breed_id}")
            return breed_id, None

        image = find_good_image(urls)
        if image is None:
            print(f"⚠ Could not load any image: {breed_id}")
            return breed_id, None

        image = ImageOps.fit(
            image,
            (OUTPUT_WIDTH, OUTPUT_HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

        image.save(filepath, "JPEG", quality=82, optimize=True)
        print(f"✓ {breed_id}")
        return breed_id, filepath

    except Exception as error:
        print(f"✗ {breed_id}: {error}")
        return breed_id, None


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("Getting breeds...")
    dogs = create_breed_list(get_breeds())
    print(f"{len(dogs)} breeds found")

    manifest = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(save_breed_image, dog): dog for dog in dogs}

        for future in as_completed(futures):
            breed_id, filepath = future.result()
            if filepath:
                manifest[breed_id] = filepath

    with open(MANIFEST_FILE, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2)

    print("\n============================")
    print("DONE")
    print("============================")
    print(f"{len(manifest)} images saved")
    print("Now run: streamlit run app.py")


if __name__ == "__main__":
    main()
