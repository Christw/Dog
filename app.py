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
# API
# ============================================================

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"


# ============================================================
# GET BREEDS
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
# GET BREED IMAGE
# ============================================================

@st.cache_data(ttl=3600)
def get_breed_image(breed):

    url = (
        f"https://dog.ceo/api/"
        f"breed/{breed}/images/random"
    )

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    return response.json()["message"]


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
# TITLE
# ============================================================

st.title("🐶 Dog Encyclopedia")

st.write(
    "Explore dog breeds and discover beautiful dog photos."
)


st.success(
    f"🐕 Found {len(breeds)} dog breeds!"
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
        if search.lower() in breed.lower()
    ]


st.write(
    f"### {len(filtered_breeds)} breed(s) found"
)


# ============================================================
# DISPLAY BREEDS
# ============================================================

columns = st.columns(4)


for index, breed in enumerate(filtered_breeds):

    with columns[index % 4]:

        # ----------------------------------------------------
        # GET IMAGE
        # ----------------------------------------------------

        try:

            image_url = get_breed_image(
                breed
            )

            st.image(
                image_url,
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
        # VIDEO SEARCH
        # ----------------------------------------------------

        youtube_url = (
            "https://www.youtube.com/results?search_query="
            + breed
            + "+dog"
        )

        st.link_button(
            "🎥 Watch videos",
            youtube_url,
            use_container_width=True
        )
