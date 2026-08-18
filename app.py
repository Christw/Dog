import streamlit as st
import requests
import json


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dog Encyclopedia",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background-color: #f7f8fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* --------------------------------------------------------
       REMOVE DEFAULT PADDING
    -------------------------------------------------------- */

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }


    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e8e8e8;
    }


    /* --------------------------------------------------------
       HERO
    -------------------------------------------------------- */

    .hero {
        background: linear-gradient(
            135deg,
            #fff4e6 0%,
            #ffffff 55%,
            #f1f7ff 100%
        );

        border-radius: 28px;

        padding: 45px 50px;

        margin-bottom: 30px;

        border: 1px solid #eeeeee;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        line-height: 1.1;
        color: #1f2937;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 20px;
        color: #6b7280;
        max-width: 650px;
        line-height: 1.6;
    }


    /* --------------------------------------------------------
       STAT CARDS
    -------------------------------------------------------- */

    .stat-card {
        background: white;

        border-radius: 18px;

        padding: 22px;

        border: 1px solid #eeeeee;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.04);

        margin-bottom: 20px;
    }

    .stat-number {
        font-size: 30px;
        font-weight: 800;
        color: #1f2937;
    }

    .stat-label {
        font-size: 14px;
        color: #6b7280;
        margin-top: 4px;
    }


    /* --------------------------------------------------------
       BREED CARD
    -------------------------------------------------------- */

    .breed-card {
        background: white;

        border-radius: 20px;

        padding: 0;

        border: 1px solid #eeeeee;

        overflow: hidden;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.05);

        margin-bottom: 15px;

        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }

    .breed-card:hover {
        transform: translateY(-4px);

        box-shadow:
            0 10px 25px rgba(0,0,0,0.08);
    }

    .breed-name {
        font-size: 21px;
        font-weight: 750;
        color: #1f2937;
        padding: 15px 18px 5px 18px;
    }

    .breed-description {
        font-size: 14px;
        color: #6b7280;
        line-height: 1.5;
        padding: 0 18px 12px 18px;
    }

    .breed-meta {
        font-size: 13px;
        color: #6b7280;
        padding: 0 18px 12px 18px;
    }


    /* --------------------------------------------------------
       DETAIL PAGE
    -------------------------------------------------------- */

    .detail-header {
        background: white;

        border-radius: 25px;

        padding: 30px;

        border: 1px solid #eeeeee;

        margin-bottom: 25px;
    }

    .detail-title {
        font-size: 45px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 10px;
    }

    .detail-description {
        font-size: 17px;
        color: #5f6368;
        line-height: 1.8;
    }


    /* --------------------------------------------------------
       FACT CARD
    -------------------------------------------------------- */

    .fact-card {
        background: white;

        border-radius: 18px;

        padding: 20px;

        border: 1px solid #eeeeee;

        min-height: 110px;

        margin-bottom: 15px;
    }

    .fact-title {
        font-size: 13px;
        color: #8a8f98;
        margin-bottom: 7px;
    }

    .fact-value {
        font-size: 17px;
        font-weight: 700;
        color: #1f2937;
    }


    /* --------------------------------------------------------
       SECTION TITLE
    -------------------------------------------------------- */

    .section-title {
        font-size: 27px;
        font-weight: 800;
        color: #1f2937;
        margin-top: 30px;
        margin-bottom: 18px;
    }


    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        border-radius: 12px;

        border: 1px solid #e5e7eb;

        font-weight: 600;

        padding: 8px 16px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #ff8a3d;

        color: #ff8a3d;
    }


    /* --------------------------------------------------------
       SEARCH INPUT
    -------------------------------------------------------- */

    [data-testid="stTextInput"] input {
        border-radius: 14px;

        border: 1px solid #dddddd;

        padding: 12px 15px;

        font-size: 16px;
    }


    /* --------------------------------------------------------
       SELECT BOX
    -------------------------------------------------------- */

    [data-testid="stSelectbox"] > div {
        border-radius: 12px;
    }


    /* --------------------------------------------------------
       MOBILE
    -------------------------------------------------------- */

    @media (max-width: 768px) {

        .hero {
            padding: 30px 25px;
        }

        .hero-title {
            font-size: 36px;
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

    return response.json()["message"][:amount]


# ============================================================
# LOAD JSON
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
            f"{display_name} is a dog breed or "
            f"breed variety. More detailed "
            f"information will be added soon."
        )
    }


# ============================================================
# CREATE BREED LIST
# ============================================================

def create_breed_list(breeds):

    result = []

    for breed, sub_breeds in breeds.items():

        if not sub_breeds:

            result.append({
                "id": breed,
                "breed": breed,
                "sub_breed": None,
                "display_name": breed.title()
            })

        else:

            for sub_breed in sub_breeds:

                result.append({
                    "id": f"{breed}_{sub_breed}",
                    "breed": breed,
                    "sub_breed": sub_breed,
                    "display_name": (
                        f"{sub_breed.title()} "
                        f"{breed.title()}"
                    )
                })

    return result


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
        "Could not load the dog encyclopedia."
    )

    st.write(error)

    st.stop()


# ============================================================
# BREED LIST
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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 25px;
        ">
        🐶 Dog Encyclopedia
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Explore"
    )

    search = st.text_input(
        "🔎 Search",
        placeholder="Golden Retriever..."
    )

    sort_option = st.selectbox(
        "↕️ Sort",
        [
            "A → Z",
            "Z → A"
        ]
    )

    st.divider()

    st.caption(
        "📸 Photos powered by Dog CEO"
    )

    st.caption(
        "📖 Breed information from your encyclopedia database"
    )


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


    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    if st.button(
        "← Back to breeds"
    ):

        st.session_state.selected_breed = None

        st.rerun()


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="detail-header">

            <div class="detail-title">
                🐶 {display_name}
            </div>

            <div class="detail-description">
                {info["description"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MAIN IMAGE
    # --------------------------------------------------------

    try:

        images = get_breed_images(
            breed,
            sub_breed,
            amount=9
        )

    except Exception:

        images = []


    if images:

        st.image(
            images[0],
            use_container_width=True
        )


    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🐕 Quick facts</div>',
        unsafe_allow_html=True
    )


    fact_columns = st.columns(4)


    facts = [
        ("📏 Size", info["size"]),
        ("⏳ Life span", info["life_span"]),
        ("⚡ Energy", info["energy"]),
        ("✂️ Grooming", info["grooming"])
    ]


    for column, (title, value) in zip(
        fact_columns,
        facts
    ):

        with column:

            st.markdown(
                f"""
                <div class="fact-card">

                    <div class="fact-title">
                        {title}
                    </div>

                    <div class="fact-value">
                        {value}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📖 About this breed</div>',
        unsafe_allow_html=True
    )

    st.write(
        info["description"]
    )


    # --------------------------------------------------------
    # BREED FACTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Breed information</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            <div class="fact-card">

                <div class="fact-title">
                    🌍 Origin
                </div>

                <div class="fact-value">
                    {info["origin"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="fact-card">

                <div class="fact-title">
                    📏 Height
                </div>

                <div class="fact-value">
                    {info["height"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="fact-card">

                <div class="fact-title">
                    ⚖️ Weight
                </div>

                <div class="fact-value">
                    {info["weight"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="fact-card">

                <div class="fact-title">
                    ❤️ Temperament
                </div>

                <div class="fact-value">
                    {info["temperament"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="fact-card">

                <div class="fact-title">
                    ⚡ Energy
                </div>

                <div class="fact-value">
                    {info["energy"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="fact-card">

                <div class="fact-title">
                    ✂️ Grooming
                </div>

                <div class="fact-value">
                    {info["grooming"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # GALLERY
    # --------------------------------------------------------

    if len(images) > 1:

        st.markdown(
            '<div class="section-title">📸 Photo gallery</div>',
            unsafe_allow_html=True
        )

        gallery_columns = st.columns(4)

        for index, image in enumerate(
            images[1:]
        ):

            with gallery_columns[index % 4]:

                st.image(
                    image,
                    use_container_width=True
                )


    # --------------------------------------------------------
    # VIDEOS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🎥 Watch videos</div>',
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
        f"▶ Watch {display_name} videos",
        youtube_url
    )


    st.stop()



# ============================================================
# STATISTICS
# ============================================================

stat1, stat2, stat3 = st.columns(3)


with stat1:

    st.markdown(
        f"""
        <div class="stat-card">

            <div class="stat-number">
                {len(all_breeds)}
            </div>

            <div class="stat-label">
                🐕 Breed varieties
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with stat2:

    st.markdown(
        f"""
        <div class="stat-card">

            <div class="stat-number">
                {len(breed_information)}
            </div>

            <div class="stat-label">
                📖 Encyclopedia entries
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with stat3:

    st.markdown(
        """
        <div class="stat-card">

            <div class="stat-number">
                📸
            </div>

            <div class="stat-label">
                Dog CEO image library
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


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

if sort_option == "A → Z":

    filtered_breeds = sorted(
        filtered_breeds,
        key=lambda dog:
        dog["display_name"].lower()
    )

else:

    filtered_breeds = sorted(
        filtered_breeds,
        key=lambda dog:
        dog["display_name"].lower(),
        reverse=True
    )


# ============================================================
# RESULTS
# ============================================================

st.markdown(
    f"""
    <div class="section-title">
        🐕 Explore breeds
    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    f"{len(filtered_breeds)} breed(s) found"
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

        sub_breed = dog[
            "sub_breed"
        ]

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
        # NAME
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="breed-name">
                {display_name}
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


        if len(description) > 115:

            description = (
                description[:115]
                + "..."
            )


        st.markdown(
            f"""
            <div class="breed-description">
                {description}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # META
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="breed-meta">
                ⏳ {info["life_span"]}
                &nbsp; • &nbsp;
                ⚡ {info["energy"]}
            </div>
            """,
            unsafe_allow_html=True
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
