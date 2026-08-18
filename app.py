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
# LOAD BREEDS FROM DOG CEO API
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
# GET IMAGES FOR A BREED
# ============================================================

@st.cache_data(ttl=3600)
def get_breed_images(breed, amount=8):

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
# FIND BREED INFORMATION
# ============================================================

def get_breed_information(breed):

    breed = breed.lower()

    for dog in breed_information:

        if dog["breed"].lower() == breed:

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
# SESSION STATE
# ============================================================

if "selected_breed" not in st.session_state:

    st.session_state.selected_breed = None


# ============================================================
# BREED DETAIL PAGE
# ============================================================

if st.session_state.selected_breed is not None:

    breed = st.session_state.selected_breed

    info = get_breed_information(
        breed
    )


    # ========================================================
    # BACK BUTTON
    # ========================================================

    if st.button(
        "← Back to all breeds"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    # ========================================================
    # BREED TITLE
    # ========================================================

    if info:

        display_name = info["name"]

    else:

        display_name = breed.title()


    st.title(
        f"🐶 {display_name}"
    )


    # ========================================================
    # MAIN PHOTO
    # ========================================================

    try:

        images = get_breed_images(
            breed,
            amount=8
        )

    except Exception as error:

        st.error(
            "Could not load breed photos."
        )

        st.write(error)

        st.stop()


    if images:

        st.image(
            images[0],
            use_container_width=True
        )


    # ========================================================
    # BASIC INFORMATION
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
                f"**⚡ Energy level**  \n"
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

        gallery_images = images[1:]

        columns = st.columns(4)

        for index, image in enumerate(
            gallery_images
        ):

            with columns[index % 4]:

                st.image(
                    image,
                    use_container_width=True
                )


    # ========================================================
    # YOUTUBE VIDEOS
    # ========================================================

    st.divider()

    st.subheader(
        "🎥 Videos"
    )

    youtube_url = (
        "https://www.youtube.com/results?search_query="
        + display_name.replace(" ", "+")
        + "+dog+breed"
    )

    st.link_button(
        f"▶ Watch {display_name} videos",
        youtube_url
    )


    # ========================================================
    # BACK BUTTON
    # ========================================================

    st.divider()

    if st.button(
        "← Back to all breeds",
        key="bottom_back"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    # Stop here so the homepage doesn't appear below
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
        "🐕 Dog Breeds",
        len(breeds)
    )


with col2:

    st.metric(
        "📖 Detailed Breeds",
        len(breed_information)
    )


with col3:

    st.metric(
        "📸 Photo API",
        "Dog CEO"
    )


# ============================================================
# SEARCH
# ============================================================

st.divider()

search = st.text_input(
    "🔎 Search for a dog breed",
    placeholder="Try Labrador, Poodle, Husky..."
)


# ============================================================
# FILTER BREEDS
# ============================================================

filtered_breeds = breeds


if search:

    filtered_breeds = [
        breed
        for breed in breeds
        if search.lower()
        in breed.lower()
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


for index, breed in enumerate(
    filtered_breeds
):

    with columns[index % 4]:

        # ----------------------------------------------------
        # GET BREED INFORMATION
        # ----------------------------------------------------

        info = get_breed_information(
            breed
        )


        # ----------------------------------------------------
        # DISPLAY NAME
        # ----------------------------------------------------

        if info:

            display_name = info["name"]

        else:

            display_name = breed.title()


        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        try:

            images = get_breed_images(
                breed,
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
        # SHORT DESCRIPTION
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


        # ----------------------------------------------------
        # LIFE SPAN
        # ----------------------------------------------------

        if info:

            st.caption(
                f"⏳ {info['life_span']}  "
                f"• ⚡ {info['energy']}"
            )


        # ----------------------------------------------------
        # VIEW BUTTON
        # ----------------------------------------------------

        if st.button(
            "View breed →",
            key=f"view_{breed}",
            use_container_width=True
        ):

            st.session_state.selected_breed = breed

            st.rerun()
