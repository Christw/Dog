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
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #ffffff;
        --surface: #ffffff;
        --surface-soft: #f7f7f7;
        --text: #1f1f1f;
        --muted: #717171;
        --border: #e7e7e7;
        --accent: #ff385c;
        --accent-dark: #e31c5f;
        --shadow: 0 8px 30px rgba(0,0,0,0.06);
        --radius-lg: 24px;
        --radius-md: 18px;
        --radius-sm: 12px;
    }

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1360px;
        padding-top: 0.8rem;
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        display: none;
    }

    hr {
        border-color: var(--border) !important;
    }

    /* ========================================================
       NAVIGATION
       ======================================================== */

    .top-nav {
        height: 68px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--border);
        margin-bottom: 8px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 18px;
        font-weight: 760;
        letter-spacing: -0.35px;
        color: var(--text);
    }

    .brand-mark {
        width: 38px;
        height: 38px;
        border-radius: 13px;
        background: var(--surface-soft);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }

    .nav-meta {
        font-size: 13px;
        color: var(--muted);
        font-weight: 500;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        padding: 72px 0 42px;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 7px 12px;
        background: var(--surface-soft);
        border-radius: 999px;
        font-size: 13px;
        font-weight: 650;
        color: #4f4f4f;
        margin-bottom: 18px;
    }

    .hero-title {
        margin: 0;
        max-width: 820px;
        font-size: clamp(44px, 5.5vw, 74px);
        line-height: 0.98;
        letter-spacing: -4px;
        font-weight: 820;
        color: var(--text);
    }

    .hero-title .accent {
        color: var(--accent);
    }

    .hero-subtitle {
        margin-top: 22px;
        max-width: 680px;
        font-size: 18px;
        line-height: 1.65;
        color: var(--muted);
    }

    /* ========================================================
       SEARCH / CONTROLS
       ======================================================== */

    .controls-label {
        margin-top: 4px;
        margin-bottom: 10px;
        font-size: 12px;
        font-weight: 700;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    div[data-testid="stTextInput"] > div > div,
    div[data-testid="stSelectbox"] > div > div {
        min-height: 50px;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        background: #fff !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInput"] input {
        font-size: 15px !important;
        color: var(--text) !important;
    }

    div[data-testid="stTextInput"] > div > div:focus-within,
    div[data-testid="stSelectbox"] > div > div:focus-within {
        border-color: #b7b7b7 !important;
        box-shadow: 0 0 0 3px rgba(0,0,0,0.03) !important;
    }

    /* ========================================================
       SECTIONS
       ======================================================== */

    .section-wrap {
        margin-top: 44px;
        margin-bottom: 18px;
    }

    .section-title {
        margin: 0;
        font-size: 26px;
        font-weight: 780;
        letter-spacing: -0.8px;
        color: var(--text);
    }

    .section-subtitle {
        margin-top: 6px;
        font-size: 14px;
        color: var(--muted);
    }

    /* ========================================================
       CARDS
       ======================================================== */

    /* Make ALL dog images identical in display size */
    [data-testid="stImage"] {
        width: 100%;
    }
    
    [data-testid="stImage"] img {
        width: 100% !important;
        height: 260px !important;
        object-fit: cover !important;
        border-radius: 18px !important;
    }

    .dog-card-title {
        margin-top: 11px;
        font-size: 17px;
        line-height: 1.3;
        font-weight: 730;
        letter-spacing: -0.2px;
        color: var(--text);
    }

    .dog-card-description {
        margin-top: 5px;
        min-height: 42px;
        font-size: 13.5px;
        line-height: 1.5;
        color: var(--muted);
    }

    .dog-card-meta {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-top: 8px;
        padding: 5px 9px;
        border-radius: 999px;
        background: var(--surface-soft);
        color: #5d5d5d;
        font-size: 12px;
        font-weight: 650;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button,
    .stLinkButton > a {
        min-height: 44px;
        border-radius: 13px !important;
        border: 1px solid var(--border) !important;
        background: #fff !important;
        color: var(--text) !important;
        font-weight: 680 !important;
        box-shadow: none !important;
        transition: all 0.18s ease !important;
    }

    .stButton > button:hover,
    .stLinkButton > a:hover {
        border-color: var(--text) !important;
        background: var(--text) !important;
        color: #fff !important;
        transform: translateY(-1px);
    }

    .stButton > button:active,
    .stLinkButton > a:active {
        transform: scale(0.99);
    }

    /* ========================================================
       DETAIL PAGE
       ======================================================== */

    .detail-header {
        padding: 30px 0 12px;
    }

    .detail-title {
        margin: 0;
        font-size: clamp(40px, 5vw, 62px);
        line-height: 1;
        font-weight: 820;
        letter-spacing: -3px;
        color: var(--text);
    }

    .detail-subtitle {
        margin-top: 9px;
        font-size: 14px;
        color: var(--muted);
    }

    .detail-description {
        font-size: 17px;
        line-height: 1.8;
        color: #484848;
        max-width: 760px;
    }

    .facts-card {
        border: 1px solid var(--border);
        border-radius: 20px;
        background: #fff;
        padding: 4px 20px;
        box-shadow: var(--shadow);
    }

    .fact {
        padding: 15px 0;
        border-bottom: 1px solid var(--border);
    }

    .fact:last-child {
        border-bottom: 0;
    }

    .fact-label {
        font-size: 11px;
        font-weight: 760;
        color: #8a8a8a;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        margin-bottom: 4px;
    }

    .fact-value {
        font-size: 15px;
        line-height: 1.4;
        font-weight: 650;
        color: var(--text);
    }

    .video-panel {
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        background: var(--surface-soft);
    }

    /* ========================================================
       EMPTY STATE / FOOTER
       ======================================================== */

    .empty-state {
        padding: 60px 24px;
        border-radius: 20px;
        border: 1px dashed #d6d6d6;
        background: #fafafa;
        text-align: center;
    }

    .empty-title {
        margin-top: 10px;
        font-size: 18px;
        font-weight: 740;
        color: var(--text);
    }

    .empty-copy {
        margin-top: 5px;
        font-size: 14px;
        color: var(--muted);
    }

    .site-footer {
        margin-top: 72px;
        padding-top: 24px;
        border-top: 1px solid var(--border);
        color: #8a8a8a;
        text-align: center;
        font-size: 13px;
    }

    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {
        .hero {
            padding-top: 52px;
        }

        .hero-title {
            letter-spacing: -2.5px;
        }

        .detail-title {
            letter-spacing: -2px;
        }
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .top-nav {
            height: 60px;
        }

        .nav-meta {
            display: none;
        }

        .hero {
            padding: 40px 0 30px;
        }

        .hero-subtitle {
            font-size: 16px;
        }

        .section-title {
            font-size: 23px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API
# ============================================================

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"


@st.cache_data(ttl=3600)
def get_breeds():
    response = requests.get(BREEDS_URL, timeout=20)
    response.raise_for_status()
    return response.json()["message"]


@st.cache_data(ttl=3600)
def get_breed_images(breed, sub_breed=None, amount=8):
    if sub_breed:
        url = f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images"
    else:
        url = f"https://dog.ceo/api/breed/{breed}/images"

    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()["message"][:amount]


@st.cache_data
def load_breed_information():
    with open("dogs.json", "r", encoding="utf-8") as file:
        return json.load(file)


def create_breed_list(breeds):
    result = []

    for breed, sub_breeds in breeds.items():
        if not sub_breeds:
            result.append(
                {
                    "id": breed,
                    "breed": breed,
                    "sub_breed": None,
                    "display_name": breed.title(),
                }
            )
        else:
            for sub_breed in sub_breeds:
                result.append(
                    {
                        "id": f"{breed}_{sub_breed}",
                        "breed": breed,
                        "sub_breed": sub_breed,
                        "display_name": f"{sub_breed.title()} {breed.title()}",
                    }
                )

    return result


def get_breed_information(breed, sub_breed=None):
    if sub_breed:
        search_name = f"{sub_breed} {breed}".lower()
    else:
        search_name = breed.lower()

    for dog in breed_information:
        if dog["breed"].lower() == search_name:
            return dog

    display_name = (
        f"{sub_breed.title()} {breed.title()}"
        if sub_breed
        else breed.title()
    )

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
            f"{display_name} is a dog breed or breed variety. "
            "Detailed information about this breed will be added soon."
        ),
    }


# ============================================================
# LOAD DATA
# ============================================================

try:
    breeds = get_breeds()
    breed_information = load_breed_information()

except Exception as error:
    st.error("Unable to load the dog encyclopedia.")
    st.write(error)
    st.stop()


all_breeds = create_breed_list(breeds)

if "selected_breed" not in st.session_state:
    st.session_state.selected_breed = None


# ============================================================
# DETAIL PAGE
# ============================================================

if st.session_state.selected_breed:
    selected = st.session_state.selected_breed

    breed = selected["breed"]
    sub_breed = selected["sub_breed"]
    display_name = selected["display_name"]
    info = get_breed_information(breed, sub_breed)

    if st.button("← Back to breeds"):
        st.session_state.selected_breed = None
        st.rerun()

    st.markdown(
        f"""
        <div class="detail-header">
            <div class="detail-title">{html.escape(display_name)}</div>
            <div class="detail-subtitle">Dog Encyclopedia · Breed profile</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        images = get_breed_images(breed, sub_breed, amount=9)
    except Exception:
        images = []

    if images:
        st.image(images[0], use_container_width=True)
    else:
        st.info("No photos available.")

    left, right = st.columns([1.7, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="section-wrap">
                <div class="section-title">About this breed</div>
                <div class="section-subtitle">
                    Personality, characteristics and background.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="detail-description">
                {html.escape(str(info["description"]))}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="section-wrap">
                <div class="section-title">Quick facts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        facts = [
            ("🌍 Origin", info["origin"]),
            ("📏 Height", info["height"]),
            ("⚖️ Weight", info["weight"]),
            ("⏳ Life span", info["life_span"]),
            ("❤️ Temperament", info["temperament"]),
            ("⚡ Energy", info["energy"]),
            ("✂️ Grooming", info["grooming"]),
        ]

        facts_html = '<div class="facts-card">'

        for label, value in facts:
            facts_html += f"""
            <div class="fact">
                <div class="fact-label">{html.escape(str(label))}</div>
                <div class="fact-value">{html.escape(str(value))}</div>
            </div>
            """

        facts_html += "</div>"

        st.markdown(facts_html, unsafe_allow_html=True)

    if len(images) > 1:
        st.markdown(
            """
            <div class="section-wrap">
                <div class="section-title">More photos</div>
                <div class="section-subtitle">
                    Explore more photos of this breed.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        gallery_columns = st.columns(4)

        for index, image in enumerate(images[1:]):
            with gallery_columns[index % 4]:
                st.image(image, use_container_width=True)

    st.markdown(
        """
        <div class="section-wrap">
            <div class="section-title">Watch & learn</div>
            <div class="section-subtitle">
                Discover breed videos on YouTube.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    youtube_query = display_name.replace(" ", "+") + "+dog+breed"
    youtube_url = (
        "https://www.youtube.com/results?search_query="
        + youtube_query
    )

    st.markdown('<div class="video-panel">', unsafe_allow_html=True)

    st.link_button(
        "▶ Explore videos on YouTube",
        youtube_url,
        use_container_width=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="site-footer">
            🐶 Dog Encyclopedia · Photos provided by Dog CEO API
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# HOME PAGE
# ============================================================

st.markdown(
    """
    <div class="top-nav">
        <div class="brand">
            <div class="brand-mark">🐶</div>
            Dog Encyclopedia
        </div>
        <div class="nav-meta">Discover · Explore · Learn</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">🐾 Explore the world of dogs</div>

        <h1 class="hero-title">
            Find a dog you'll <span class="accent">love.</span>
        </h1>

        <div class="hero-subtitle">
            Explore dog breeds from around the world, discover their
            personalities and characteristics, and browse beautiful photos.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

search_column, sort_column = st.columns([3.2, 1])

with search_column:
    search = st.text_input(
        "Search breeds",
        placeholder="🔎 Search by breed name...",
        label_visibility="collapsed",
    )

with sort_column:
    sort_option = st.selectbox(
        "Sort breeds",
        ["A → Z", "Z → A"],
        label_visibility="collapsed",
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
    "Beagle",
]

if not search:
    popular = [
        dog
        for dog in all_breeds
        if dog["display_name"] in popular_names
    ]

    if popular:
        st.markdown(
            """
            <div class="section-wrap">
                <div class="section-title">Popular breeds</div>
                <div class="section-subtitle">
                    Start with some of the world's most loved dogs.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        popular_columns = st.columns(len(popular))

        for column, dog in zip(popular_columns, popular):
            with column:
                try:
                    images = get_breed_images(
                        dog["breed"],
                        dog["sub_breed"],
                        amount=1,
                    )
                except Exception:
                    images = []

                if images:
                    st.image(images[0], use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div style="
                            width:100%;
                            aspect-ratio:1/1;
                            background:#f7f7f7;
                            border-radius:18px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-size:40px;
                        ">🐶</div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <div class="dog-card-title">
                        {html.escape(dog["display_name"])}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Explore breed",
                    key=f"popular_{dog['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_breed = dog
                    st.rerun()


# ============================================================
# FILTER / SORT
# ============================================================

filtered_breeds = all_breeds.copy()

if search:
    filtered_breeds = [
        dog
        for dog in filtered_breeds
        if search.lower() in dog["display_name"].lower()
    ]

filtered_breeds = sorted(
    filtered_breeds,
    key=lambda dog: dog["display_name"].lower(),
    reverse=(sort_option == "Z → A"),
)


# ============================================================
# RESULT HEADER
# ============================================================

if search:
    st.markdown(
        f"""
        <div class="section-wrap">
            <div class="section-title">Search results</div>
            <div class="section-subtitle">
                {len(filtered_breeds)} breed(s) found
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="section-wrap">
            <div class="section-title">Explore all breeds</div>
            <div class="section-subtitle">
                Browse the complete breed library.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# NO RESULTS
# ============================================================

if not filtered_breeds:
    st.markdown(
        """
        <div class="empty-state">
            <div style="font-size:42px;">🐕</div>
            <div class="empty-title">No breeds found</div>
            <div class="empty-copy">
                Try another search term.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# BREED GRID
# ============================================================

columns = st.columns(4)

for index, dog in enumerate(filtered_breeds):
    with columns[index % 4]:
        breed = dog["breed"]
        sub_breed = dog["sub_breed"]
        display_name = dog["display_name"]

        info = get_breed_information(
            breed,
            sub_breed,
        )

        try:
            images = get_breed_images(
                breed,
                sub_breed,
                amount=1,
            )
        except Exception:
            images = []

        if images:
            st.image(
                images[0],
                use_container_width=True,
            )
        else:
            st.markdown(
                """
                <div style="
                    width:100%;
                    aspect-ratio:1/1;
                    background:#f7f7f7;
                    border-radius:18px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:40px;
                ">🐶</div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="dog-card-title">
                {html.escape(display_name)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        description = str(info["description"])

        if len(description) > 105:
            description = description[:105] + "..."

        st.markdown(
            f"""
            <div class="dog-card-description">
                {html.escape(description)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="dog-card-meta">
                ⏳ {html.escape(str(info["life_span"]))}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "View breed",
            key=f"breed_{dog['id']}",
            use_container_width=True,
        ):
            st.session_state.selected_breed = dog
            st.rerun()


st.markdown(
    """
    <div class="site-footer">
        🐶 Dog Encyclopedia · Photos provided by Dog CEO API
    </div>
    """,
    unsafe_allow_html=True,
)
