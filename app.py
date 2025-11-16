"""
SignHub - Professional Sign Language Learning Platform
COMPLETE VERSION: Professional Frontend + ASL Alphabet Keyboard
"""

import streamlit as st
import json
import os
import re
import hashlib
import random
import time
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="SignHub - Master Sign Language",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ASL ALPHABET DATA
# ============================================================
ASL_ALPHABET = {
    'A': '👊', 'B': '✋', 'C': '👌', 'D': '☝️', 'E': '✊',
    'F': '🤏', 'G': '👈', 'H': '✌️', 'I': '🤙', 'J': '🤙',
    'K': '✌️', 'L': '👆', 'M': '👊', 'N': '✌️', 'O': '👌',
    'P': '☝️', 'Q': '👇', 'R': '✌️', 'S': '✊', 'T': '👊',
    'U': '✌️', 'V': '✌️', 'W': '🤟', 'X': '☝️', 'Y': '🤙', 'Z': '☝️'
}

ASL_DESCRIPTIONS = {
    'A': 'Closed fist with thumb alongside', 'B': 'Flat hand, fingers together',
    'C': 'Hand curved in C shape', 'D': 'Index finger up', 'E': 'Fingers curled',
    'F': 'Index and thumb form circle', 'G': 'Index and thumb point horizontally',
    'H': 'Index and middle fingers together', 'I': 'Pinky finger up',
    'J': 'Pinky up with J-motion', 'K': 'Index up, middle out, thumb between',
    'L': 'Thumb and index form L shape', 'M': 'Thumb under first three fingers',
    'N': 'Thumb under first two fingers', 'O': 'All fingers curved forming O',
    'P': 'K handshape pointing down', 'Q': 'Index and thumb point down',
    'R': 'Index and middle crossed', 'S': 'Fist with thumb across fingers',
    'T': 'Thumb between index and middle', 'U': 'Index and middle fingers up',
    'V': 'Index and middle apart', 'W': 'Three fingers up',
    'X': 'Index bent in hook shape', 'Y': 'Thumb and pinky extended',
    'Z': 'Draw Z in the air with index'
}

LANGUAGES = {
    "English": {
        "app_name": "SignHub",
        "tagline": "Master Sign Language. Connect with a New World.",
        "sub_tagline": "Learn ASL with interactive alphabet keyboard, quizzes, and games",
        "cta_primary": "Start Learning for Free",
        "alphabet_keyboard": "ASL Alphabet Keyboard",
        "click_letter": "Click any letter to see the hand sign",
        "login": "Sign In",
        "register": "Create Account",
        "dashboard": "Dashboard",
        "learning": "Learn",
        "quizzes": "Quizzes",
        "games": "Games",
        "profile": "Profile",
        "logout": "Logout",
        "welcome": "Welcome back",
        "feature1_title": "Interactive Lessons",
        "feature1_desc": "Learn with visual ASL alphabet keyboard",
        "feature2_title": "Video Dictionary",
        "feature2_desc": "Complete ASL sign reference guide",
        "feature3_title": "Practice & Games",
        "feature3_desc": "Quizzes and interactive games"
    },
    "हिंदी": {
        "app_name": "साइनहब",
        "tagline": "सांकेतिक भाषा में महारत हासिल करें",
        "sub_tagline": "इंटरैक्टिव कीबोर्ड के साथ ASL सीखें",
        "cta_primary": "मुफ्त में सीखना शुरू करें",
        "alphabet_keyboard": "ASL वर्णमाला कीबोर्ड",
        "click_letter": "किसी भी अक्षर को क्लिक करें",
        "login": "साइन इन",
        "register": "खाता बनाएं",
        "dashboard": "डैशबोर्ड",
        "learning": "सीखें",
        "quizzes": "क्विज",
        "games": "खेल",
        "profile": "प्रोफाइल",
        "logout": "लॉगआउट",
        "welcome": "स्वागत है",
        "feature1_title": "इंटरैक्टिव पाठ",
        "feature1_desc": "दृश्य ASL कीबोर्ड के साथ सीखें",
        "feature2_title": "वीडियो शब्दकोश",
        "feature2_desc": "सांकेतिक भाषा संदर्भ गाइड",
        "feature3_title": "अभ्यास और खेल",
        "feature3_desc": "क्विज और इंटरैक्टिव खेल"
    }
}

QUIZZES = {
    "ASL Alphabet Quiz": {
        "questions": [
            {"q": "What does the letter 'A' look like in ASL?", "options": ["Closed fist with thumb up", "Open palm", "Pointing finger", "Peace sign"], "correct": 0},
            {"q": "How do you sign the letter 'B'?", "options": ["Flat hand, fingers together", "Closed fist", "Two fingers up", "Thumb between fingers"], "correct": 0},
            {"q": "Which letter uses the 'OK' hand shape?", "options": ["C", "O", "F", "All of above"], "correct": 3},
            {"q": "How many handshapes are in the ASL alphabet?", "options": ["24", "26", "28", "30"], "correct": 1},
            {"q": "Which letters require movement?", "options": ["J and Z", "A and B", "X and Y", "None"], "correct": 0}
        ]
    },
    "Numbers Quiz": {
        "questions": [
            {"q": "How do you sign the number 1?", "options": ["Index finger up", "Thumb up", "Open palm", "Closed fist"], "correct": 0},
            {"q": "What number is signed with thumb and pinky?", "options": ["3", "5", "6", "9"], "correct": 2},
            {"q": "Which number looks like letter F?", "options": ["7", "8", "9", "10"], "correct": 2},
            {"q": "How do you sign 10?", "options": ["Thumbs up", "Open palms", "X shape", "Closed fist"], "correct": 0},
            {"q": "Numbers 1-5 hand orientation?", "options": ["Palm facing you", "Palm out", "Palm down", "Side"], "correct": 1}
        ]
    },
    "Greetings Quiz": {
        "questions": [
            {"q": "How to sign 'Hello'?", "options": ["Wave hand", "Salute", "Shake hands", "Nod"], "correct": 1},
            {"q": "Sign for 'Thank you'?", "options": ["Hand on chest", "Clapping", "Thumbs up", "Wave"], "correct": 0},
            {"q": "How to ask 'How are you?'", "options": ["Point up", "Shrug", "Wave", "Thumbs up"], "correct": 0},
            {"q": "What does chin touch mean?", "options": ["Think", "Please", "Sorry", "Mom"], "correct": 1},
            {"q": "How to sign 'Good morning'?", "options": ["Sun rising", "Wave", "Smile", "Flat hand"], "correct": 3}
        ]
    }
}

# ============================================================
# PROFESSIONAL CSS WITH KEYBOARD STYLES
# ============================================================
def get_professional_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&family=Open+Sans:wght@300;400;600&display=swap');

        * {
            font-family: 'Open Sans', sans-serif;
            box-sizing: border-box;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .main {
            background: #FFFFFF;
            padding: 0;
        }

        /* =============================================
           NAVIGATION BAR
        ============================================= */
        .nav-bar {
            background: #FFFFFF;
            padding: 1.2rem 3rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .nav-logo {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            color: #0F4C81;
            margin: 0;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-link {
            color: #2C3E50;
            font-weight: 600;
            font-size: 0.95rem;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .nav-link:hover {
            color: #0F4C81;
        }

        /* =============================================
           HERO SECTION
        ============================================= */
        .hero-section {
            background: linear-gradient(135deg, #0F4C81 0%, #16a085 100%);
            padding: 5rem 3rem;
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.05" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,165.3C1248,171,1344,149,1392,138.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
            background-size: cover;
            opacity: 0.3;
        }

        .hero-content {
            position: relative;
            z-index: 1;
            max-width: 900px;
            margin: 0 auto;
        }

        .hero-headline {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            line-height: 1.2;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .hero-subheadline {
            font-size: 1.3rem;
            font-weight: 400;
            margin-bottom: 2.5rem;
            opacity: 0.95;
            line-height: 1.6;
        }

        .cta-button-primary {
            background: #FF6B6B;
            color: white;
            padding: 1rem 3rem;
            font-size: 1.1rem;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .cta-button-primary:hover {
            background: #FF5252;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5);
        }

        /* =============================================
           FEATURES SECTION
        ============================================= */
        .features-section {
            padding: 5rem 3rem;
            background: #F8F9FA;
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            color: #2C3E50;
            margin-bottom: 3rem;
            font-weight: 700;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .feature-card {
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-top: 4px solid #0F4C81;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
        }

        .feature-title {
            font-size: 1.4rem;
            color: #0F4C81;
            margin-bottom: 1rem;
            font-weight: 700;
        }

        .feature-description {
            color: #5A6C7D;
            font-size: 1rem;
            line-height: 1.6;
        }

        /* =============================================
           ASL KEYBOARD STYLES
        ============================================= */
        .asl-keyboard-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin: 2rem auto;
            max-width: 1000px;
        }

        .asl-keyboard-title {
            text-align: center;
            color: #0F4C81;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }

        .asl-keyboard {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.8rem;
            margin: 1.5rem 0;
        }

        .asl-key {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 2px solid #dee2e6;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .asl-key:hover {
            background: linear-gradient(135deg, #0F4C81 0%, #16a085 100%);
            border-color: #0F4C81;
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(15, 76, 129, 0.3);
        }

        .asl-key:hover .key-letter {
            color: white;
        }

        .asl-key:hover .key-emoji {
            transform: scale(1.2);
        }

        .key-emoji {
            font-size: 2.5rem;
            margin-bottom: 0.3rem;
            transition: transform 0.3s ease;
        }

        .key-letter {
            font-size: 1.2rem;
            font-weight: 700;
            color: #0F4C81;
            transition: color 0.3s ease;
        }

        .selected-key-display {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            color: white;
            margin: 2rem 0;
        }

        .selected-key-emoji {
            font-size: 5rem;
            margin-bottom: 1rem;
        }

        .selected-key-letter {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .selected-key-description {
            font-size: 1.2rem;
            opacity: 0.95;
        }

        /* =============================================
           COURSE/STATS CARDS
        ============================================= */
        .courses-section {
            padding: 5rem 3rem;
            background: white;
        }

        .course-card {
            background: white;
            border: 2px solid #E8EEF2;
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }

        .course-card:hover {
            border-color: #0F4C81;
            box-shadow: 0 6px 16px rgba(15, 76, 129, 0.15);
        }

        .stat-card-modern {
            background: white;
            border: 2px solid #E8EEF2;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }

        .stat-card-modern:hover {
            border-color: #0F4C81;
            box-shadow: 0 4px 12px rgba(15, 76, 129, 0.1);
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0F4C81;
            margin: 0.5rem 0;
        }

        .stat-label {
            color: #5A6C7D;
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* =============================================
           BUTTONS
        ============================================= */
        .stButton > button {
            background: #0F4C81;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background: #0D3F6B;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(15, 76, 129, 0.3);
        }

        .btn-primary {
            background: #0F4C81;
            color: white;
            padding: 0.8rem 2rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }

        .btn-primary:hover {
            background: #0D3F6B;
        }

        /* =============================================
           QUIZ CARDS
        ============================================= */
        .quiz-card-pro {
            background: white;
            border: 2px solid #E8EEF2;
            border-left: 6px solid #FF6B6B;
            border-radius: 12px;
            padding: 2rem;
            margin: 1.5rem 0;
        }

        /* =============================================
           GAME CARDS
        ============================================= */
        .game-card-pro {
            background: linear-gradient(135deg, #FFF9F0 0%, #FFF 100%);
            border: 2px solid #FFE5CC;
            border-radius: 12px;
            padding: 2.5rem;
            text-align: center;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }

        .game-card-pro:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.15);
        }

        /* =============================================
           RESPONSIVE
        ============================================= */
        @media (max-width: 968px) {
            .asl-keyboard {
                grid-template-columns: repeat(5, 1fr);
            }
            .features-grid {
                grid-template-columns: 1fr;
            }
            .hero-headline {
                font-size: 2.5rem;
            }
        }
    </style>
    """

st.markdown(get_professional_css(), unsafe_allow_html=True)

# ============================================================
# DATA MANAGEMENT
# ============================================================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def load_json(p, default=None):
    if default is None: default = {}
    try:
        if Path(p).exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return default

def save_json(p, data):
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def initialize():
    if not USERS_FILE.exists():
        save_json(USERS_FILE, {
            "admin": {"password": hash_password("admin123"), "email": "admin@signhub.com", 
                     "created_at": datetime.now().isoformat(), "role": "admin",
                     "preferred_language": "English", "full_name": "Admin User", "country": "USA"},
            "demo": {"password": hash_password("demo123"), "email": "demo@signhub.com",
                    "created_at": datetime.now().isoformat(), "role": "student",
                    "preferred_language": "English", "full_name": "Demo User", "country": "USA"}
        })
    if not PROGRESS_FILE.exists():
        save_json(PROGRESS_FILE, {})

def register_user(username, email, password, full_name, lang, country):
    users = load_json(USERS_FILE, {})
    if username in users:
        return False, "Username already exists"
    if len(password) < 6:
        return False, "Password must be 6+ characters"
    users[username] = {
        "password": hash_password(password), "email": email,
        "created_at": datetime.now().isoformat(), "role": "student",
        "preferred_language": lang, "full_name": full_name, "country": country
    }
    prog = load_json(PROGRESS_FILE, {})
    prog[username] = {"level": 1, "videos": 0, "quizzes_taken": 0, 
                     "quiz_scores": [], "games_played": 0, "total_xp": 0, "streak": 0}
    save_json(USERS_FILE, users)
    save_json(PROGRESS_FILE, prog)
    return True, "Registration successful!"

def login_user(username, password):
    users = load_json(USERS_FILE, {})
    if username not in users:
        return False, "User not found"
    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password"
    return True, "Login successful"

def get_user(username):
    return load_json(USERS_FILE, {}).get(username, {})

def get_progress(username):
    return load_json(PROGRESS_FILE, {}).get(username, {})

def update_progress(username, updates):
    prog = load_json(PROGRESS_FILE, {})
    if username in prog:
        prog[username].update(updates)
        save_json(PROGRESS_FILE, prog)

# ============================================================
# ASL KEYBOARD COMPONENT
# ============================================================
def show_asl_keyboard():
    lang = LANGUAGES[st.session_state.language]

    st.markdown(f"""
    <div class="asl-keyboard-container">
        <h2 class="asl-keyboard-title">🤟 {lang['alphabet_keyboard']}</h2>
        <p style="text-align: center; color: #5A6C7D; margin-bottom: 1.5rem;">
            {lang['click_letter']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'selected_letter' not in st.session_state:
        st.session_state.selected_letter = 'A'

    st.markdown('<div class="asl-keyboard">', unsafe_allow_html=True)
    cols = st.columns(7)
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    for idx, letter in enumerate(letters):
        col_idx = idx % 7
        with cols[col_idx]:
            if st.button(f"{ASL_ALPHABET[letter]}\n{letter}", key=f"key_{letter}", use_container_width=True):
                st.session_state.selected_letter = letter
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    selected = st.session_state.selected_letter
    st.markdown(f"""
    <div class="selected-key-display">
        <div class="selected-key-emoji">{ASL_ALPHABET[selected]}</div>
        <div class="selected-key-letter">Letter: {selected}</div>
        <div class="selected-key-description">{ASL_DESCRIPTIONS[selected]}</div>
    </div>
    """, unsafe_allow_html=True)

# Continue in next part...
print("✅ Part 1: Professional CSS + ASL Keyboard Foundation")

# ============================================================
# LANDING PAGE
# ============================================================
def page_landing():
    lang = LANGUAGES[st.session_state.language]

    # Navigation
    st.markdown(f"""
    <div class="nav-bar">
        <h1 class="nav-logo">🤟 {lang['app_name']}</h1>
        <div class="nav-links">
            <a href="#" class="nav-link">Home</a>
            <a href="#" class="nav-link">Learn</a>
            <a href="#" class="nav-link">Resources</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-headline">{lang['tagline']}</h1>
            <p class="hero-subheadline">{lang['sub_tagline']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ASL KEYBOARD - Main Feature
    show_asl_keyboard()

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🚀 {lang['cta_primary']}", key="cta_main", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "demo"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Features
    st.markdown(f"""
    <div class="features-section">
        <h2 class="section-title">How It Works</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <h3 class="feature-title">{lang['feature1_title']}</h3>
                <p class="feature-description">{lang['feature1_desc']}</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3 class="feature-title">{lang['feature2_title']}</h3>
                <p class="feature-description">{lang['feature2_desc']}</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title">{lang['feature3_title']}</h3>
                <p class="feature-description">{lang['feature3_desc']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Login/Register
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 🔐 {lang['login']}")
        u = st.text_input("Username", key="u")
        p = st.text_input("Password", type="password", key="p")
        if st.button(lang['login'], key="login_btn", use_container_width=True):
            ok, msg = login_user(u, p)
            if ok:
                st.session_state.authenticated = True
                st.session_state.username = u
                st.success("✅ " + msg)
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ " + msg)

    with col2:
        st.markdown(f"### 📝 {lang['register']}")
        ru = st.text_input("Username", key="ru")
        em = st.text_input("Email")
        fn = st.text_input("Full Name")
        rp = st.text_input("Password", type="password", key="rp")
        if st.button(lang['register'], key="reg_btn", use_container_width=True):
            ok, msg = register_user(ru, em, rp, fn, st.session_state.language, "India")
            if ok:
                st.success("✅ " + msg)
            else:
                st.error("❌ " + msg)

# ============================================================
# DASHBOARD PAGE
# ============================================================
def page_dashboard():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)
    lang = LANGUAGES[st.session_state.language]

    st.markdown(f"""
    <div class="hero-section" style="padding: 3rem;">
        <h1 class="hero-headline" style="font-size: 2.5rem;">{lang['welcome']}, {user.get('full_name', u)}!</h1>
        <p class="hero-subheadline">Continue your ASL learning journey</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats Cards
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("📚", "Videos", prog.get('videos', 12), c1),
        ("⭐", "Level", prog.get('level', 1), c2),
        ("🔥", "Streak", f"{prog.get('streak', 5)} days", c3),
        ("✨", "XP", prog.get('total_xp', 250), c4)
    ]

    for icon, label, value, col in stats:
        with col:
            st.markdown(f"""
            <div class="stat-card-modern">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button("📚 Learn", use_container_width=True):
            st.session_state.page = "learning"
            st.rerun()
    with c2:
        if st.button("✍️ Quizzes", use_container_width=True):
            st.session_state.page = "quizzes"
            st.rerun()
    with c3:
        if st.button("🎮 Games", use_container_width=True):
            st.session_state.page = "games"
            st.rerun()
    with c4:
        if st.button("📊 Progress", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔤 Practice ASL Alphabet")
    show_asl_keyboard()

# ============================================================
# LEARNING PAGE
# ============================================================
def page_learning():
    lang = LANGUAGES[st.session_state.language]

    st.markdown(f"""
    <div class="hero-section" style="padding: 3rem;">
        <h1 class="hero-headline" style="font-size: 2.5rem;">📚 Learn ASL Alphabet</h1>
        <p class="hero-subheadline">Master the ASL alphabet with our interactive keyboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    show_asl_keyboard()

    st.markdown("---")
    st.markdown("### 📖 Complete ASL Alphabet Reference")

    cols = st.columns(4)
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    for idx, letter in enumerate(letters):
        col_idx = idx % 4
        with cols[col_idx]:
            st.markdown(f"""
            <div style="background: white; border: 2px solid #E8EEF2; border-radius: 10px; 
                        padding: 1rem; margin: 0.5rem 0; text-align: center;">
                <div style="font-size: 2rem;">{ASL_ALPHABET[letter]}</div>
                <div style="font-weight: 700; color: #0F4C81; font-size: 1.5rem;">{letter}</div>
                <div style="font-size: 0.8rem; color: #5A6C7D;">{ASL_DESCRIPTIONS[letter][:30]}...</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# QUIZZES PAGE
# ============================================================
def page_quizzes():
    st.markdown("""
    <div class="hero-section" style="padding: 3rem;">
        <h1 class="hero-headline" style="font-size: 2.5rem;">✍️ Practice Quizzes</h1>
        <p class="hero-subheadline">Test your ASL knowledge!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔤 Show ASL Alphabet Reference"):
        show_asl_keyboard()

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    if not st.session_state.quiz_started:
        st.markdown("### 📝 Available Quizzes")
        for quiz_name in QUIZZES.keys():
            st.markdown(f"""
            <div class="quiz-card-pro">
                <h3>{quiz_name}</h3>
                <p>🎯 {len(QUIZZES[quiz_name]['questions'])} Questions • 🏆 Earn 50 XP</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Start {quiz_name}", key=f"start_{quiz_name}", use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.quiz_name = quiz_name
                st.session_state.current_question = 0
                st.session_state.quiz_score = 0
                st.rerun()
    else:
        quiz_name = st.session_state.quiz_name
        questions = QUIZZES[quiz_name]['questions']
        current_q = st.session_state.current_question

        if current_q < len(questions):
            progress = (current_q / len(questions)) * 100
            st.progress(progress / 100)
            st.markdown(f"**Question {current_q + 1} of {len(questions)}**")

            question = questions[current_q]
            st.markdown(f"### {question['q']}")

            answer = st.radio("Select your answer:", question['options'], key=f"q_{current_q}")

            if st.button("Submit Answer →", use_container_width=True):
                selected = question['options'].index(answer)
                if selected == question['correct']:
                    st.session_state.quiz_score += 1
                st.session_state.current_question += 1
                st.rerun()
        else:
            score = st.session_state.quiz_score
            total = len(questions)
            percentage = (score / total) * 100

            if percentage >= 80:
                st.balloons()
                st.success(f"🎉 Excellent! {score}/{total} ({percentage:.0f}%) - Earned 50 XP!")
            else:
                st.info(f"😊 Good try! {score}/{total} ({percentage:.0f}%)")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Retake", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.rerun()
            with col2:
                if st.button("🏠 Dashboard", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.session_state.page = "dashboard"
                    st.rerun()

# ============================================================
# GAMES PAGE
# ============================================================
def page_games():
    st.markdown("""
    <div class="hero-section" style="padding: 3rem;">
        <h1 class="hero-headline" style="font-size: 2.5rem;">🎮 Learning Games</h1>
        <p class="hero-subheadline">Make learning fun and interactive!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔤 Show ASL Alphabet Reference"):
        show_asl_keyboard()

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0
    if 'game_round' not in st.session_state:
        st.session_state.game_round = 0

    if not st.session_state.game_started:
        st.markdown("### 🎯 Choose Your Game")
        games = [
            ("🔤 Fingerspelling Challenge", "Spell words using ASL", "fingerspell"),
            ("🃏 Memory Match", "Match letters with signs", "memory"),
            ("⚡ Speed Quiz", "Quick ASL recognition", "speed"),
            ("📖 Story Builder", "Build words with signs", "story")
        ]

        cols = st.columns(2)
        for i, (name, desc, key) in enumerate(games):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="game-card-pro">
                    <h2>{name}</h2>
                    <p>{desc}</p>
                    <p>🏆 Earn 100 XP</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Play", key=f"play_{key}", use_container_width=True):
                    st.session_state.game_started = True
                    st.session_state.game_name = key
                    st.session_state.game_score = 0
                    st.session_state.game_round = 0
                    st.rerun()
    else:
        game_name = st.session_state.game_name

        if game_name == "fingerspell":
            words = ["CAT", "DOG", "HELLO", "THANKS", "FRIEND"]
            if st.session_state.game_round < 5:
                word = random.choice(words)

                st.markdown("### 🔤 Fingerspelling Challenge")
                st.markdown(f"**Spell this word:** {word}")

                sign_display = " ".join([ASL_ALPHABET[letter] for letter in word])
                st.markdown(f"""
                <div class="selected-key-display">
                    <div style="font-size: 4rem;">{sign_display}</div>
                    <div style="font-size: 2rem;">{word}</div>
                </div>
                """, unsafe_allow_html=True)

                user_input = st.text_input("Type the word:", key=f"spell_{st.session_state.game_round}")

                if st.button("Submit", use_container_width=True):
                    if user_input.upper() == word:
                        st.session_state.game_score += 20
                        st.success("✅ Correct! +20 points")
                    else:
                        st.error(f"❌ The word was {word}")
                    st.session_state.game_round += 1
                    time.sleep(1)
                    st.rerun()
            else:
                st.success(f"🎉 Complete! Score: {st.session_state.game_score}/100")
                u = st.session_state.username
                prog = get_progress(u)
                prog['games_played'] = prog.get('games_played', 0) + 1
                prog['total_xp'] = prog.get('total_xp', 0) + 100
                update_progress(u, prog)
                if st.button("Play Again", use_container_width=True):
                    st.session_state.game_started = False
                    st.rerun()

# ============================================================
# PROFILE PAGE
# ============================================================
def page_profile():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)

    st.markdown("""
    <div class="hero-section" style="padding: 3rem;">
        <h1 class="hero-headline" style="font-size: 2.5rem;">👤 Your Profile</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Stats", "⚙️ Settings"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Account Info")
            st.info(f"**Username:** {u}")
            st.info(f"**Name:** {user.get('full_name', 'N/A')}")
        with col2:
            st.markdown("### Learning Stats")
            st.metric("Level", prog.get('level', 1))
            st.metric("Total XP", prog.get('total_xp', 0))

# ============================================================
# PROGRESS PAGE
# ============================================================
def page_progress():
    u = st.session_state.username
    prog = get_progress(u)

    st.markdown("""
    <div class="hero-section" style="padding: 3rem;">
        <h1 class="hero-headline" style="font-size: 2.5rem;">📊 Your Progress</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Level", prog.get('level', 1))
    with c2:
        st.metric("Total XP", prog.get('total_xp', 0))
    with c3:
        st.metric("Quizzes", prog.get('quizzes_taken', 0))
    with c4:
        st.metric("Games", prog.get('games_played', 0))

# ============================================================
# SIDEBAR
# ============================================================
def sidebar():
    with st.sidebar:
        user = get_user(st.session_state.username)
        prog = get_progress(st.session_state.username)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F4C81 0%, #16a085 100%); 
                    padding: 1.5rem; border-radius: 12px; color: white; text-align: center; margin-bottom: 1.5rem;">
            <h2 style="margin: 0;">👤 {user.get('full_name', st.session_state.username)}</h2>
            <p style="margin: 0.5rem 0;">Level {prog.get('level', 1)} • {prog.get('total_xp', 0)} XP</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        pages = {
            "🏠 Dashboard": "dashboard",
            "📚 Learn": "learning",
            "✍️ Quizzes": "quizzes",
            "🎮 Games": "games",
            "📊 Progress": "progress",
            "👤 Profile": "profile"
        }

        for label, page in pages.items():
            if st.button(label, use_container_width=True, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    initialize()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.language = "English"
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    if not st.session_state.authenticated:
        page_landing()
    else:
        sidebar()

        if st.session_state.page == "dashboard":
            page_dashboard()
        elif st.session_state.page == "learning":
            page_learning()
        elif st.session_state.page == "quizzes":
            page_quizzes()
        elif st.session_state.page == "games":
            page_games()
        elif st.session_state.page == "progress":
            page_progress()
        elif st.session_state.page == "profile":
            page_profile()

if __name__ == "__main__":
    main()
