import os
import json
import html
import streamlit as st
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

    .stApp { background: white; }
    .block-container { max-width: 1320px; padding-top: 1rem; padding-bottom: 4rem; }
    #MainMenu, footer, [data-testid="stHeader"] { display: none !important; }

    .top-nav {
        min-height: 64px; display: flex; justify-content: space-between;
        align-items: center; border-bottom: 1px solid var(--border); margin-bottom: 28px;
    }
    .brand { font-size: 19px; font-weight: 750; color: var(--text); }
    .hero { padding: 28px 0 36px 0; }
    .hero-title {
        margin: 0; font-size: clamp(42px, 5vw, 66px); line-height: 1;
        letter-spacing: -2.7px; font-weight: 800; color: var(--text);
    }
    .hero-title span { color: var(--accent); }
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

    nav_left, nav_menu = st.columns(
        [9.5, 0.5],
        vertical_alignment="center"
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
    "get_dog_nl"
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

st.markdown(
    """
    <div class="hero">
        <h1 class="hero-title">
            Find a dog you'll <span>love.</span>
        </h1>
    </div>
    """,
    unsafe_allow_html=True,
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
