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

BREEDS_URL = (
    "https://dogapi.dog/api/v2/breeds"
)


# ============================================================
# GET BREEDS
# ============================================================

@st.cache_data(ttl=3600)
def get_breeds():

    response = requests.get(
        BREEDS_URL,
        params={
            "page[size]": 1000
        },
        timeout=20
    )

    response.raise_for_status()

    return response.json()["data"]


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
    "Explore dog breeds, characteristics, "
    "life span and more."
)


# ============================================================
# API STATUS
# ============================================================

st.success(
    f"🐕 Loaded {len(breeds)} dog breeds!"
)


# ============================================================
# SEARCH
# ============================================================

search = st.text_input(
    "🔎 Search for a dog breed",
    placeholder="Try Labrador..."
)


# ============================================================
# FILTER
# ============================================================

filtered_breeds = breeds


if search:

    filtered_breeds = [
        breed
        for breed in breeds
        if search.lower()
        in breed["attributes"]["name"].lower()
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


for index, breed in enumerate(filtered_breeds):

    with columns[index % 4]:

        attributes = breed["attributes"]

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        st.subheader(
            attributes["name"]
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = attributes.get(
            "description"
        )

        if description:

            # Keep cards short
            if len(description) > 150:

                description = (
                    description[:150]
                    + "..."
                )

            st.write(
                description
            )

        # ----------------------------------------------------
        # LIFE SPAN
        # ----------------------------------------------------

        life = attributes.get(
            "life"
        )

        if life:

            minimum = life.get(
                "min"
            )

            maximum = life.get(
                "max"
            )

            if minimum and maximum:

                st.write(
                    f"❤️ Life span: "
                    f"{minimum}–{maximum} years"
                )

        # ----------------------------------------------------
        # VIEW BUTTON
        # ----------------------------------------------------

        if st.button(
            "View breed →",
            key=f"breed_{breed['id']}",
            use_container_width=True
        ):

            st.session_state.selected_breed = breed

            st.rerun()
