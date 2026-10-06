# 🐶 Dog Encyclopedia

A Streamlit web app for exploring dog breeds, with breed information and optimized local images for fast loading.

## Installation

Install the required dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Build the Image Cache

Before running the app for the first time, build the local image cache:

```bash
python3 build_home_images.py
```

This creates:

- `breed_images/` — optimized images for each breed
- `breed_images.json` — image metadata used by the app

The image builder prioritizes images that are at least **450 × 300 pixels**. If no image meets this requirement, it uses the largest valid image available so that the breed card does not remain blank.

## Run the App

Start the Streamlit application with:

```bash
streamlit run app.py
```

The app should then open in your browser.

## Breed Descriptions

A blank `dogs.json` file is included so the app can run immediately.

If you already have a populated `dogs.json`, replace the included file with your own version.

## Rebuild the Image Cache

If you want to refresh the breed images, delete:

```text
breed_images/
breed_images.json
```

Then run:

```bash
python3 build_home_images.py
```

After rebuilding the cache, start the app:

```bash
streamlit run app.py
```
