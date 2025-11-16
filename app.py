"""
SignHub - Sign Language Learning Website
Main application file
"""

import streamlit as st
import json
import os
import re
import hashlib
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="SignHub - Learn ASL",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

LANGUAGES = {
    "English": {
        "app_name": "SignHub",
        "tagline": "Learn American Sign Language Interactively",
        "login": "Sign In",
        "register": "Create Account",
        "dashboard": "Dashboard",
        "learning": "Learning Modules",
        "quizzes": "Practice Tests",
        "games": "Gaming Zone",
        "profile": "My Profile",
        "logout": "Logout",
        "welcome": "Welcome back",
        "continue": "Continue Learning",
        "quiz_btn": "Take Quiz",
        "game_btn": "Play Games",
        "progress_btn": "View Progress"
    },
    "हिंदी (Hindi)": {
        "app_name": "साइनहब",
        "tagline": "अमेरिकी सांकेतिक भाषा सीखें",
        "login": "साइन इन करें",
        "register": "खाता बनाएं",
        "dashboard": "डैशबोर्ड",
        "learning": "सीखने के मॉड्यूल",
        "quizzes": "परीक्षा अभ्यास",
        "games": "गेमिंग जोन",
        "profile": "मेरी प्रोफाइल",
        "logout": "लॉगआउट",
        "welcome": "स्वागत है",
        "continue": "सीखना जारी रखें",
        "quiz_btn": "क्विज लें",
        "game_btn": "गेम खेलें",
        "progress_btn": "प्रगति देखें"
    }
}

def get_custom_css():
    return """
    <style>
        .main {
            padding: 2rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .header {
            background: linear-gradient(135deg, #4A90E2 0%, #50E3C2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 6px 12px rgba(74, 144, 226, 0.3);
        }
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        .stat-card h3 {
            margin: 0.5rem 0;
            font-size: 2rem;
            font-weight: bold;
        }
        .stButton > button {
            background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
        }
    </style>
    """

st.markdown(get_custom_css(), unsafe_allow_html=True)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(file_path, default=None):
    if default is None:
        default = {}
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error: {e}")
    return default

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def initialize_data():
    if not USERS_FILE.exists():
        save_json(USERS_FILE, {
            "admin": {
                "password": hash_password("admin123"),
                "email": "admin@signhub.com",
                "created_at": datetime.now().isoformat(),
                "role": "admin",
                "preferred_language": "English",
                "full_name": "Admin User",
                "country": "USA"
            },
            "demo": {
                "password": hash_password("demo123"),
                "email": "demo@signhub.com",
                "created_at": datetime.now().isoformat(),
                "role": "student",
                "preferred_language": "English",
                "full_name": "Demo User",
                "country": "USA"
            }
        })
    if not PROGRESS_FILE.exists():
        save_json(PROGRESS_FILE, {})

def register_user(username, email, password, full_name, lang, country):
    users = load_json(USERS_FILE, {})
    if username in users:
        return False, "Username already exists"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email"
    if len(password) < 6:
        return False, "Password must be 6+ characters"
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "created_at": datetime.now().isoformat(),
        "role": "student",
        "preferred_language": lang,
        "full_name": full_name,
        "country": country
    }
    prog = load_json(PROGRESS_FILE, {})
    prog[username] = {"current_level": 1, "completed_videos": [], "quiz_scores": [], "total_xp": 0, "streak": 0}
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

def update_user(username, updates):
    users = load_json(USERS_FILE, {})
    if username in users:
        users[username].update(updates)
        save_json(USERS_FILE, users)
        return True
    return False

def page_login():
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown("### 🌐 Language")
    with c2:
        st.session_state.language = st.selectbox(
            "Select",
            list(LANGUAGES.keys()),
            label_visibility="collapsed"
        )
    st.markdown("---")
    lang = LANGUAGES[st.session_state.language]
    a, b = st.columns(2)
    with a:
        st.markdown(f"""<div class="header"><h1>{lang['app_name']}</h1><p>{lang['tagline']}</p></div>""", unsafe_allow_html=True)
        st.markdown("- Connect with Deaf community\n- Grow skills\n- Career opportunities")
    with b:
        t1, t2 = st.tabs([f"🔐 {lang['login']}", f"📝 {lang['register']}"])
        with t1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button(lang['login'], use_container_width=True):
                ok, msg = login_user(u, p)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.username = u
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with t2:
            ru = st.text_input("Username", key="ru")
            em = st.text_input("Email")
            fn = st.text_input("Full Name")
            c3, c4 = st.columns(2)
            with c3:
                country = st.text_input("Country", value="India")
            with c4:
                pl = st.selectbox("Language", list(LANGUAGES.keys()))
            rp = st.text_input("Password", type="password", key="rp")
            rc = st.text_input("Confirm Password", type="password")
            if st.button(lang['register'], use_container_width=True):
                if rp != rc:
                    st.error("Passwords do not match")
                else:
                    ok, msg = register_user(ru, em, rp, fn, pl, country)
                    st.success(msg) if ok else st.error(msg)

def page_dashboard():
    u = st.session_state.username
    user = get_user(u)
    lang = LANGUAGES[st.session_state.language]
    st.markdown(f"""<div class="header"><h1>👋 {lang['welcome']}, {user.get('full_name', u)}!</h1></div>""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for html, col in [
        ('<div class="stat-card"><p>📚 Videos</p><h3>12</h3></div>', c1),
        ('<div class="stat-card"><p>⭐ Level</p><h3>1</h3></div>', c2),
        ('<div class="stat-card"><p>🔥 Streak</p><h3>5</h3></div>', c3),
        ('<div class="stat-card"><p>✨ XP</p><h3>250</h3></div>', c4)
    ]:
        with col:
            st.markdown(html, unsafe_allow_html=True)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button(lang['continue'], use_container_width=True):
        st.session_state.page = "learning"
        st.rerun()
    if c2.button(lang['quiz_btn'], use_container_width=True):
        st.session_state.page = "quizzes"
        st.rerun()
    if c3.button(lang['game_btn'], use_container_width=True):
        st.session_state.page = "games"
        st.rerun()
    if c4.button(lang['progress_btn'], use_container_width=True):
        st.session_state.page = "progress"
        st.rerun()

def page_profile():
    u = st.session_state.username
    user = get_user(u)
    lang = LANGUAGES[st.session_state.language]
    st.markdown(f"""<div class="header"><h1>👤 {lang['profile']}</h1></div>""", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Info", "Edit"])
    with t1:
        st.markdown(f"**Username:** {u}")
        st.markdown(f"**Email:** {user.get('email', 'N/A')}")
        st.markdown(f"**Language:** {user.get('preferred_language', 'English')}")
    with t2:
        with st.form("edit"):
            name = st.text_input("Name", user.get('full_name', ''))
            email = st.text_input("Email", user.get('email', ''))
            new_lang = st.selectbox("Language", list(LANGUAGES.keys()))
            if st.form_submit_button("Save"):
                update_user(u, {"full_name": name, "email": email, "preferred_language": new_lang})
                st.session_state.language = new_lang
                st.success("Updated!")
                st.rerun()

def page_learning():
    lang = LANGUAGES[st.session_state.language]
    st.markdown(f"""<div class="header"><h1>📚 {lang['learning']}</h1></div>""", unsafe_allow_html=True)
    for section in ["ASL Alphabet", "Numbers 1-20", "Greetings"]:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{section}**")
        if c2.button("Watch", key=section):
            st.markdown("[Learn How to Sign](https://www.youtube.com/@LearnHowtoSign)")

def page_quizzes():
    lang = LANGUAGES[st.session_state.language]
    st.markdown(f"""<div class="header"><h1>✍️ {lang['quizzes']}</h1></div>""", unsafe_allow_html=True)
    for quiz in ["Alphabet Quiz", "Greetings Quiz"]:
        if st.button(quiz, use_container_width=True):
            st.success("Quiz started!")

def page_games():
    st.markdown("""<div class="header"><h1>🎮 Gaming Zone</h1></div>""", unsafe_allow_html=True)
    for game in ["🔤 Fingerspelling", "🃏 Memory Match"]:
        if st.button(game, use_container_width=True):
            st.info(f"Starting {game}...")

def page_progress():
    st.markdown("""<div class="header"><h1>📊 Progress</h1></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Videos", 12)
    c2.metric("Quizzes", 3)
    c3.metric("Level", 1)

def sidebar():
    with st.sidebar:
        user = get_user(st.session_state.username)
        st.markdown(f"### 👤 {user.get('full_name', st.session_state.username)}")
        st.markdown(f"🌐 {st.session_state.language}")
        st.markdown("---")
        pages = {"🏠 Dashboard": "dashboard", "📚 Learning": "learning", "✍️ Quizzes": "quizzes", "🎮 Games": "games", "📊 Progress": "progress", "👤 Profile": "profile"}
        for label, page in pages.items():
            if st.button(label, use_container_width=True, key=f"n_{page}"):
                st.session_state.page = page
                st.rerun()
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

def main():
    initialize_data()
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.language = "English"
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if not st.session_state.authenticated:
        page_login()
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
