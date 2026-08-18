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
# SIMPLE CUSTOM CSS
# ============================================================
#
# Important:
# We deliberately avoid Streamlit's internal data-testid
# selectors. They can change between Streamlit versions.
#
# This CSS only targets stable elements/classes that we
# control ourselves.
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
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    html,
    body,
    [class*="css"] {
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        padding: 45px 0 35px 0;
    }

    .hero h1 {
        font-size: 52px;
        line-height: 1.05;
        letter-spacing: -2px;
        font-weight: 750;
        color: #222222;
        margin: 0;
    }

    .hero p {
        font-size: 19px;
        line-height: 1.5;
        color: #717171;
        margin-top: 14px;
        max-width: 650px;
    }


    /* ========================================================
       SEARCH AREA
       ======================================================== */

    .search-box {
        border: 1px solid #dddddd;
        border-radius: 18px;
        padding: 7px 10px;
        background: #ffffff;
        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 25px;
    }


    /* ========================================================
       FILTER PILLS
       ======================================================== */

    .filter-label {
        color: #717171;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 4px;
    }


    /* ========================================================
       SECTION
       ======================================================== */

    .section-heading {
        font-size: 25px;
        font-weight: 700;
        color: #222222;
        letter-spacing: -0.5px;
        margin-top: 25px;
        margin-bottom: 20px;
    }


    /* ========================================================
       BREED CARD
       ======================================================== */

    .dog-image {
        border-radius: 16px;
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        display: block;
    }

    .dog-card-title {
        font-size: 16px;
        font-weight: 650;
        color: #222222;
        margin-top: 11px;
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
    }


    /* ========================================================
       DETAIL PAGE
       ======================================================== */

    .detail-title {
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -1.5px;
        color: #222222;
        margin-top: 20px;
        margin-bottom: 6px;
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
        padding: 18px 0;
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
       GALLERY
       ======================================================== */

    .gallery-image {
        border-radius: 14px;
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
    }


    /* ========================================================
       SMALL TEXT
       ======================================================== */

    .muted {
        color: #717171;
        font-size: 14px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .hero h1 {
            font-size: 36px;
            letter-spacing: -1px;
        }

        .hero p {
            font-size: 17px;
        }

        .detail-title {
            font-size: 32px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API
# ============================================================

BREEDS_URL = (
    "https://dog.ceo/api/breeds/list/all"
)


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

    return response.json()["message"][:amount]


# ============================================================
# LOAD LOCAL BREED DATA
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

        if not sub_breeds:

            result.append(
                {
                    "id": breed,
                    "breed": breed,
                    "sub_breed": None,
                    "display_name": breed.title()
                }
            )

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
# GET BREED INFORMATION
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


all_breeds = create_breed_list(
    breeds
)


# ============================================================
# SESSION STATE
# ============================================================

if "selected_breed" not in st.session_state:

    st.session_state.selected_breed = None


# ============================================================
# DETAIL PAGE
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
        "← Back to breeds"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        f"""
        <div class="detail-title">
            {html.escape(display_name)}
        </div>

        <div class="detail-subtitle">
            Dog breed encyclopedia
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # LOAD PHOTOS
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
    # MAIN PHOTO
    # ========================================================

    if images:

        st.image(
            images[0],
            use_container_width=True
        )


    # ========================================================
    # ABOUT
    # ========================================================

    left, right = st.columns(
        [2, 1],
        gap="large"
    )


    with left:

        st.markdown(
            '<div class="section-heading">About this breed</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="detail-description">
                {html.escape(info["description"])}
            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        st.markdown(
            '<div class="section-heading">Quick facts</div>',
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
                        {html.escape(label)}
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
            '<div class="section-heading">More photos</div>',
            unsafe_allow_html=True
        )


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
    # VIDEOS
    # ========================================================

    st.markdown(
        '<div class="section-heading">Watch videos</div>',
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
# HOME PAGE
# ============================================================

st.markdown(
    """
    <div class="hero">

        <h1>
            Find your perfect dog.
        </h1>

        <p>
            Explore dog breeds from around the world,
            discover their personalities, and browse
            beautiful photos.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SEARCH
# ============================================================

search_col, sort_col = st.columns(
    [3, 1]
)


with search_col:

    search = st.text_input(
        "Search",
        placeholder=(
            "🔎  Search breeds..."
        ),
        label_visibility="collapsed"
    )


with sort_col:

    sort_option = st.selectbox(
        "Sort",
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
            '<div class="section-heading">Popular breeds</div>',
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


                st.markdown(
                    f"""
                    <div class="dog-card-title">
                        {html.escape(dog["display_name"])}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.button(
                    "Explore",
                    key=f"popular_{dog['id']}",
                    use_container_width=True
                ):

                    st.session_state.selected_breed = dog

                    st.rerun()


# ============================================================
# FILTER
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
# RESULTS
# ============================================================

if search:

    st.markdown(
        f"""
        <div class="section-heading">
            Search results
        </div>

        <div class="muted">
            {len(filtered_breeds)}
            breed(s) found
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-heading">Explore all breeds</div>',
        unsafe_allow_html=True
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

        description = (
            info["description"]
        )


        if len(description) > 100:

            description = (
                description[:100]
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
        # META
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="dog-card-meta">
                ⏳ {html.escape(str(info["life_span"]))}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        if st.button(
            "View breed",
            key=f"breed_{dog['id']}",
            use_container_width=True
        ):

            st.session_state.selected_breed = dog

            st.rerun()
