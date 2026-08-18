import requests
import json


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "https://dog.ceo/api/breeds/list/all"

OUTPUT_FILE = "dogs.json"


# ============================================================
# GET BREEDS FROM DOG CEO
# ============================================================

def get_breeds():

    print("Connecting to Dog CEO API...")

    response = requests.get(
        API_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]


# ============================================================
# CREATE BREED ENTRY
# ============================================================

def create_breed_entry(
    breed,
    sub_breed=None
):

    # --------------------------------------------------------
    # DISPLAY NAME
    # --------------------------------------------------------

    if sub_breed:

        display_name = (
            f"{sub_breed.title()} "
            f"{breed.title()}"
        )

        api_name = (
            f"{sub_breed} {breed}"
        )

    else:

        display_name = breed.title()

        api_name = breed


    # --------------------------------------------------------
    # DEFAULT INFORMATION
    # --------------------------------------------------------

    return {

        "breed": api_name,

        "name": display_name,

        "origin": "Information not available",

        "group": "Information not available",

        "size": "Information not available",

        "height": "Information not available",

        "weight": "Information not available",

        "life_span": "Information not available",

        "temperament": "Information not available",

        "energy": "Information not available",

        "grooming": "Information not available",

        "description": (
            f"{display_name} is a dog breed "
            f"or breed variety. More detailed "
            f"information will be added soon."
        )

    }


# ============================================================
# CREATE ALL BREEDS
# ============================================================

def create_breed_database(breeds):

    breed_database = []


    for breed, sub_breeds in breeds.items():

        # ----------------------------------------------------
        # NORMAL BREED
        # ----------------------------------------------------

        if not sub_breeds:

            entry = create_breed_entry(
                breed
            )

            breed_database.append(
                entry
            )


        # ----------------------------------------------------
        # SUB-BREEDS
        # ----------------------------------------------------

        else:

            for sub_breed in sub_breeds:

                entry = create_breed_entry(
                    breed,
                    sub_breed
                )

                breed_database.append(
                    entry
                )


    return breed_database


# ============================================================
# SAVE JSON
# ============================================================

def save_database(data):

    print(
        f"Saving {len(data)} breeds..."
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        breeds = get_breeds()

        database = create_breed_database(
            breeds
        )

        save_database(
            database
        )

        print()
        print(
            "✅ dogs.json created successfully!"
        )

        print(
            f"🐕 Total breed entries: "
            f"{len(database)}"
        )

    except Exception as error:

        print()
        print(
            "❌ Something went wrong:"
        )

        print(error)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()
