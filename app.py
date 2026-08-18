import streamlit as st
import requests
import json
import html


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Dog Encyclopedia",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #ffffff;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        padding: 45px 0 35px 0;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.05;
        letter-spacing: -2px;
        font-weight: 750;
        color: #222222;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 19px;
        line-height: 1.5;
        color: #717171;
        margin-top: 14px;
        max-width: 650px;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-heading {
        font-size: 25px;
        font-weight: 700;
        color: #222222;
        letter-spacing: -0.5px;
        margin-top: 30px;
        margin-bottom: 18px;
    }


    /* ========================================================
       DOG CARD
       ======================================================== */

    .dog-image {
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 16px;
        display: block;
    }

    .dog-card-title {
        font-size: 16px;
        font-weight: 650;
        color: #222222;
        margin-top: 10px;
        line-height: 1.3;
    }

    .dog-card-description {
        font-size: 14px;
        color: #717171;
        line-height: 1.45;
        margin-top: 5px;
        min-height: 40px;
    }

    .dog-card-meta {
        font-size: 13px;
        color: #717171;
        margin-top: 7px;
        margin-bottom: 8px;
    }


    /* ========================================================
       DETAIL PAGE
       ======================================================== */

    .detail-title {
        font-size: 44px;
        font-weight: 750;
        letter-spacing: -1.5px;
        color: #222222;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .detail-subtitle {
        font-size: 15px;
        color: #717171;
        margin-bottom: 25px;
    }

    .detail-description {
        font-size: 17px;
        line-height: 1.75;
        color: #484848;
    }


    /* ========================================================
       FACTS
       ======================================================== */

    .fact {
        padding: 16px 0;
        border-bottom: 1px solid #eeeeee;
    }

    .fact-label {
        font-size: 13px;
        color: #717171;
        margin-bottom: 5px;
    }

    .fact-value {
        font-size: 16px;
        font-weight: 600;
        color: #222222;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid #dddddd;
        background: white;
        color: #222222;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #222222;
        background: #f7f7f7;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .hero-title {
            font-size: 38px;
            letter-spacing: -1px;
        }

        .hero-subtitle {
            font-size: 17px;
        }

        .detail-title {
            font-size: 34px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API
# ============================================================

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"


# ============================================================
# LOAD BREEDS
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
# LOAD LOCAL BREED INFORMATION
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
        # SUB BREEDS
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
# FIND BREED INFORMATION
# ============================================================

def get_breed_information(
    breed,
    sub_breed=None
):

    if sub_breed:

        search_name = (
            f"{sub_breed} {breed}"
        )

    else:

        search_name = breed

    search_name = search_name.lower()


    # --------------------------------------------------------
    # SEARCH JSON
    # --------------------------------------------------------

    for dog in breed_information:

        if dog["breed"].lower() == search_name:

            return dog


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if sub_breed:

        display_name = (
            f"{sub_breed.title()} "
            f"{breed.title()}"
        )

    else:

        display_name = breed.title()


    return {
        "breed": search_name,
        "name": display_name,
        "origin": "Information coming soon",
        "group": "Dog breed",
        "size": "Information coming soon",
        "height": "Information coming soon",
        "weight": "Information coming soon",
        "life_span": "Information coming soon",
        "temperament": "Information coming soon",
        "energy": "Information coming soon",
        "grooming": "Information coming soon",
        "description": (
            f"{display_name} is a dog breed or "
            f"breed variety. Detailed information "
            f"about this breed will be added soon."
        )
    }


# ============================================================
# LOAD DATA
# ============================================================

try:

    breeds = get_breeds()

    breed_information = (
        load_breed_information()
    )

except Exception as error:

    st.error(
        "Unable to load the dog encyclopedia."
    )

    st.write(error)

    st.stop()


# ============================================================
# CREATE BREED DATABASE
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
# ============================================================
# DETAIL PAGE
# ============================================================
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
    # BACK BUTTON
    # ========================================================

    if st.button(
        "← Back to breeds"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    # ========================================================
    # TITLE
    # ========================================================

    st.markdown(
        f"""
        <div class="detail-title">
            {html.escape(display_name)}
        </div>

        <div class="detail-subtitle">
            Dog Encyclopedia
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # LOAD IMAGES
    # ========================================================

    try:

        images = get_breed_images(
            breed,
            sub_breed,
            amount=9
        )

    except Exception:

        images = []


    # ========================================================
    # MAIN IMAGE
    # ========================================================

    if images:

        st.image(
            images[0],
            use_container_width=True
        )

    else:

        st.info(
            "No photos available."
        )


    # ========================================================
    # ABOUT + FACTS
    # ========================================================

    left, right = st.columns(
        [2, 1],
        gap="large"
    )


    # ========================================================
    # ABOUT
    # ========================================================

    with left:

        st.markdown(
            """
            <div class="section-heading">
                About this breed
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="detail-description">
                {html.escape(
                    str(info["description"])
                )}
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FACTS
    # ========================================================

    with right:

        st.markdown(
            """
            <div class="section-heading">
                Quick facts
            </div>
            """,
            unsafe_allow_html=True
        )


        facts = [
            (
                "🌍 Origin",
                info["origin"]
            ),
            (
                "📏 Height",
                info["height"]
            ),
            (
                "⚖️ Weight",
                info["weight"]
            ),
            (
                "⏳ Life span",
                info["life_span"]
            ),
            (
                "❤️ Temperament",
                info["temperament"]
            ),
            (
                "⚡ Energy",
                info["energy"]
            ),
            (
                "✂️ Grooming",
                info["grooming"]
            )
        ]


        for label, value in facts:

            st.markdown(
                f"""
                <div class="fact">

                    <div class="fact-label">
                        {html.escape(str(label))}
                    </div>

                    <div class="fact-value">
                        {html.escape(str(value))}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # PHOTO GALLERY
    # ========================================================

    if len(images) > 1:

        st.markdown(
            """
            <div class="section-heading">
                More photos
            </div>
            """,
            unsafe_allow_html=True
        )


        gallery = images[1:]


        columns = st.columns(4)


        for index, image in enumerate(
            gallery
        ):

            with columns[index % 4]:

                st.image(
                    image,
                    use_container_width=True
                )


    # ========================================================
    # VIDEOS
    # ========================================================

    st.markdown(
        """
        <div class="section-heading">
            Watch videos
        </div>
        """,
        unsafe_allow_html=True
    )


    youtube_query = (
        display_name
        .replace(" ", "+")
        + "+dog+breed"
    )


    youtube_url = (
        "https://www.youtube.com/results?"
        "search_query="
        + youtube_query
    )


    st.link_button(
        "▶ Find videos on YouTube",
        youtube_url
    )


    st.stop()


# ============================================================
# ============================================================
# HOME PAGE
# ============================================================
# ============================================================


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            Find your perfect dog.
        </div>

        <div class="hero-subtitle">
            Explore dog breeds from around the world,
            discover their personalities, and browse
            beautiful photos.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SEARCH + SORT
# ============================================================

search_column, sort_column = st.columns(
    [3, 1]
)


with search_column:

    search = st.text_input(
        "Search breeds",
        placeholder="🔎  Search for a breed...",
        label_visibility="collapsed"
    )


with sort_column:

    sort_option = st.selectbox(
        "Sort breeds",
        [
            "A → Z",
            "Z → A"
        ],
        label_visibility="collapsed"
    )


# ============================================================
# POPULAR BREEDS
# ============================================================

popular_names = [
    "Labrador Retriever",
    "Golden Retriever",
    "German Shepherd",
    "French Bulldog",
    "Poodle",
    "Beagle"
]


if not search:

    popular = [

        dog

        for dog in all_breeds

        if dog["display_name"]
        in popular_names

    ]


    if popular:

        st.markdown(
            """
            <div class="section-heading">
                Popular breeds
            </div>
            """,
            unsafe_allow_html=True
        )


        popular_columns = st.columns(
            len(popular)
        )


        for column, dog in zip(
            popular_columns,
            popular
        ):

            with column:

                # --------------------------------------------
                # IMAGE
                # --------------------------------------------

                try:

                    images = get_breed_images(
                        dog["breed"],
                        dog["sub_breed"],
                        amount=1
                    )

                except Exception:

                    images = []


                if images:

                    st.image(
                        images[0],
                        use_container_width=True
                    )


                # --------------------------------------------
                # NAME
                # --------------------------------------------

                st.markdown(
                    f"""
                    <div class="dog-card-title">
                        {html.escape(
                            dog["display_name"]
                        )}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # BUTTON
                # --------------------------------------------

                if st.button(
                    "Explore",
                    key=f"popular_{dog['id']}",
                    use_container_width=True
                ):

                    st.session_state.selected_breed = dog

                    st.rerun()


# ============================================================
# FILTER BREEDS
# ============================================================

filtered_breeds = all_breeds.copy()


if search:

    filtered_breeds = [

        dog

        for dog in filtered_breeds

        if search.lower()
        in dog["display_name"].lower()

    ]


# ============================================================
# SORT
# ============================================================

filtered_breeds = sorted(
    filtered_breeds,
    key=lambda dog:
    dog["display_name"].lower(),
    reverse=(
        sort_option == "Z → A"
    )
)


# ============================================================
# RESULTS HEADER
# ============================================================

if search:

    st.markdown(
        """
        <div class="section-heading">
            Search results
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        f"{len(filtered_breeds)} breed(s) found"
    )

else:

    st.markdown(
        """
        <div class="section-heading">
            Explore all breeds
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# NO RESULTS
# ============================================================

if not filtered_breeds:

    st.info(
        "No breeds found. Try another search."
    )


# ============================================================
# BREED GRID
# ============================================================

columns = st.columns(4)


for index, dog in enumerate(
    filtered_breeds
):

    with columns[index % 4]:

        breed = dog["breed"]

        sub_breed = dog["sub_breed"]

        display_name = dog[
            "display_name"
        ]


        # ----------------------------------------------------
        # BREED INFORMATION
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

        except Exception:

            images = []


        if images:

            st.image(
                images[0],
                use_container_width=True
            )

        else:

            st.markdown(
                """
                <div
                    style="
                        width:100%;
                        aspect-ratio:1/1;
                        background:#f5f5f5;
                        border-radius:16px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:40px;
                    "
                >
                    🐶
                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="dog-card-title">
                {html.escape(display_name)}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = str(
            info["description"]
        )


        if len(description) > 105:

            description = (
                description[:105]
                + "..."
            )


        st.markdown(
            f"""
            <div class="dog-card-description">
                {html.escape(description)}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # LIFE SPAN
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="dog-card-meta">
                ⏳ {html.escape(
                    str(info["life_span"])
                )}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # VIEW BUTTON
        # ----------------------------------------------------

        if st.button(
            "View breed",
            key=f"breed_{dog['id']}",
            use_container_width=True
        ):

            st.session_state.selected_breed = dog

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🐶 Dog Encyclopedia · Photos provided by Dog CEO API"
)
