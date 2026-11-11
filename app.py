import os
import json
import html
import streamlit as st
import streamlit.components.v1 as components
import requests
from PIL import Image, ImageOps
import base64
from yt_dlp import YoutubeDL
from streamlit_searchbox import st_searchbox
from breed_data import breed_information

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Dog Encyclopedia",
    page_icon="🐕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --text: #222222;
        --muted: #717171;
        --border: #e8e8e8;
        --soft: #f7f7f7;
        --accent: #ff385c;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 12%, rgba(255, 224, 205, .72), transparent 34%),
            radial-gradient(ellipse at 88% 18%, rgba(222, 211, 255, .76), transparent 36%),
            linear-gradient(125deg, #fff9ef 0%, #fff0ef 48%, #f3efff 100%);
    }
    .block-container { max-width: 1320px; padding-top: 1rem; padding-bottom: 4rem; }
    /* Homepage hero: one cohesive, responsive section */
    div[data-testid="stHorizontalBlock"]:has(iframe[title="streamlit.components.v1.html"]) {
        align-items: center;
        gap: clamp(1.25rem, 3vw, 3rem);
        padding: clamp(1.25rem, 3.5vw, 3.25rem);
        border: 1px solid rgba(255,255,255,.78);
        border-radius: 32px;
        background: linear-gradient(115deg, rgba(255,250,241,.94), rgba(255,239,241,.91) 52%, rgba(241,236,255,.94));
        box-shadow: 0 24px 70px rgba(91, 61, 120, .10);
        overflow: hidden;
    }
    div[data-testid="stHorizontalBlock"]:has(iframe[title="streamlit.components.v1.html"]) > div {
        min-width: 0;
    }
    div[data-testid="stHorizontalBlock"]:has(iframe[title="streamlit.components.v1.html"]) iframe {
        border-radius: 24px;
        overflow: hidden;
    }
    @media (max-width: 760px) {
        div[data-testid="stHorizontalBlock"]:has(iframe[title="streamlit.components.v1.html"]) {
            flex-direction: column !important;
            padding: 1.15rem;
            gap: 1rem;
            border-radius: 24px;
        }
        div[data-testid="stHorizontalBlock"]:has(iframe[title="streamlit.components.v1.html"]) > div {
            width: 100% !important;
            flex: 1 1 auto !important;
        }
        div[data-testid="stHorizontalBlock"]:has(iframe[title="streamlit.components.v1.html"]) iframe {
            width: 100% !important;
        }
    }
    #MainMenu, footer, [data-testid="stHeader"] { display: none !important; }

    .top-nav {
        min-height: 64px; display: flex; justify-content: space-between;
        align-items: center; border-bottom: 1px solid var(--border); margin-bottom: 28px;
    }
    .brand { font-size: 19px; font-weight: 750; color: var(--text); }
    .hero { padding: 28px 10px 36px 4px; }
    .hero-title {
        margin: 0; font-size: clamp(42px, 5.4vw, 76px); line-height: .99;
        letter-spacing: -3.2px; font-weight: 850; color: #292333;
        max-width: 610px;
    }
    .hero-title span {
        background: linear-gradient(100deg, #e17c75, #9a78d5);
        -webkit-background-clip: text; background-clip: text; color: transparent;
    }
    .hero-copy {
        max-width: 440px; margin-top: 20px; color: #6e6574;
        font-size: clamp(15px, 1.4vw, 18px); line-height: 1.7;
    }
    @media (max-width: 760px) {
        .hero { padding: 10px 4px 2px; }
        .hero-title { font-size: clamp(42px, 11vw, 60px); letter-spacing: -2px; }
    }
    .section-title {
        margin-top: 36px; margin-bottom: 6px; font-size: 25px;
        font-weight: 750; letter-spacing: -0.5px; color: var(--text);
    }
    .section-subtitle { margin-bottom: 18px; font-size: 14px; color: var(--muted); }
    .dog-card-title {
        height: 46px; margin-top: 10px; font-size: 17px; line-height: 23px;
        font-weight: 700; color: var(--text); overflow: hidden;
    }
    .dog-card-description {
        height: 66px; font-size: 13.5px; line-height: 22px; color: var(--muted); overflow: hidden;
    }
    .dog-card-meta {
        height: 30px; display: flex; align-items: center; margin-top: 4px;
        font-size: 12px; font-weight: 600; color: #5f5f5f;
    }
    .detail-title {
        margin-top: 20px; font-size: clamp(38px, 5vw, 56px); line-height: 1;
        font-weight: 800; letter-spacing: -2px; color: var(--text);
    }
    .detail-subtitle { margin-top: 8px; margin-bottom: 24px; color: var(--muted); font-size: 14px; }
    .detail-description { font-size: 17px; line-height: 1.75; color: #454545; }
    .facts-card { border: 1px solid var(--border); border-radius: 18px; padding: 6px 18px; background: white; }
    .fact { padding: 13px 0; border-bottom: 1px solid var(--border); }
    .fact:last-child { border-bottom: 0; }
    .fact-label { font-size: 11px; font-weight: 700; color: #8a8a8a; text-transform: uppercase; letter-spacing: 0.5px; }
    .fact-value { margin-top: 3px; font-size: 15px; font-weight: 600; color: var(--text); }
    .footer-note { margin-top: 60px; padding-top: 20px; border-top: 1px solid var(--border); text-align: center; color: #8a8a8a; font-size: 13px; }
    .stButton > button { border-radius: 12px !important; min-height: 42px; font-weight: 650; }
    div[data-testid="stTextInput"] > div > div,
    div[data-testid="stSelectbox"] > div > div { border-radius: 12px !important; }
    .filter-label {
    font-size: 14px;
    margin-bottom: 3px;
    color: #31333f;
    }
    .gallery-image {
    width: 100%;
    aspect-ratio: 4 / 3;
    overflow: hidden;
    border-radius: 12px;
    margin-bottom: 16px;
    }

    .gallery-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    }
    /* ============================================================
   COMPACT BREED DETAIL PAGE
   ============================================================ */

.compact-title {
    margin-top: 0 !important;
    margin-bottom: 10px !important;
}

.compact-facts-title {
    margin-top: 22px !important;
    margin-bottom: 10px !important;
}


/* Description */
.detail-description {
    font-size: 16px;
    line-height: 1.65;
    color: #454545;
}


/* Facts in compact grid */
.facts-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}


/* Individual fact */
.fact-compact {
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 11px 13px;
    background: white;
}


/* Remove old vertical fact spacing */
.fact-compact .fact-label {
    font-size: 10px;
    margin-bottom: 3px;
}

.fact-compact .fact-value {
    font-size: 14px;
    line-height: 1.35;
}

.compact-facts-title {
    margin-top: 22px !important;
    margin-bottom: 10px !important;
}

.facts-compact-list {
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    background: white;
}

.fact-row {
    display: grid;
    grid-template-columns: 100px minmax(0, 1fr);
    gap: 12px;
    align-items: start;

    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
}

.fact-row:last-child {
    border-bottom: none;
}

.fact-row .fact-label {
    margin: 0;
    font-size: 11px;
    line-height: 1.4;
    font-weight: 700;
    color: #8a8a8a;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.fact-row .fact-value {
    margin: 0;
    min-width: 0;

    font-size: 14px;
    line-height: 1.4;
    font-weight: 600;
    color: var(--text);

    overflow-wrap: break-word;
}
.breed-image-link {
    display: block;
    text-decoration: none;
}

.breed-card-image {
    width: 100%;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    border-radius: 12px;
    display: block;
    cursor: pointer;
    transition: transform 0.18s ease, opacity 0.18s ease;
}

.breed-card-image:hover {
    transform: scale(1.015);
    opacity: 0.92;
}

.breed-image-placeholder {
    width: 100%;
    aspect-ratio: 4 / 3;
    background: #f7f7f7;
    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 38px;
    cursor: pointer;
}
    .video-title {
    font-size: 14px;
    font-weight: 600;
    line-height: 1.4;
    color: var(--text);
    margin-top: -4px;
    margin-bottom: 18px;
}
    .quiz-hero {
    max-width: 760px;
    padding: 32px 0 28px 0;
}

.quiz-hero h1 {
    margin: 0;
    font-size: clamp(38px, 5vw, 58px);
    letter-spacing: -2px;
    line-height: 1;
    font-weight: 800;
}

.quiz-hero p {
    margin-top: 14px;
    font-size: 17px;
    line-height: 1.6;
    color: var(--muted);
}

.quiz-result-name {
    margin-top: 10px;
    font-size: 18px;
    font-weight: 750;
}

.quiz-match {
    margin-top: 4px;
    margin-bottom: 8px;
    color: #ff385c;
    font-size: 14px;
    font-weight: 700;
}
/* ============================================================
   DOG PERSONALITY QUIZ
   ============================================================ */

.quiz-progress-text {
    margin-top: 8px;
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
}

.quiz-question {
    max-width: 780px;
    padding: 60px 0 30px 0;
}

.quiz-question h1 {
    margin: 0;
    font-size: clamp(36px, 4vw, 54px);
    line-height: 1.05;
    letter-spacing: -1.8px;
    color: var(--text);
}

.quiz-question p {
    margin-top: 14px;
    color: var(--muted);
    font-size: 16px;
    line-height: 1.6;
}

.quiz-header {
    max-width: 760px;
    padding: 34px 0 42px 0;
}

.quiz-header h1 {
    margin: 6px 0 0 0;
    font-size: clamp(40px, 5vw, 58px);
    letter-spacing: -2px;
    line-height: 1;
}

.quiz-header p {
    margin-top: 14px;
    font-size: 16px;
    color: var(--muted);
}

.quiz-kicker,
.match-rank {
    color: #ff385c;
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 800;
}

.match-name {
    margin-top: 5px;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.6px;
}

.match-score {
    margin-top: 5px;
    color: #ff385c;
    font-size: 15px;
    font-weight: 700;
}

.match-temperament {
    margin-top: 12px;
    margin-bottom: 18px;
    color: var(--muted);
    line-height: 1.5;
}

.match-divider {
    border-bottom: 1px solid var(--border);
    margin: 26px 0;
}
    button[kind="tertiary"] {
    height: 40px !important;
    min-height: 40px !important;

    padding-top: 0 !important;
    padding-bottom: 0 !important;

    border: none !important;
    box-shadow: none !important;
    background: transparent !important;

    display: flex !important;
    align-items: center !important;

    font-size: 16px !important;
    font-weight: 650 !important;

    transition: transform 0.12s ease !important;
}

button[kind="tertiary"]:hover {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    transform: scale(1.01) !important;
}

div[data-testid="stHorizontalBlock"] > div:last-child button[kind="tertiary"] {
    justify-content: flex-end !important;
}

/* ============================================================
   DOG TRAINING
   ============================================================ */

.training-hero {
    max-width: 720px;
    padding: 42px 0 38px 0;
}

.training-hero h1 {
    margin: 7px 0 0 0;
    font-size: clamp(42px, 5vw, 60px);
    line-height: 1;
    letter-spacing: -2px;
    font-weight: 800;
}

.training-hero p {
    margin-top: 15px;
    max-width: 620px;
    color: var(--muted);
    font-size: 17px;
    line-height: 1.6;
}

.training-small-title {
    margin: 10px 0 16px 0;
    color: var(--muted);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
}


/* PRINCIPLES */

.training-principle {
    min-height: 130px;
    padding: 18px 4px;
}

.training-principle-icon {
    font-size: 27px;
    margin-bottom: 12px;
}

.training-principle-title {
    font-size: 16px;
    font-weight: 750;
}

.training-principle-text {
    margin-top: 5px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.5;
}


/* DIVIDER */

.training-divider {
    border-bottom: 1px solid var(--border);
    margin: 28px 0 34px 0;
}


/* TOPIC */

.training-topic-header {
    max-width: 760px;
    padding: 38px 0 36px 0;
}

.training-topic-icon {
    font-size: 34px;
    margin-bottom: 12px;
}

.training-topic-header h2 {
    margin: 0;
    font-size: 32px;
    letter-spacing: -0.8px;
}

.training-topic-header p {
    margin-top: 12px;
    max-width: 680px;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.7;
}


/* STEPS */

.training-step {
    display: flex;
    gap: 20px;
    max-width: 780px;
    padding: 19px 0;
    border-bottom: 1px solid var(--border);
}

.training-step-number {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 34px;
    height: 34px;
    min-width: 34px;

    border-radius: 50%;

    background: var(--text);
    color: white;

    font-size: 13px;
    font-weight: 800;
}

.training-step-content {
    padding-top: 4px;
}

.training-step-title {
    font-size: 16px;
    font-weight: 750;
}

.training-step-text {
    margin-top: 5px;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
}


/* TIP */

.training-tip {
    display: flex;
    gap: 15px;

    max-width: 780px;

    margin-top: 26px;
    padding: 20px 22px;

    border-radius: 14px;
    background: var(--surface);
}

.training-tip-icon {
    font-size: 22px;
}

.training-tip-title {
    font-size: 14px;
    font-weight: 750;
}

.training-tip-text {
    margin-top: 4px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
}


/* VIDEOS */

.training-video-heading {
    margin-bottom: 20px;
}

.training-video-heading h2 {
    margin: 0;
    font-size: 28px;
    letter-spacing: -0.6px;
}

div[data-testid="stPopover"] button {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    font-size: 24px !important;
}

div[data-testid="stPopover"] button:hover {
    background: #f7f7f7 !important;
    transform: scale(1.03);
}

/* ============================================================
   NAV MENU
   ============================================================ */

/* menu trigger */
div[data-testid="stPopover"] > button {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;

    min-height: 40px !important;
    padding: 0 8px !important;

    font-size: 23px !important;
    border-radius: 10px !important;
}

div[data-testid="stPopover"] > button:hover {
    background: #f7f7f7 !important;
}


/* menu heading */
.menu-title {
    padding: 4px 4px 10px 4px;

    color: var(--muted);
    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1px;
    text-transform: uppercase;
}


/* buttons inside popover */
div[data-testid="stPopoverBody"]
div[data-testid="stButton"] button {

    width: 100% !important;

    min-height: 46px !important;

    padding: 0 12px !important;

    border: none !important;
    box-shadow: none !important;
    background: transparent !important;

    border-radius: 10px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;

    text-align: left !important;

    font-size: 14px !important;
    font-weight: 600 !important;

    transition:
        background 0.12s ease,
        transform 0.12s ease !important;
}


/* make button text align left */
div[data-testid="stPopoverBody"]
div[data-testid="stButton"] button p {

    width: 100% !important;
    text-align: left !important;
    margin: 0 !important;
}


/* hover */
div[data-testid="stPopoverBody"]
div[data-testid="stButton"] button:hover {

    background: #f7f7f7 !important;

    transform: translateX(2px) !important;
}


/* MENU TRIGGER */

div[data-testid="stPopover"] > button {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    font-size: 24px !important;
    padding: 0 !important;
}


/* HIDE ANY ICON/CHEVRON INSIDE THE TRIGGER */

div[data-testid="stPopover"] > button svg,
div[data-testid="stPopover"] > button span[data-testid],
div[data-testid="stPopover"] > button [class*="icon"],
div[data-testid="stPopover"] > button [class*="Icon"] {
    display: none !important;
}


/* keep the actual ☰ text */
div[data-testid="stPopover"] > button p {
    display: block !important;
    margin: 0 !important;
}


/* MENU LIST ITEMS */

div[data-testid="stPopoverBody"]
div[data-testid="stButton"] button {
    width: 100% !important;

    border: none !important;
    box-shadow: none !important;
    background: transparent !important;

    justify-content: flex-start !important;
    text-align: left !important;

    padding: 10px 12px !important;
    border-radius: 8px !important;

    font-size: 14px !important;
    font-weight: 600 !important;
}


div[data-testid="stPopoverBody"]
div[data-testid="stButton"] button p {
    width: 100% !important;
    text-align: left !important;
}


/* HOVER */

div[data-testid="stPopoverBody"]
div[data-testid="stButton"] button:hover {
    background: #f7f7f7 !important;
    transform: none !important;
}

/* Make ☰ larger */
div[data-testid="stPopover"] button p {
    font-size: 25px !important;
    line-height: 1 !important;
}

div[data-testid="stPopoverBody"] div[data-testid="stButton"] button {
    width: 100% !important;
    min-height: 38px !important;
    padding: 7px 10px !important;

    justify-content: flex-start !important;
    text-align: left !important;
}

div[data-testid="stPopoverBody"] div[data-testid="stButton"] button p {
    width: 100% !important;
    text-align: left !important;
    white-space: nowrap !important;
    font-size: 14px !important;
}

/* ============================================================
   MOBILE NAVIGATION
   Keep logo + hamburger on same row
   ============================================================ */

.st-key-main_navigation div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    width: 100% !important;
}

/* Logo side */
.st-key-main_navigation div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:first-child {
    flex: 1 1 auto !important;
    width: auto !important;
    min-width: 0 !important;
}

/* Menu side */
.st-key-main_navigation div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:last-child {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: fit-content !important;
}

/* Remove unnecessary vertical spacing */
.st-key-main_navigation div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

@media (max-width: 768px) {

    .st-key-main_navigation {
        width: 100%;
    }

    .st-key-main_navigation button[kind="tertiary"] {
        white-space: nowrap !important;
    }

    .st-key-main_navigation div[data-testid="stPopover"] {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
    }

    .st-key-main_navigation div[data-testid="stPopover"] > button {
        margin: 0 !important;
        padding: 0 4px !important;
        height: 40px !important;
        min-height: 40px !important;
    }
}

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# QUIZ
# ============================================================
QUIZ_QUESTIONS = [
    {
        "key": "activity",
        "question": "How active are you?",
        "subtitle": "Think about how much exercise you normally enjoy.",
        "options": [
            "Relaxed",
            "Moderately active",
            "Very active",
        ],
    },

    {
        "key": "size",
        "question": "What size dog would you prefer?",
        "subtitle": "Choose the size that would fit your lifestyle best.",
        "options": [
            "No preference",
            "Small",
            "Medium",
            "Large",
        ],
    },

    {
        "key": "grooming",
        "question": "How much grooming are you comfortable with?",
        "subtitle": "Some breeds require considerably more brushing and coat care.",
        "options": [
            "Low",
            "Moderate",
            "High",
        ],
    },

    {
        "key": "personality",
        "question": "What personality are you looking for?",
        "subtitle": "Choose the characteristic that matters most to you.",
        "options": [
            "Friendly & social",
            "Playful",
            "Calm",
            "Independent",
            "Protective",
        ],
    },

    {
        "key": "lifestyle",
        "question": "Which best describes your lifestyle?",
        "subtitle": "Your living environment can make some breeds a better match.",
        "options": [
            "Apartment / city",
            "Balanced everyday life",
            "House / more space",
            "Very active / outdoors",
        ],
    },
]


# ============================================================
# TRAINING_TOPICS
# ============================================================
TRAINING_TOPICS = {
    "Getting started": {
        "icon": "🐾",
        "title": "Getting started with training",
        "intro": (
            "Good training is built on consistency, patience and rewards. "
            "Start in a quiet environment and keep sessions short so your "
            "dog stays interested."
        ),
        "steps": [
            (
                "Choose a quiet place",
                "Begin somewhere with few distractions so your dog can focus on you."
            ),
            (
                "Prepare rewards",
                "Use small treats, a favourite toy or praise that your dog genuinely enjoys."
            ),
            (
                "Keep sessions short",
                "Five to ten minutes is usually enough. Several short sessions are better than one long session."
            ),
            (
                "Reward immediately",
                "Reward the behaviour as soon as it happens so your dog can understand what earned the reward."
            ),
        ],
        "tip": (
            "Finish while your dog is still interested. Training should feel "
            "like a game rather than a chore."
        ),
        "search": "positive dog training basics beginners",
    },

    "Sit": {
        "icon": "🦴",
        "title": "Teach your dog to sit",
        "intro": (
            "Sit is one of the easiest and most useful behaviours to teach. "
            "It also creates a foundation for stay, waiting and polite greetings."
        ),
        "steps": [
            (
                "Get your dog's attention",
                "Stand in front of your dog with a small treat in your hand."
            ),
            (
                "Guide the movement",
                "Hold the treat close to the nose and slowly move it upward and slightly backward."
            ),
            (
                "Reward the sit",
                "As your dog's head follows the treat, their bottom will usually lower. Reward immediately when they sit."
            ),
            (
                "Add the word",
                "Once your dog understands the movement, say “Sit” just before they perform it."
            ),
        ],
        "tip": (
            "Avoid pushing your dog's back down. Let your dog discover the "
            "position naturally."
        ),
        "search": "how to teach dog sit positive reinforcement",
    },

    "Stay": {
        "icon": "✋",
        "title": "Teach your dog to stay",
        "intro": (
            "Stay teaches your dog patience and impulse control. Build it "
            "slowly by increasing time and distance separately."
        ),
        "steps": [
            (
                "Start with sit",
                "Ask your dog to sit somewhere calm and familiar."
            ),
            (
                "Give your stay cue",
                "Say “Stay” once and use a consistent hand signal."
            ),
            (
                "Wait briefly",
                "Start with only one or two seconds, then reward your dog for remaining still."
            ),
            (
                "Increase gradually",
                "Slowly increase the duration, then begin adding a little distance."
            ),
        ],
        "tip": (
            "Don't increase distance and duration at the same time. Make only "
            "one part of the exercise harder at a time."
        ),
        "search": "how to teach dog stay positive reinforcement",
    },

    "Come": {
        "icon": "🐕",
        "title": "Teach reliable recall",
        "intro": (
            "A reliable recall is one of the most important skills your dog "
            "can learn. Coming to you should always lead to something positive."
        ),
        "steps": [
            (
                "Start somewhere safe",
                "Practise indoors or in a secure fenced area with very few distractions."
            ),
            (
                "Use your recall cue",
                "Say your dog's name followed by your chosen cue, such as “Come”."
            ),
            (
                "Make yourself rewarding",
                "Encourage your dog enthusiastically and reward generously when they reach you."
            ),
            (
                "Add distractions slowly",
                "Gradually practise from greater distances and around mild distractions."
            ),
        ],
        "tip": (
            "Never punish your dog after they come to you, even if they took "
            "a long time. Reaching you should always be worthwhile."
        ),
        "search": "dog recall training come positive reinforcement",
    },

    "Leave it": {
        "icon": "🚫",
        "title": "Teach leave it",
        "intro": (
            "Leave it helps prevent your dog from picking up food, rubbish "
            "or potentially dangerous objects."
        ),
        "steps": [
            (
                "Start with a treat",
                "Place a low-value treat in your closed hand and let your dog investigate."
            ),
            (
                "Wait",
                "Don't pull your hand away. Wait until your dog stops licking or pawing at it."
            ),
            (
                "Reward disengagement",
                "The moment your dog moves away or looks at you, reward from your other hand."
            ),
            (
                "Add the cue",
                "Once your dog understands the game, introduce the words “Leave it”."
            ),
        ],
        "tip": (
            "The reward should come from you, not from the object your dog "
            "was asked to leave."
        ),
        "search": "teach dog leave it positive reinforcement",
    },

    "Leash walking": {
        "icon": "🦮",
        "title": "Teach loose-leash walking",
        "intro": (
            "Loose-leash walking teaches your dog that staying near you is "
            "more rewarding than pulling ahead."
        ),
        "steps": [
            (
                "Start somewhere quiet",
                "Practise indoors, in a garden or on a quiet street before moving to busy areas."
            ),
            (
                "Reward the right position",
                "Reward your dog frequently whenever they walk close to you with a loose leash."
            ),
            (
                "Stop when they pull",
                "If the leash becomes tight, stop moving forward and wait for the tension to disappear."
            ),
            (
                "Add distractions",
                "Gradually practise around people, dogs and interesting smells as your dog improves."
            ),
        ],
        "tip": (
            "Don't expect a perfect walk immediately. Sniffing is important "
            "for dogs, so give them opportunities to explore too."
        ),
        "search": "loose leash walking dog positive reinforcement",
    },
}

# ============================================================
# HOW TO GET A DOG
# ============================================================

GET_DOG_NL_STEPS = [
    {
        "icon": "🏠",
        "title": "Decide what fits your life",
        "text": (
            "Think about your home, working hours, activity level, "
            "experience, budget and how much time you can spend on "
            "training and daily exercise."
        ),
    },

    {
        "icon": "🐕",
        "title": "Choose adoption or a breeder",
        "text": (
            "You can adopt from a Dutch shelter or rehoming organisation, "
            "or buy from a responsible breeder. Avoid making a decision "
            "based only on an attractive online advertisement."
        ),
    },

    {
        "icon": "🔎",
        "title": "Check the dog and seller",
        "text": (
            "If you are buying a puppy, visit the place where the puppy "
            "was raised. Check the living conditions, behaviour and health "
            "of the puppies and, where possible, meet the mother."
        ),
    },

    {
        "icon": "📄",
        "title": "Check the documents",
        "text": (
            "Before ownership is transferred, check that the dog has a "
            "microchip, is correctly registered and has an EU pet passport."
        ),
    },

    {
        "icon": "✅",
        "title": "Register your ownership",
        "text": (
            "After getting the dog, register yourself as the new owner "
            "through one of the designated dog-registration portals. "
            "The previous owner separately reports that the dog has left."
        ),
    },

    {
        "icon": "🩺",
        "title": "Arrange a vet visit",
        "text": (
            "Schedule an initial veterinary check and discuss vaccinations, "
            "parasite prevention, nutrition and any breed-specific health risks."
        ),
    },

    {
        "icon": "🦴",
        "title": "Give the dog time to settle",
        "text": (
            "Keep the first days calm. Establish predictable routines for "
            "sleep, meals, toilet breaks, walks and training before gradually "
            "introducing more people and environments."
        ),
    },
]

# ============================================================
# PAT THE SHIBA WIDGET
# Original interactive Shiba design embedded for the homepage.
# ============================================================
PAT_THE_SHIBA_HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Pat the Shiba</title>
<style>
:root{--bg:#F4F1EC;--panel:#FFFFFF;--text:#1A1C22;--muted:#5B6270;--line:#E0DCD3;--accent:#5B3DF5;--on:#FFFFFF;
box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#101216;--panel:#1A1D24;--text:#F2F3F5;--muted:#A3A9B6;--line:#2B303B;--accent:#8B7BFF;--on:#101216}}
:root[data-theme="dark"]{--bg:#101216;--panel:#1A1D24;--text:#F2F3F5;--muted:#A3A9B6;--line:#2B303B;--accent:#8B7BFF;--on:#101216}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{width:100%;max-width:560px;margin:0 auto;padding:4px 0 8px;display:flex;flex-direction:column;gap:12px;background:transparent;border:0;border-radius:0;box-shadow:none}
.pat-hint{display:flex;align-items:center;justify-content:center;gap:9px;margin:0 auto 2px;padding:9px 16px;border:1px solid rgba(255,255,255,.78);border-radius:999px;background:rgba(255,255,255,.62);color:#745b87;font-size:14px;font-weight:750;letter-spacing:.1px;box-shadow:0 5px 18px rgba(91,61,120,.07)}
.pat-hint .hand{display:inline-block;font-size:19px;transform-origin:70% 80%;animation:patWave 1.5s ease-in-out infinite}
@keyframes patWave{0%,100%{transform:rotate(0)}25%{transform:rotate(-18deg)}50%{transform:rotate(9deg)}75%{transform:rotate(-12deg)}}
h1{margin:0;font-size:clamp(30px,7vw,44px);line-height:1.1}
p{margin:6px 0 0;color:var(--muted)}
.stage{position:relative;background:transparent;border:0;border-radius:0;padding:0 4px;overflow:hidden}
svg{display:block;width:100%;max-width:420px;margin:0 auto;touch-action:none;user-select:none;-webkit-user-select:none}
[data-act]{cursor:pointer}
.heart{position:absolute;width:22px;pointer-events:none}
.bubble{position:absolute;font-weight:800;color:var(--accent);pointer-events:none}
.tail{transform-origin:290px 340px;animation:sway 3s ease-in-out infinite}
.joy .tail{animation:wag var(--wag,.26s) ease-in-out infinite alternate}
.dogw{transform-origin:200px 392px;animation:breathe 3.2s ease-in-out infinite}
.eyes{transform-origin:200px 165px;animation:blink 5s infinite}
.happy,.tongue,.grin,.spark,.heartEyes{opacity:0;transition:opacity .2s}
.cheek{opacity:.35;transition:opacity .4s}
.lv1 .cheek{opacity:.55}.lv2 .cheek{opacity:.75}
.lv2 .grin,.lv2 .spark,.lv2 .tongue{opacity:1}
.joy .eyes{opacity:0}.joy .happy,.joy .tongue{opacity:1}
.lv3 .eyes,.lv3 .happy{opacity:0}.lv3 .heartEyes{opacity:1}
.ear{transition:transform .3s}
.ear.l{transform-origin:128px 140px}.ear.r{transform-origin:272px 140px}
.joy .ear.l{transform:rotate(-10deg)}.joy .ear.r{transform:rotate(10deg)}
#head{transform-origin:200px 275px}#nose{transform-origin:200px 204px}
@keyframes sway{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(5deg)}}
@keyframes wag{from{transform:rotate(-22deg)}to{transform:rotate(22deg)}}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.012)}}
@keyframes blink{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
@media (prefers-reduced-motion:reduce){.tail,.dogw,.eyes{animation:none!important}}
</style>
</head>
<body style="background:transparent">
<main>
<div class="pat-hint"><span class="hand" aria-hidden="true">👋</span><span>Go ahead — give me a pat!</span></div>
<div class="stage" id="stage">
<svg id="dog" viewBox="0 0 400 420" role="img" aria-label="A cute Shiba Inu waiting to be petted">
<ellipse cx="200" cy="398" rx="125" ry="13" fill="#000" opacity=".14"/>
<g class="tail"><path d="M286 336Q352 334 342 274Q334 236 302 248" stroke="#D9822B" stroke-width="30" stroke-linecap="round" fill="none"/><path d="M346 292Q338 250 308 247" stroke="#FFF1DC" stroke-width="9" stroke-linecap="round" fill="none"/></g>
<g class="dogw">
<ellipse cx="200" cy="322" rx="108" ry="82" fill="#D9822B"/>
<ellipse cx="200" cy="350" rx="62" ry="50" fill="#FFF1DC"/>
<rect x="132" y="335" width="54" height="58" rx="27" fill="#D9822B"/><rect x="214" y="335" width="54" height="58" rx="27" fill="#D9822B"/>
<ellipse cx="159" cy="391" rx="30" ry="15" fill="#FFF1DC"/><ellipse cx="241" cy="391" rx="30" ry="15" fill="#FFF1DC"/>
<ellipse data-act="belly" cx="200" cy="350" rx="66" ry="42" fill="transparent" pointer-events="all"/>
<g id="head">
<g class="ear l"><path d="M104 170L112 80L174 124z" fill="#D9822B"/><path d="M117 152L121 100L154 126z" fill="#F4B6B0"/></g>
<g class="ear r"><path d="M296 170L288 80L226 124z" fill="#D9822B"/><path d="M283 152L279 100L246 126z" fill="#F4B6B0"/></g>
<ellipse cx="200" cy="188" rx="98" ry="82" fill="#D9822B"/>
<path d="M104 200Q108 264 200 270Q292 264 296 200Q262 234 200 228Q138 234 104 200z" fill="#FFF1DC"/><circle cx="158" cy="138" r="7" fill="#FFF1DC"/><circle cx="242" cy="138" r="7" fill="#FFF1DC"/>
<circle class="cheek" cx="140" cy="200" r="13" fill="#F4727F"/><circle class="cheek" cx="260" cy="200" r="13" fill="#F4727F"/>
<ellipse cx="200" cy="220" rx="46" ry="36" fill="#FFF1DC"/>
<path d="M200 214v12M184 228q16 14 32 0" stroke="#2B2118" stroke-width="4" fill="none" stroke-linecap="round"/>
<path class="grin" d="M174 226Q200 272 226 226Q200 238 174 226z" fill="#8A3030"/>
<path class="tongue" d="M191 236q9 22 18 0z" fill="#F4727F"/>
<ellipse id="nose" cx="200" cy="204" rx="15" ry="11" fill="#2B2118"/><ellipse cx="195" cy="200" rx="4" ry="2.5" fill="#fff" opacity=".7"/>
<g class="eyes"><circle cx="160" cy="165" r="11" fill="#2B2118"/><circle cx="240" cy="165" r="11" fill="#2B2118"/><circle cx="164" cy="161" r="3.5" fill="#fff"/><circle cx="244" cy="161" r="3.5" fill="#fff"/></g>
<g class="spark" fill="#fff"><path d="M150 152l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/><path d="M230 152l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/></g>
<g class="happy" fill="none" stroke="#2B2118" stroke-width="6" stroke-linecap="round"><path d="M146 170q14-20 28 0"/><path d="M226 170q14-20 28 0"/></g>
<g class="heartEyes" fill="#F4727F"><path d="M160 180S141 168 141 156A9.5 9.5 0 0 1 160 153A9.5 9.5 0 0 1 179 156C179 168 160 180 160 180z"/><path d="M240 180S221 168 221 156A9.5 9.5 0 0 1 240 153A9.5 9.5 0 0 1 259 156C259 168 240 180 240 180z"/></g>
<ellipse data-act="head" cx="200" cy="170" rx="104" ry="100" fill="transparent" pointer-events="all"/>
<ellipse data-act="ear" cx="116" cy="185" rx="28" ry="56" transform="rotate(14 116 185)" fill="transparent" pointer-events="all"/>
<ellipse data-act="ear" cx="284" cy="185" rx="28" ry="56" transform="rotate(-14 284 185)" fill="transparent" pointer-events="all"/>
<ellipse data-act="chin" cx="200" cy="257" rx="50" ry="19" fill="transparent" pointer-events="all"/>
<ellipse data-act="boop" cx="200" cy="205" rx="20" ry="15" fill="transparent" pointer-events="all"/>
</g>
</g>
<g id="hand" opacity="0" pointer-events="none">
    <!-- Wrist -->
    <path
        d="M-13 12 Q-15 30 -11 43 L11 43 Q15 28 13 12Z"
        fill="#E8B58F"
    />

    <!-- Palm -->
    <path
        d="M-23 -18
           Q-25 -31 -17 -39
           Q-10 -45 0 -42
           Q13 -42 22 -33
           Q29 -25 24 -8
           L19 13
           Q15 25 0 25
           Q-17 24 -21 10Z"
        fill="#F1C9A5"
        stroke="#D9A782"
        stroke-width="1.2"
    />

    <!-- Fingers -->
    <path d="M-19 -24 Q-23 -39 -20 -51 Q-18 -58 -13 -55 Q-8 -53 -10 -40 L-8 -24"
        fill="#F1C9A5" stroke="#D9A782" stroke-width="1"/>

    <path d="M-8 -31 Q-12 -49 -7 -59 Q-4 -65 1 -61 Q5 -58 2 -45 L3 -27"
        fill="#F1C9A5" stroke="#D9A782" stroke-width="1"/>

    <path d="M4 -31 Q2 -48 7 -57 Q11 -63 16 -58 Q19 -54 14 -39 L13 -24"
        fill="#F1C9A5" stroke="#D9A782" stroke-width="1"/>

    <!-- Thumb -->
    <path d="M19 -17 Q33 -27 38 -17 Q42 -10 32 -3 L22 5"
        fill="#F1C9A5" stroke="#D9A782" stroke-width="1"/>
</g>
</svg>
</div>
</main>
<script>
const $=id=>document.getElementById(id),svg=$('dog'),head=$('head'),hand=$('hand'),stage=$('stage'),nose=$('nose');
const body=document.querySelector('.dogw'),earL=document.querySelector('.ear.l'),earR=document.querySelector('.ear.r');
const HEART='<svg viewBox="0 0 24 22"><path d="M12 21S2 14 2 7.5A5.5 5.5 0 0 1 12 5a5.5 5.5 0 0 1 10 2.5C22 14 12 21 12 21z" fill="#F4727F"/></svg>';
const SPOT={head:[200,150],ear:[116,180],chin:[200,257],belly:[200,350],boop:[200,205]};
const calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
let n=0,L=0,joyT=0,stroke=false,cur='',lastT=0,lx=0,ly=0,lastTouch=0;const seen={};function applyLevel(){L=n>=24?3:n>=12?2:n>=5?1:0;['lv1','lv2','lv3'].forEach((c,i)=>svg.classList.toggle(c,L>i));}
function toSvg(x,y){const p=svg.createSVGPoint();p.x=x;p.y=y;return p.matrixTransform(svg.getScreenCTM().inverse());}
function toClient(x,y){const p=svg.createSVGPoint();p.x=x;p.y=y;return p.matrixTransform(svg.getScreenCTM());}
function pop(el,cx,cy,dy,dur){const b=stage.getBoundingClientRect();el.style.left=(cx-b.left)+'px';el.style.top=(cy-b.top)+'px';stage.appendChild(el);
if(calm){setTimeout(()=>el.remove(),700);return;}el.animate([{transform:'translateY(0) scale(.6)',opacity:0},{opacity:1,offset:.2},{transform:'translateY('+dy+'px) scale(1.1)',opacity:0}],{duration:dur,easing:'ease-out'}).onfinish=()=>el.remove();}
function heart(cx,cy){const h=document.createElement('div');h.className='heart';h.innerHTML=HEART;pop(h,cx-11+Math.random()*40-20,cy-30,-90,1100);}
function say(t,cx,cy){const b=document.createElement('div');b.className='bubble';b.textContent=t;pop(b,cx+10,cy-40,-40,800);}

function handAnim(k, p) {
    // Rotate the SVG hand around its own centre.
    hand.style.transformBox = 'fill-box';
    hand.style.transformOrigin = 'center';

    const t = (dx, dy, opacity, offset, angle = 0) => ({
        transform:
            'translate(' + (p.x + dx) + 'px,' +
            (p.y - 26 + dy) + 'px) rotate(' + angle + 'deg)',
        opacity,
        offset
    });

    let f, d = 500;

    if (k === 'head') {
        // Hand turned sideways, sweeping across the head.
        f = [
            t(-35, -10, 0, 0, -90),
            t(-25, 0, 1, 0.15, -90),
            t(-10, 0, 1, 0.3, -90),
            t(10, 0, 1, 0.5, -90),
            t(25, 0, 1, 0.7, -90),
            t(35, -10, 0, 1, -90)
        ];
        d = 750;
    }
    else if (k === 'boop') {
        f = [
            t(0, -70, 0, 0),
            t(0, -14, 1, 0.35),
            t(0, -6, 1, 0.55),
            t(0, -60, 0, 1)
        ];
        d = 340;
    }
    else if (k === 'belly') {
        f = [
            t(0, -60, 0, 0),
            t(14, -8, 1, 0.15),
            t(0, 2, 1, 0.35),
            t(-14, -8, 1, 0.55),
            t(0, -18, 1, 0.75),
            t(0, -60, 0, 1)
        ];
        d = 800;
    }
    else {
        f = [
            t(0, -60, 0, 0),
            t(-12, -8, 1, 0.2),
            t(12, -8, 1, 0.4),
            t(-12, -8, 1, 0.6),
            t(12, -8, 1, 0.8),
            t(0, -60, 0, 1)
        ];
        d = 650;
    }

    hand.animate(f, {
        duration: d,
        easing: 'ease-in-out',
        fill: 'none'
    });
}
function act(a,cx,cy){
const p=toSvg(cx,cy),first=!seen[a];seen[a]=1;n+=first?3:1;
const oL=L;lastTouch=performance.now();applyLevel();
svg.style.setProperty('--wag',Math.max(.11,.26-n*.006)+'s');
svg.classList.add('joy');clearTimeout(joyT);joyT=setTimeout(()=>svg.classList.remove('joy'),1500);
if(!calm){handAnim(a,p);
if(a==='head')head.animate([{transform:'scale(1,1)'},{transform:'scale(1.04,.9)'},{transform:'scale(.98,1.04)'},{transform:'scale(1,1)'}],{duration:380});
else if(a==='ear'){const l=p.x<200;(l?earL:earR).animate([{transform:'rotate(0)'},{transform:'rotate('+(l?-18:18)+'deg)'},{transform:'rotate('+(l?8:-8)+'deg)'},{transform:'rotate(0)'}],{duration:320});
head.animate([{transform:'rotate(0)'},{transform:'rotate('+(l?-3:3)+'deg)'},{transform:'rotate(0)'}],{duration:400});}
else if(a==='chin')head.animate([{transform:'rotate(0) translateY(0)'},{transform:'rotate(-6deg) translateY(-6px)',offset:.3},{transform:'rotate(-6deg) translateY(-6px)',offset:.8},{transform:'rotate(0) translateY(0)'}],{duration:700});
else if(a==='belly')body.animate([{transform:'rotate(0) scale(1)'},{transform:'rotate(-3deg) scale(1.03,.97)'},{transform:'rotate(3deg) scale(.98,1.03)'},{transform:'rotate(0) scale(1)'}],{duration:420});
else{nose.animate([{transform:'scale(1)'},{transform:'scale(1.5)'},{transform:'scale(1)'}],{duration:260});head.animate([{transform:'translateY(0)'},{transform:'translateY(5px)'},{transform:'translateY(0)'}],{duration:260});}}
if(a==='boop')say('Boop!',cx,cy);
heart(cx,cy);if(a==='belly')heart(cx+20,cy);
if(L>oL){const c=toClient(200,110);for(let i=0;i<5;i++)setTimeout(()=>heart(c.x,c.y),i*120);}}
const A=e=>{const el=document.elementFromPoint(e.clientX,e.clientY);return el&&el.dataset?el.dataset.act:'';};
svg.addEventListener('pointerdown',e=>{const a=A(e);if(!a)return;e.preventDefault();stroke=true;cur=a;lx=e.clientX;ly=e.clientY;lastT=performance.now();act(a,e.clientX,e.clientY);});
svg.addEventListener('pointermove',e=>{if(!stroke)return;const a=A(e),t=performance.now();if(!a||a==='boop')return;
if(t-lastT>160&&(a!==cur||t-lastT>260)&&Math.hypot(e.clientX-lx,e.clientY-ly)>24){cur=a;lastT=t;lx=e.clientX;ly=e.clientY;act(a,e.clientX,e.clientY);}});
['pointerup','pointercancel'].forEach(k=>addEventListener(k,()=>{stroke=false;}));
setInterval(()=>{if(n>0&&!stroke&&performance.now()-lastTouch>2500){n=Math.max(0,n-2);applyLevel();}},250);setInterval(()=>{if(L>=3&&!document.hidden&&!calm){const c=toClient(200,100);heart(c.x,c.y);}},1600);
</script>
</body>
</html>
'''


# ============================================================
# PATHS
# ============================================================
BREEDS_URL = "https://dog.ceo/api/breeds/list/all"
MANIFEST_FILE = "breed_images.json"
#BREED_INFO_FILE = "dogs.json"

# ============================================================
# DATA / API
# ============================================================
@st.cache_data(ttl=86400)
def get_breeds():
    response = requests.get(BREEDS_URL, timeout=15)
    response.raise_for_status()
    return response.json()["message"]


@st.cache_data(ttl=86400)
def get_breed_images(breed, sub_breed=None, amount=9):
    if sub_breed:
        url = f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images"
    else:
        url = f"https://dog.ceo/api/breed/{breed}/images"

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()["message"][:amount]


@st.cache_data
def load_manifest():
    if not os.path.exists(MANIFEST_FILE):
        return {}

    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}
    

def create_breed_list(breeds):
    result = []
    for breed, sub_breeds in breeds.items():
        if not sub_breeds:
            result.append({
                "id": breed,
                "breed": breed,
                "sub_breed": None,
                "display_name": breed.title(),
            })
        else:
            for sub_breed in sub_breeds:
                result.append({
                    "id": f"{breed}_{sub_breed}",
                    "breed": breed,
                    "sub_breed": sub_breed,
                    "display_name": f"{sub_breed.title()} {breed.title()}",
                })
    return result


def get_breed_information(breed, sub_breed=None):
    search_name = f"{sub_breed} {breed}".lower() if sub_breed else breed.lower()

    for dog in breed_information:
        if dog.get("breed", "").lower() == search_name:
            return dog

    display_name = f"{sub_breed.title()} {breed.title()}" if sub_breed else breed.title()

    return {
        "breed": search_name,
        "name": display_name,
        "origin": "Information coming soon",
        "group": "Other",
        "size": "Information coming soon",
        "height": "Information coming soon",
        "weight": "Information coming soon",
        "life_span": "Information coming soon",
        "temperament": "Information coming soon",
        "energy": "Information coming soon",
        "grooming": "Information coming soon",
        "description": f"{display_name} is a dog breed or breed variety. Detailed information will be added soon.",
    }


def local_image_for(dog):
    path = breed_images.get(dog["id"])
    if path and os.path.exists(path):
        return path
    return None

def gallery_image(image_url):
    st.markdown(
        f"""
        <div class="gallery-image">
            <img src="{html.escape(image_url)}">
        </div>
        """,
        unsafe_allow_html=True,
    )

@st.cache_data(ttl=86400)
def get_youtube_videos(breed_name, max_results=4):
    query = f"{breed_name} dog breed"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch{max_results}:{query}",
                download=False
            )

        videos = []

        for item in result.get("entries", []):
            if not item:
                continue

            video_id = item.get("id")

            if not video_id:
                continue

            videos.append({
                "id": video_id,
                "title": item.get(
                    "title",
                    f"{breed_name} video"
                ),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

        return videos[:max_results]

    except Exception as error:
        print(
            f"YouTube search error for {breed_name}:",
            error
        )

        return []
    
@st.cache_data(ttl=86400)
def get_training_videos(topic, max_results=4):
    query = f"dog training {topic}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch{max_results}:{query}",
                download=False
            )

        videos = []

        for item in result.get("entries", []):
            if not item:
                continue

            video_id = item.get("id")

            if not video_id:
                continue

            videos.append({
                "id": video_id,
                "title": item.get("title", "Dog training video"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

        return videos[:max_results]

    except Exception as error:
        print("Training video search error:", error)
        return []
    
def calculate_dog_matches(answers):

    results = []

    temperament_words = {
        "Friendly & social": [
            "friendly",
            "social",
            "outgoing",
            "gentle",
            "affectionate",
        ],

        "Playful": [
            "playful",
            "lively",
            "curious",
            "energetic",
        ],

        "Calm": [
            "calm",
            "gentle",
            "patient",
            "dignified",
        ],

        "Independent": [
            "independent",
            "confident",
            "reserved",
        ],

        "Protective": [
            "protective",
            "loyal",
            "courageous",
            "alert",
        ],
    }

    for dog in all_breeds:

        info = get_breed_information(
            dog["breed"],
            dog["sub_breed"]
        )

        score = 0
        possible_score = 0

        energy = str(
            info.get("energy", "")
        ).lower()

        size = str(
            info.get("size", "")
        ).lower()

        grooming = str(
            info.get("grooming", "")
        ).lower()

        temperament = str(
            info.get("temperament", "")
        ).lower()

        # ====================================================
        # ACTIVITY
        # ====================================================

        possible_score += 3

        activity = answers.get("activity")

        if activity == "Relaxed":

            if energy in [
                "low",
                "low to moderate",
                "moderate",
            ]:
                score += 3

        elif activity == "Moderately active":

            if energy in [
                "moderate",
                "moderate to high",
                "high",
            ]:
                score += 3

        elif activity == "Very active":

            if energy in [
                "moderate to high",
                "high",
                "very high",
            ]:
                score += 3

        # ====================================================
        # SIZE
        # ====================================================

        possible_score += 3

        preferred_size = answers.get("size")

        if preferred_size == "No preference":

            score += 3

        elif preferred_size == "Small":

            if size in [
                "very small",
                "small",
                "small to medium",
            ]:
                score += 3

        elif preferred_size == "Medium":

            if size in [
                "small to medium",
                "medium",
                "medium to large",
            ]:
                score += 3

        elif preferred_size == "Large":

            if size in [
                "medium to large",
                "large",
                "large to giant",
                "giant",
            ]:
                score += 3

        # ====================================================
        # GROOMING
        # ====================================================

        possible_score += 2

        grooming_answer = answers.get("grooming")

        if grooming_answer == "Low":

            if grooming in [
                "low",
                "low to moderate",
            ]:
                score += 2

        elif grooming_answer == "Moderate":

            if grooming in [
                "low to moderate",
                "moderate",
                "moderate to high",
            ]:
                score += 2

        elif grooming_answer == "High":

            if grooming in [
                "moderate",
                "moderate to high",
                "high",
                "very high",
            ]:
                score += 2

        # ====================================================
        # PERSONALITY
        # ====================================================

        possible_score += 3

        personality = answers.get("personality")

        desired_words = temperament_words.get(
            personality,
            []
        )

        if any(
            word in temperament
            for word in desired_words
        ):
            score += 3

        # ====================================================
        # LIFESTYLE
        # ====================================================

        possible_score += 3

        lifestyle = answers.get("lifestyle")

        if lifestyle == "Apartment / city":

            if (
                size in [
                    "very small",
                    "small",
                    "small to medium",
                ]
                and energy not in [
                    "very high"
                ]
            ):
                score += 3

        elif lifestyle == "Balanced everyday life":

            if energy in [
                "low to moderate",
                "moderate",
                "moderate to high",
            ]:
                score += 3

        elif lifestyle == "House / more space":

            if size in [
                "medium",
                "medium to large",
                "large",
                "large to giant",
            ]:
                score += 3

        elif lifestyle == "Very active / outdoors":

            if energy in [
                "high",
                "very high",
            ]:
                score += 3

        # ====================================================
        # FINAL SCORE
        # ====================================================

        percentage = round(
            score / possible_score * 100
        )

        results.append({
            "dog": dog,
            "info": info,
            "score": percentage,
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:5]

def home_link():
    if st.button(
        "🐕 Dog Encyclopedia",
        key=f"home_link_{st.session_state.page}",
        type="tertiary"
    ):
        st.session_state.page = "home"
        st.session_state.selected_breed = None
        st.query_params.clear()
        st.rerun()

@st.cache_data(ttl=86400)
def get_nl_dog_videos(max_results=2):

    query = (
        "getting adopting buying dog Netherlands "
        "puppy responsible owner"
    )

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "noplaylist": True,
    }

    try:

        with YoutubeDL(ydl_opts) as ydl:

            result = ydl.extract_info(
                f"ytsearch{max_results}:{query}",
                download=False
            )

        videos = []

        for item in result.get("entries", []):

            if not item:
                continue

            video_id = item.get("id")

            if not video_id:
                continue

            videos.append({
                "id": video_id,
                "title": item.get(
                    "title",
                    "Getting a dog in the Netherlands"
                ),
                "url": (
                    f"https://www.youtube.com/watch?v={video_id}"
                ),
            })

        return videos[:max_results]

    except Exception as error:

        print(
            "NL dog video search error:",
            error
        )

        return []

def main_navigation():

    with st.container(key="main_navigation"):

        nav_left, nav_menu = st.columns(
            [9.5, 0.5],
            vertical_alignment="center",
            gap="small"
        )

        with nav_left:
            home_link()

        with nav_menu:

            with st.popover(
                "☰",
                use_container_width=False
            ):

                if st.button(
                    "Find your match",
                    key=f"menu_match_{st.session_state.page}",
                    use_container_width=True
                ):
                    st.session_state.page = "quiz"
                    st.session_state.selected_breed = None
                    st.query_params.clear()
                    st.rerun()

                if st.button(
                    "Dog training",
                    key=f"menu_training_{st.session_state.page}",
                    use_container_width=True
                ):
                    st.session_state.page = "training"
                    st.session_state.selected_breed = None
                    st.query_params.clear()
                    st.rerun()

                if st.button(
                    "Getting a dog in NL",
                    key=f"menu_nl_{st.session_state.page}",
                    use_container_width=True
                ):
                    st.session_state.page = "get_dog_nl"
                    st.session_state.selected_breed = None
                    st.query_params.clear()
                    st.rerun()
                if st.button(
                    "Dog AI Assistant",
                    key=f"menu_ai_{st.session_state.page}",
                    use_container_width=True
                ):
                    st.session_state.page = "ai_assistant"
                    st.session_state.selected_breed = None
                    st.query_params.clear()
                    st.rerun()

# ============================================================
# LOAD DATA
# ============================================================
try:
    breeds = get_breeds()
except Exception as error:
    st.error("Unable to load dog breeds from Dog CEO.")
    st.write(error)
    st.stop()

breed_images = load_manifest()
all_breeds = create_breed_list(breeds)

if "selected_breed" not in st.session_state:
    st.session_state.selected_breed = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 0

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = None

    # your homepage content
# ============================================================
# URL PAGE ROUTING
# ============================================================

page_param = st.query_params.get("page")

if page_param in [
    "home",
    "quiz",
    "training",
    "get_dog_nl",
    "ai_assistant"
]:
    st.session_state.page = page_param

# Open breed from clickable image
breed_id = st.query_params.get("breed")

if breed_id and not st.session_state.selected_breed:
    for dog in all_breeds:
        if dog["id"] == breed_id:
            st.session_state.selected_breed = dog
            break

detail_placeholder = st.empty()
quiz_placeholder = st.empty()
# ============================================================
# DETAIL PAGE
# ============================================================

if st.session_state.selected_breed:
    with detail_placeholder.container():
        main_navigation()
        selected = st.session_state.selected_breed
        breed = selected["breed"]
        sub_breed = selected["sub_breed"]
        display_name = selected["display_name"]
        info = get_breed_information(breed, sub_breed)
    
        st.markdown(
            f"""
            <div class="detail-title">{html.escape(display_name)}</div>
            <div class="detail-subtitle">Dog Encyclopedia · Breed profile</div>
            """,
            unsafe_allow_html=True,
        )
    
        # ============================================================
        # BREED DETAIL CONTENT
        # ============================================================
    
        top_left, top_right = st.columns([1.05, 1.3], gap="large")
    
        # ------------------------------------------------------------
        # LEFT: MAIN IMAGE
        # ------------------------------------------------------------
        with top_left:
            local_main = local_image_for(selected)
    
            if local_main:
                st.image(
                    local_main,
                    use_container_width=True
                )
            else:
                try:
                    detail_images = get_breed_images(
                        breed,
                        sub_breed,
                        amount=1
                    )
    
                    if detail_images:
                        st.image(
                            detail_images[0],
                            use_container_width=True
                        )
    
                except Exception:
                    pass
                
                
        # ------------------------------------------------------------
        # RIGHT: DESCRIPTION + FACTS
        # ------------------------------------------------------------
        with top_right:
        
            st.markdown(
                '<div class="section-title compact-title">About</div>',
                unsafe_allow_html=True
            )
    
            st.markdown(
                f'''
                <div class="detail-description">
                    {html.escape(str(info["description"]))}
                </div>
                ''',
                unsafe_allow_html=True
            )
    
            st.markdown(
                '<div class="section-title compact-facts-title">Quick facts</div>',
                unsafe_allow_html=True
            )
    
            facts = [
                ("Origin", info["origin"]),
                ("Height", info["height"]),
                ("Weight", info["weight"]),
                ("Life span", info["life_span"]),
                ("Temperament", info["temperament"]),
                ("Energy", info["energy"]),
                ("Grooming", info["grooming"]),
            ]
    
            facts_html = '<div class="facts-compact-list">'
    
            for label, value in facts:
                facts_html += (
                    '<div class="fact-row">'
                    f'<div class="fact-label">{html.escape(str(label))}</div>'
                    f'<div class="fact-value">{html.escape(str(value))}</div>'
                    '</div>'
                )
    
            facts_html += '</div>'
    
            st.markdown(
                facts_html,
                unsafe_allow_html=True
            )
    
        # Gallery: remote only when detail page is opened
        try:
            gallery = get_breed_images(breed, sub_breed, amount=9)
        except Exception:
            gallery = []
    
        if len(gallery) > 1:
            st.markdown(
            '<div class="section-title">More photos</div>',
            unsafe_allow_html=True
            )
    
            gallery_columns = st.columns(4)
    
            for index, image_url in enumerate(gallery[1:9]):
                with gallery_columns[index % 4]:
                    gallery_image(image_url)
    
        # ============================================================
        # WATCH & LEARN
        # ============================================================
    
        st.markdown(
            '<div class="section-title">Watch videos</div>',
            unsafe_allow_html=True
        )
    
        videos = get_youtube_videos(
            display_name,
            max_results=4
        )
    
        if videos:
        
            video_columns = st.columns(
                2,
                gap="medium"
            )
    
            for index, video in enumerate(videos):
            
                with video_columns[index % 2]:
                
                    st.video(
                        video["url"]
                    )
    
                    st.markdown(
                        f'''
                        <div class="video-title">
                            {html.escape(video["title"])}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
    
        else:
        
            st.caption(
                "No videos available for this breed."
            )
    
        st.markdown(
            '<div class="footer-note">🐕 Dog Encyclopedia · Photos provided by Dog CEO API</div>',
            unsafe_allow_html=True,
        )
        st.stop()

# ============================================================
# DOG AI ASSISTANT
# ============================================================

if st.session_state.page == "ai_assistant":

    main_navigation()

    from agent.chat_ui import render_chat_page

    render_chat_page()

    st.stop()

# ============================================================
# FIND YOUR DOG
# ============================================================

if st.session_state.page == "quiz":
    with quiz_placeholder.container():

        # Same navigation on BOTH questions and results
        main_navigation()

        # --------------------------------------------------------
        # RESULTS PAGE
        # --------------------------------------------------------

        if st.session_state.quiz_results is not None:

            st.markdown(
                (
                    '<div class="quiz-header">'
                    '<div class="quiz-kicker">YOUR RESULTS</div>'
                    '<h1>Your best matches.</h1>'
                    '<p>'
                    'Based on your lifestyle and preferences, '
                    'these breeds may suit you best.'
                    '</p>'
                    '</div>'
                    ),
                    unsafe_allow_html=True,
                )

            results = st.session_state.quiz_results

            for index, result in enumerate(results):

                dog = result["dog"]
                info = result["info"]
                score = result["score"]

                image_col, info_col = st.columns(
                    [1, 2.1],
                    gap="large"
                )

                with image_col:

                    image_path = local_image_for(dog)

                    if image_path:
                        st.image(
                            image_path,
                            use_container_width=True
                        )

                with info_col:

                    st.markdown(
                        f"""
                        <div class="match-rank">
                            #{index + 1} MATCH
                        </div>

                        <div class="match-name">
                            {html.escape(dog["display_name"])}
                        </div>

                        <div class="match-score">
                            {score}% match
                        </div>

                        <div class="match-temperament">
                            {html.escape(str(info["temperament"]))}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "View →",
                        key=f"match_{dog['id']}"
                    ):

                        st.session_state.selected_breed = dog

                        st.query_params["breed"] = dog["id"]

                        st.rerun()

                st.markdown(
                    '<div class="match-divider"></div>',
                    unsafe_allow_html=True
                )

            st.write("")

            if st.button(
                "↻ Take the test again"
            ):

                st.session_state.quiz_step = 0
                st.session_state.quiz_answers = {}
                st.session_state.quiz_results = None

                st.rerun()

            st.stop()

    # --------------------------------------------------------
    # QUESTION PAGE
    # --------------------------------------------------------

    step = st.session_state.quiz_step

    question_data = QUIZ_QUESTIONS[step]

    total_questions = len(QUIZ_QUESTIONS)

    progress = (
        (step + 1) /
        total_questions
    )

    # Progress
    st.progress(progress)

    st.markdown(
        f'<div class="quiz-progress-text">'
        f'Question {step + 1} of {total_questions}'
        f'</div>',
    unsafe_allow_html=True,
    )

    # Question
    st.markdown(
    (
        '<div class="quiz-question">'
            f'<h1>{html.escape(question_data["question"])}</h1>'
            f'<p>{html.escape(question_data["subtitle"])}</p>'
        '</div>'
    ),
    unsafe_allow_html=True,
)

    question_key = question_data["key"]

    previous_answer = (
        st.session_state.quiz_answers.get(
            question_key
        )
    )

    options = question_data["options"]

    default_index = None

    if previous_answer in options:
        default_index = options.index(
            previous_answer
        )

    answer = st.radio(
        question_data["question"],
        options,
        index=default_index,
        label_visibility="collapsed",
        key=f"quiz_question_{step}",
    )

    st.write("")

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    back_col, next_col = st.columns(
        [1, 1],
        gap="medium"
    )

    with back_col:

        if step > 0:
            

            if st.button(
                "← Back",
                use_container_width=True
            ):

                st.session_state.quiz_step -= 1

                st.rerun()

    with next_col:

        is_last_question = (
            step == total_questions - 1
        )

        button_text = (
            "See my matches 🐾"
            if is_last_question
            else "Next →"
        )

        if st.button(
            button_text,
            type="primary",
            use_container_width=True,
            disabled=answer is None,
            key=f"quiz_next_{step}",
        ):

            # Save current answer
            st.session_state.quiz_answers[
                question_key
            ] = answer

            if is_last_question:

                final_answers = dict(
                    st.session_state.quiz_answers
                )

                final_answers[
                    question_key
                ] = answer

                st.session_state.quiz_results = (
                    calculate_dog_matches(
                        final_answers
                    )
                )

            else:
                st.session_state.quiz_step += 1

            st.rerun()

    st.stop()


# ============================================================
# DOG TRAINING PAGE
# ============================================================

if st.session_state.page == "training":

    main_navigation()

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="training-hero">'
            '<div class="quiz-kicker">DOG TRAINING</div>'
            '<h1>Train your dog.</h1>'
            '<p>'
            'Build good habits through simple, positive and '
            'consistent training.'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # TRAINING PRINCIPLES
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-small-title">START HERE</div>',
        unsafe_allow_html=True,
    )

    principle_1, principle_2, principle_3 = st.columns(3)

    with principle_1:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">⏱️</div>'
                '<div class="training-principle-title">Keep it short</div>'
                '<div class="training-principle-text">'
                'Aim for 5–10 minute sessions.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    with principle_2:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">🦴</div>'
                '<div class="training-principle-title">Reward success</div>'
                '<div class="training-principle-text">'
                'Reward the behaviour you want to see again.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    with principle_3:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">🔁</div>'
                '<div class="training-principle-title">Be consistent</div>'
                '<div class="training-principle-text">'
                'Use the same cues and practise regularly.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="training-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # SELECT SKILL
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-small-title">CHOOSE A SKILL</div>',
        unsafe_allow_html=True,
    )

    selected_training_topic = st.selectbox(
        "Training skill",
        list(TRAINING_TOPICS.keys()),
        label_visibility="collapsed",
    )

    topic = TRAINING_TOPICS[selected_training_topic]

    # --------------------------------------------------------
    # TOPIC
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="training-topic-header">'
            f'<div class="training-topic-icon">{topic["icon"]}</div>'
            f'<h2>{html.escape(topic["title"])}</h2>'
            f'<p>{html.escape(topic["intro"])}</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # STEPS
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-small-title">STEP BY STEP</div>',
        unsafe_allow_html=True,
    )

    for number, (step_title, step_text) in enumerate(
        topic["steps"],
        start=1,
    ):
        st.markdown(
            (
                '<div class="training-step">'
                f'<div class="training-step-number">{number}</div>'
                '<div class="training-step-content">'
                f'<div class="training-step-title">'
                f'{html.escape(step_title)}'
                '</div>'
                f'<div class="training-step-text">'
                f'{html.escape(step_text)}'
                '</div>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # TIP
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="training-tip">'
            '<div class="training-tip-icon">💡</div>'
            '<div>'
            '<div class="training-tip-title">Training tip</div>'
            f'<div class="training-tip-text">'
            f'{html.escape(topic["tip"])}'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # VIDEOS
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            '<div class="training-video-heading">'
            '<div class="training-small-title">Watch videos</div>'
            '<h2>See it in action</h2>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    videos = get_training_videos(
        topic["search"],
        max_results=1,
    )

    if videos:

        video_columns = st.columns(
            2,
            gap="medium",
        )

        for index, video in enumerate(videos[:2]):

            with video_columns[index]:

                st.video(video["url"])

                st.markdown(
                    (
                        '<div class="video-title">'
                        f'{html.escape(video["title"])}'
                        '</div>'
                    ),
                    unsafe_allow_html=True,
                )

    else:
        st.caption(
            "No videos available for this training topic."
        )

    st.stop()


# ============================================================
# GETTING A DOG IN THE NETHERLANDS
# ============================================================

if st.session_state.page == "get_dog_nl":

    main_navigation()

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="training-hero">'
            '<div class="quiz-kicker">DOG OWNERSHIP · NETHERLANDS</div>'
            '<h1>Getting a dog in the Netherlands.</h1>'
            '<p>'
            'From choosing the right dog to checking documents '
            'and registering your new companion.'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # THREE MAIN OPTIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-small-title">WHERE TO START</div>',
        unsafe_allow_html=True,
    )

    adoption_col, breeder_col, rehome_col = st.columns(
        3,
        gap="large"
    )

    with adoption_col:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">🏠</div>'
                '<div class="training-principle-title">'
                'Adopt from a shelter'
                '</div>'
                '<div class="training-principle-text">'
                'Dutch shelters have dogs of different ages, '
                'breeds and backgrounds looking for new homes.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    with breeder_col:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">🐶</div>'
                '<div class="training-principle-title">'
                'Responsible breeder'
                '</div>'
                '<div class="training-principle-text">'
                'Take your time, visit the breeder and check '
                'health, socialisation and documentation.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    with rehome_col:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">❤️</div>'
                '<div class="training-principle-title">'
                'Rehoming'
                '</div>'
                '<div class="training-principle-text">'
                'An adult dog may be looking for a new home '
                'because its previous owner can no longer care for it.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="training-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # STEP BY STEP
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-small-title">STEP BY STEP</div>',
        unsafe_allow_html=True,
    )

    for number, step in enumerate(
        GET_DOG_NL_STEPS,
        start=1
    ):

        st.markdown(
            (
                '<div class="training-step">'
                f'<div class="training-step-number">{number}</div>'

                '<div class="training-step-content">'

                f'<div class="training-step-title">'
                f'{step["icon"]} '
                f'{html.escape(step["title"])}'
                '</div>'

                f'<div class="training-step-text">'
                f'{html.escape(step["text"])}'
                '</div>'

                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # IMPORTANT DOCUMENTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            '<div class="training-topic-header">'
            '<div class="training-topic-icon">📋</div>'
            '<h2>Before you take the dog home</h2>'
            '<p>'
            'Check these items before accepting ownership.'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    document_col1, document_col2, document_col3 = st.columns(3)

    with document_col1:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">🔢</div>'
                '<div class="training-principle-title">'
                'Microchip'
                '</div>'
                '<div class="training-principle-text">'
                'Check that the dog is chipped and that '
                'the chip number matches the documentation.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    with document_col2:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">📘</div>'
                '<div class="training-principle-title">'
                'EU pet passport'
                '</div>'
                '<div class="training-principle-text">'
                'A dog changing owner must have the required '
                'EU pet passport.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    with document_col3:
        st.markdown(
            (
                '<div class="training-principle">'
                '<div class="training-principle-icon">📝</div>'
                '<div class="training-principle-title">'
                'Registration'
                '</div>'
                '<div class="training-principle-text">'
                'Check that the dog is registered to the '
                'seller before ownership is transferred.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="training-tip">'
            '<div class="training-tip-icon">⚠️</div>'
            '<div>'
            '<div class="training-tip-title">'
            'Be careful with online puppy advertisements'
            '</div>'
            '<div class="training-tip-text">'
            'Avoid sellers who pressure you to decide immediately, '
            'will not let you visit where the puppy was raised, '
            'cannot show the mother, or cannot provide the required '
            'chip, registration and passport information.'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # IMPORTING
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="training-topic-header">'
            '<div class="training-topic-icon">✈️</div>'
            '<h2>Bringing a dog from abroad?</h2>'
            '<p>'
            'Different rules apply when you personally bring '
            'a dog into the Netherlands. The dog must already '
            'meet identification and travel requirements before '
            'entering the country, and additional registration '
            'requirements apply after arrival.'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # VIDEOS — ONLY TWO
    # --------------------------------------------------------

    st.markdown(
        '<div class="training-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            '<div class="training-video-heading">'
            '<div class="training-small-title">WATCH & LEARN</div>'
            '<h2>Before getting your dog.</h2>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    videos = get_nl_dog_videos(
        max_results=2
    )

    if videos:

        video_columns = st.columns(
            2,
            gap="medium"
        )

        for index, video in enumerate(videos[:2]):

            with video_columns[index]:

                st.video(
                    video["url"]
                )

                st.markdown(
                    (
                        '<div class="video-title">'
                        f'{html.escape(video["title"])}'
                        '</div>'
                    ),
                    unsafe_allow_html=True,
                )

    else:
        st.caption(
            "No videos available right now."
        )

    st.stop()


# ============================================================
# HOME PAGE
# ============================================================

main_navigation()

# Homepage hero + interactive Shiba pet
hero_text_col, shiba_col = st.columns(
    [1.35, 1],
    gap="large",
    vertical_alignment="center",
)

with hero_text_col:
    st.markdown(
        """
        <div class="hero">
            <h1 class="hero-title">
                Find a dog you'll <span>love.</span>
            </h1>
            <p class="hero-copy">Discover the companion who fits your lifestyle, your energy, and your heart.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with shiba_col:
    components.html(
        PAT_THE_SHIBA_HTML,
        height=590,
        scrolling=False,
    )

# ============================================================
# SEARCH / FILTERS
# ============================================================

SIZE_ORDER = [
    "Very Small",
    "Small",
    "Small to Medium",
    "Medium",
    "Medium to Large",
    "Large",
    "Large to Giant",
    "Giant",
]

ENERGY_ORDER = [
    "Low",
    "Low to Moderate",
    "Moderate",
    "Moderate to High",
    "High",
    "Very High",
]

GROOMING_ORDER = [
    "Low",
    "Low to Moderate",
    "Moderate",
    "Moderate to High",
    "High",
    "Very High",
]

origins = sorted({
    str(get_breed_information(
        dog["breed"],
        dog["sub_breed"]
    ).get("origin", "Unknown"))
    for dog in all_breeds
})

groups = sorted({
    str(get_breed_information(
        dog["breed"],
        dog["sub_breed"]
    ).get("group", "Other"))
    for dog in all_breeds
})

available_sizes = {
    str(get_breed_information(
        dog["breed"],
        dog["sub_breed"]
    ).get("size", "Unknown"))
    for dog in all_breeds
}

available_energies = {
    str(get_breed_information(
        dog["breed"],
        dog["sub_breed"]
    ).get("energy", "Unknown"))
    for dog in all_breeds
}

available_grooming = {
    str(get_breed_information(
        dog["breed"],
        dog["sub_breed"]
    ).get("grooming", "Unknown"))
    for dog in all_breeds
}


sizes = [
    value for value in SIZE_ORDER
    if value in available_sizes
]

energies = [
    value for value in ENERGY_ORDER
    if value in available_energies
]

grooming_levels = [
    value for value in GROOMING_ORDER
    if value in available_grooming
]


# ============================================================
# SEARCH ROW
# ============================================================

def search_breeds(searchterm: str):
    term = searchterm.lower().strip()

    if not term:
        return [
            dog["display_name"]
            for dog in all_breeds[:10]
        ]

    matches = [
        dog["display_name"]
        for dog in all_breeds
        if term in dog["display_name"].lower()
    ]

    return matches[:10]


default_breeds = [
    dog["display_name"]
    for dog in all_breeds[:]
]

search = st_searchbox(
    search_breeds,
    placeholder="Search breeds",
    key="breed_search",
    default_options=default_breeds,
    style_absolute=True,
    debounce=150,
    clear_on_submit=False,
    style_overrides={
        "searchbox": {
            "menuList": {
                "backgroundColor": "#ffffff",
                "border": "0.5px solid #d9d9d9",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.10)",
                "padding": "4px",
                "borderRadius": "6px",
            },
            "option": {
                "backgroundColor": "#ffffff",
                "color": "#222222",
                "borderRadius": "15px",
                "padding": "10px 12px",
            },
        }
    },
)

# ============================================================
# FILTER ROW
# ============================================================

origin_col, group_col, size_col, energy_col, grooming_col, sort_col = st.columns(6)

with origin_col:
    selected_origin = st.selectbox(
        "Origin",
        ["All"] + origins
    )

with group_col:
    selected_group = st.selectbox(
        "Group",
        ["All"] + groups
    )

with size_col:
    selected_size = st.selectbox(
        "Size",
        ["All"] + sizes
    )

with energy_col:
    selected_energy = st.selectbox(
        "Energy",
        ["All"] + energies
    )

with grooming_col:
    selected_grooming = st.selectbox(
        "Grooming",
        ["All"] + grooming_levels
    )

if "sort_descending" not in st.session_state:
    st.session_state.sort_descending = False

with sort_col:
    st.markdown(
        '<div class="filter-label">Sort</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "A → Z" if not st.session_state.sort_descending else "Z → A",
        use_container_width=True
    ):
        st.session_state.sort_descending = not st.session_state.sort_descending
        st.rerun()

# ============================================================
# FILTER BREEDS
# ============================================================

filtered_breeds = []

for dog in all_breeds:

    info = get_breed_information(
        dog["breed"],
        dog["sub_breed"]
    )

    matches_search = (
        not search
        or search.lower() in dog["display_name"].lower()
    )

    matches_origin = (
        selected_origin == "All"
        or str(info.get("origin")) == selected_origin
    )

    matches_group = (
        selected_group == "All"
        or str(info.get("group")) == selected_group
    )

    matches_size = (
        selected_size == "All"
        or str(info.get("size")) == selected_size
    )

    matches_energy = (
        selected_energy == "All"
        or str(info.get("energy")) == selected_energy
    )

    matches_grooming = (
        selected_grooming == "All"
        or str(info.get("grooming")) == selected_grooming
    )

    if (
        matches_search
        and matches_origin
        and matches_group
        and matches_size
        and matches_energy
        and matches_grooming
    ):
        filtered_breeds.append(dog)


# ============================================================
# SORT
# ============================================================

filtered_breeds = sorted(
    filtered_breeds,
    key=lambda dog: dog["display_name"].lower(),
    reverse=st.session_state.sort_descending,
)

st.markdown('<div class="section-title">Explore dogs</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-subtitle">{len(filtered_breeds)} breed(s)</div>',
    unsafe_allow_html=True,
)

if not filtered_breeds:
    st.info("No breeds found.")

CARDS_PER_ROW = 4

for row_start in range(0, len(filtered_breeds), CARDS_PER_ROW):
    row_dogs = filtered_breeds[row_start:row_start + CARDS_PER_ROW]
    columns = st.columns(CARDS_PER_ROW, gap="medium")

    for column, dog in zip(columns, row_dogs):
        with column:
            info = get_breed_information(
                dog["breed"],
                dog["sub_breed"]
            )

            image_path = local_image_for(dog)

            # --------------------------------------------------------
            # CLICKABLE IMAGE
            # --------------------------------------------------------
            if image_path:
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(
                        image_file.read()
                    ).decode()

                st.markdown(
                    f"""
                    <a href="?breed={dog['id']}" class="breed-image-link">
                        <img
                            src="data:image/jpeg;base64,{encoded_image}"
                            class="breed-card-image"
                        >
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

            else:
                st.markdown(
                    f"""
                    <a href="?breed={dog['id']}" class="breed-image-link">
                        <div class="breed-image-placeholder">
                            🐶
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

            # --------------------------------------------------------
            # BREED NAME
            # --------------------------------------------------------
            st.markdown(
                f'<div class="dog-card-title">{html.escape(dog["display_name"])}</div>',
                unsafe_allow_html=True,
            )

            # --------------------------------------------------------
            # DESCRIPTION
            # --------------------------------------------------------
            description = str(info["description"])

            if len(description) > 130:
                description = (
                    description[:127]
                    .rsplit(" ", 1)[0]
                    .rstrip(".,;: ")
                    + "..."
                )

            st.markdown(
                f'<div class="dog-card-description">{html.escape(description)}</div>',
                unsafe_allow_html=True,
            )

    st.write("")

st.markdown(
    '<div class="footer-note">🐕 Dog Encyclopedia · Photos provided by Dog CEO API</div>',
    unsafe_allow_html=True,
)
