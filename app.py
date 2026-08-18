import streamlit as st
import requests
import json


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dog Encyclopedia",
    page_icon="🐶",
    layout="wide"
)


# ============================================================
# API CONFIGURATION
# ============================================================

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"


# ============================================================
# LOAD DOG CEO BREEDS
# ============================================================

@st.cache_data(ttl=3600)
def get_breeds():

    response = requests.get(
        BREEDS_URL,
        timeout=20
    )

    response.raise_for_status()

    return response.json()["message"]


# ============================================================
# GET IMAGES
# ============================================================

@st.cache_data(ttl=3600)
def get_breed_images(
    breed,
    sub_breed=None,
    amount=8
):

    if sub_breed:

        url = (
            f"https://dog.ceo/api/"
            f"breed/{breed}/"
            f"{sub_breed}/images"
        )

    else:

        url = (
            f"https://dog.ceo/api/"
            f"breed/{breed}/images"
        )

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    images = response.json()["message"]

    return images[:amount]


# ============================================================
# LOAD OUR BREED INFORMATION
# ============================================================

@st.cache_data
def load_breed_information():

    with open(
        "dogs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# CREATE BREED LIST
# ============================================================

def create_breed_list(breeds):

    result = []

    for breed, sub_breeds in breeds.items():

        # ----------------------------------------------------
        # NORMAL BREED
        # ----------------------------------------------------

        if not sub_breeds:

            result.append(
                {
                    "id": breed,
                    "breed": breed,
                    "sub_breed": None,
                    "display_name": breed.title()
                }
            )

        # ----------------------------------------------------
        # BREED WITH SUB-BREEDS
        # ----------------------------------------------------

        else:

            for sub_breed in sub_breeds:

                result.append(
                    {
                        "id": f"{breed}_{sub_breed}",
                        "breed": breed,
                        "sub_breed": sub_breed,
                        "display_name": (
                            f"{sub_breed.title()} "
                            f"{breed.title()}"
                        )
                    }
                )

    return result


# ============================================================
# FIND INFORMATION
# ============================================================

def get_breed_information(
    breed,
    sub_breed=None
):

    search_name = (
        f"{sub_breed} {breed}"
        if sub_breed
        else breed
    )

    search_name = search_name.lower()

    for dog in breed_information:

        if dog["breed"].lower() == search_name:

            return dog

    return None


# ============================================================
# LOAD DATA
# ============================================================

try:

    breeds = get_breeds()

except Exception as error:

    st.error(
        "Could not connect to Dog CEO API."
    )

    st.write(error)

    st.stop()


try:

    breed_information = load_breed_information()

except Exception as error:

    st.error(
        "Could not load dogs.json."
    )

    st.write(error)

    st.stop()


# ============================================================
# CREATE BREED LIST
# ============================================================

all_breeds = create_breed_list(
    breeds
)


# ============================================================
# SESSION STATE
# ============================================================

if "selected_breed" not in st.session_state:

    st.session_state.selected_breed = None


# ============================================================
# BREED DETAIL PAGE
# ============================================================

if st.session_state.selected_breed:

    selected = (
        st.session_state.selected_breed
    )

    breed = selected["breed"]

    sub_breed = selected["sub_breed"]

    display_name = selected[
        "display_name"
    ]

    info = get_breed_information(
        breed,
        sub_breed
    )


    # ========================================================
    # BACK
    # ========================================================

    if st.button(
        "← Back to all breeds"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    # ========================================================
    # TITLE
    # ========================================================

    st.title(
        f"🐶 {display_name}"
    )


    # ========================================================
    # GET IMAGES
    # ========================================================

    try:

        images = get_breed_images(
            breed,
            sub_breed,
            amount=9
        )

    except Exception as error:

        st.error(
            "Could not load breed photos."
        )

        st.write(error)

        st.stop()


    # ========================================================
    # MAIN PHOTO
    # ========================================================

    if images:

        st.image(
            images[0],
            use_container_width=True
        )


    # ========================================================
    # BREED OVERVIEW
    # ========================================================

    if info:

        st.divider()

        st.subheader(
            "📋 Breed Overview"
        )

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "📏 Size",
                info["size"]
            )


        with col2:

            st.metric(
                "⏳ Life span",
                info["life_span"]
            )


        with col3:

            st.metric(
                "⚡ Energy",
                info["energy"]
            )


        with col4:

            st.metric(
                "✂️ Grooming",
                info["grooming"]
            )


    # ========================================================
    # DESCRIPTION
    # ========================================================

    st.divider()

    st.subheader(
        "📖 About this breed"
    )

    if info:

        st.write(
            info["description"]
        )

    else:

        st.info(
            "A detailed description for this breed "
            "has not been added yet."
        )


    # ========================================================
    # BREED FACTS
    # ========================================================

    if info:

        st.divider()

        st.subheader(
            "🐕 Breed Facts"
        )

        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"**🌍 Origin**  \n"
                f"{info['origin']}"
            )

            st.write(
                f"**📏 Height**  \n"
                f"{info['height']}"
            )

            st.write(
                f"**⚖️ Weight**  \n"
                f"{info['weight']}"
            )


        with col2:

            st.write(
                f"**❤️ Temperament**  \n"
                f"{info['temperament']}"
            )

            st.write(
                f"**⚡ Energy**  \n"
                f"{info['energy']}"
            )

            st.write(
                f"**✂️ Grooming**  \n"
                f"{info['grooming']}"
            )


    # ========================================================
    # PHOTO GALLERY
    # ========================================================

    st.divider()

    st.subheader(
        "📸 Photo Gallery"
    )

    if len(images) > 1:

        columns = st.columns(4)

        for index, image in enumerate(
            images[1:]
        ):

            with columns[index % 4]:

                st.image(
                    image,
                    use_container_width=True
                )


    # ========================================================
    # VIDEOS
    # ========================================================

    st.divider()

    st.subheader(
        "🎥 Videos"
    )

    youtube_search = (
        display_name.replace(
            " ",
            "+"
        )
        + "+dog+breed"
    )

    youtube_url = (
        "https://www.youtube.com/results?search_query="
        + youtube_search
    )

    st.link_button(
        f"▶ Watch {display_name} videos",
        youtube_url
    )


    # ========================================================
    # BACK
    # ========================================================

    st.divider()

    if st.button(
        "← Back to all breeds",
        key="bottom_back"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    st.stop()


# ============================================================
# HOME PAGE
# ============================================================

st.title(
    "🐶 Dog Encyclopedia"
)

st.write(
    "Explore dog breeds, photos, characteristics "
    "and videos."
)


# ============================================================
# STATISTICS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🐕 Breed varieties",
        len(all_breeds)
    )


with col2:

    st.metric(
        "📖 Detailed breeds",
        len(breed_information)
    )


with col3:

    st.metric(
        "📸 Image source",
        "Dog CEO"
    )


# ============================================================
# SEARCH
# ============================================================

st.divider()

search = st.text_input(
    "🔎 Search for a dog breed",
    placeholder="Try Golden Retriever..."
)


# ============================================================
# FILTER
# ============================================================

filtered_breeds = all_breeds


if search:

    filtered_breeds = [
        dog
        for dog in all_breeds
        if search.lower()
        in dog["display_name"].lower()
    ]


# ============================================================
# RESULTS
# ============================================================

st.write(
    f"### {len(filtered_breeds)} breed(s) found"
)


# ============================================================
# BREED CARDS
# ============================================================

columns = st.columns(4)


for index, dog in enumerate(
    filtered_breeds
):

    with columns[index % 4]:

        breed = dog["breed"]

        sub_breed = dog[
            "sub_breed"
        ]

        display_name = dog[
            "display_name"
        ]


        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        info = get_breed_information(
            breed,
            sub_breed
        )


        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        try:

            images = get_breed_images(
                breed,
                sub_breed,
                amount=1
            )

            if images:

                st.image(
                    images[0],
                    use_container_width=True
                )

        except Exception:

            st.info(
                "No image available"
            )


        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        st.subheader(
            display_name
        )


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        if info:

            description = info[
                "description"
            ]

            if len(description) > 120:

                description = (
                    description[:120]
                    + "..."
                )

            st.write(
                description
            )

        else:

            st.caption(
                "Breed information coming soon."
            )


        # ----------------------------------------------------
        # LIFE SPAN
        # ----------------------------------------------------

        if info:

            st.caption(
                f"⏳ {info['life_span']} "
                f"• ⚡ {info['energy']}"
            )


        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        if st.button(
            "View breed →",
            key=f"view_{dog['id']}",
            use_container_width=True
        ):

            st.session_state.selected_breed = dog

            st.rerun()
