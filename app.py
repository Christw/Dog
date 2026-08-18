import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dog Encyclopedia",
    page_icon="🐶",
    layout="wide"
)


# ============================================================
# API URLS
# ============================================================

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"


# ============================================================
# GET ALL BREEDS
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
# GET BREED IMAGES
# ============================================================

@st.cache_data(ttl=3600)
def get_breed_images(breed, amount=6):

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

    # Return only a few images
    return images[:amount]


# ============================================================
# LOAD BREEDS
# ============================================================

try:

    breeds = get_breeds()

except Exception as error:

    st.error(
        "Could not load dog breeds."
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

if st.session_state.selected_breed:

    breed = st.session_state.selected_breed

    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    if st.button("← Back to all breeds"):

        st.session_state.selected_breed = None

        st.rerun()

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.title(
        f"🐶 {breed.title()}"
    )

    st.write(
        f"Explore photos of the {breed.title()}."
    )

    st.divider()

    # --------------------------------------------------------
    # GET PHOTOS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # PHOTO GALLERY
    # --------------------------------------------------------

    st.subheader(
        "📸 Photo Gallery"
    )

    columns = st.columns(4)

    for index, image in enumerate(images):

        with columns[index % 4]:

            st.image(
                image,
                use_container_width=True
            )


    # --------------------------------------------------------
    # VIDEOS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🎥 Videos"
    )

    youtube_url = (
        "https://www.youtube.com/results?search_query="
        + breed
        + "+dog"
    )

    st.link_button(
        f"▶ Watch {breed.title()} videos",
        youtube_url
    )


    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📖 About this breed"
    )

    st.info(
        "Detailed breed information will be added "
        "in the next step."
    )

    st.stop()


# ============================================================
# HOME PAGE
# ============================================================

st.title(
    "🐶 Dog Encyclopedia"
)

st.write(
    "Explore dog breeds, photos and videos."
)


# ============================================================
# SEARCH
# ============================================================

search = st.text_input(
    "🔎 Search for a breed",
    placeholder="Try Labrador..."
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


st.write(
    f"### {len(filtered_breeds)} breed(s) found"
)


# ============================================================
# BREED CARDS
# ============================================================

columns = st.columns(4)


for index, breed in enumerate(filtered_breeds):

    with columns[index % 4]:

        # ----------------------------------------------------
        # GET ONE PHOTO
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
        # BREED NAME
        # ----------------------------------------------------

        st.subheader(
            breed.title()
        )


        # ----------------------------------------------------
        # VIEW BREED BUTTON
        # ----------------------------------------------------

        if st.button(
            "View breed →",
            key=f"breed_{breed}",
            use_container_width=True
        ):

            st.session_state.selected_breed = breed

            st.rerun()
