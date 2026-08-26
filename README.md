# Dog Encyclopedia

This version makes the homepage fast by preparing one optimized local image per breed **once**.

## 1. Install

```bash
python3 -m pip install -r requirements.txt
```

## 2. Build the local image cache once

```bash
python3 build_home_images.py
```

This creates:

- `breed_images/`
- `breed_images.json`

The builder rejects pictures smaller than **450×300** when possible. If a breed has no image above that threshold, it uses the largest valid image it can find so the card does not stay blank.

## 3. Run the website

```bash
streamlit run app.py
```

## Breed descriptions

A blank `dogs.json` is included so the app runs immediately. If you already have your populated `dogs.json`, replace the included file with your existing one.

## Rebuild images

Delete the `breed_images` folder and `breed_images.json`, then run:

```bash
python3 -m streamlit run app.py
```
git config --global user.name "Christw"
git config --global user.email "st950314tw@gmail.com"
