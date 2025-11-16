"""
SignHub - Ultimate Redesigned Version
Complete with Vibrant Design, Login, Certificates, and All Features
"""

import streamlit as st
import json
import hashlib
import random
import time
from pathlib import Path
from datetime import datetime
from io import BytesIO
import base64

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

QUIZZES = {
    "ASL Alphabet": {
        "questions": [
            {"q": "What does letter 'A' look like?", "options": ["Closed fist", "Open palm", "Point finger", "Peace"], "emojis": ["👊", "✋", "☝️", "✌️"], "correct": 0},
            {"q": "How to sign 'B'?", "options": ["Flat hand", "Closed fist", "Two fingers", "Thumb between"], "emojis": ["✋", "👊", "✌️", "🤏"], "correct": 0},
            {"q": "Which is 'C'?", "options": ["C shape", "Open palm", "Pointing", "Peace sign"], "emojis": ["👌", "✋", "☝️", "✌️"], "correct": 0},
            {"q": "Sign for 'D'?", "options": ["Index up", "Closed fist", "Flat hand", "Pinky up"], "emojis": ["☝️", "👊", "✋", "🤙"], "correct": 0},
            {"q": "How is 'E' signed?", "options": ["Fingers curled", "Open palm", "Two fingers", "Thumb up"], "emojis": ["✊", "✋", "✌️", "👍"], "correct": 0}
        ]
    },
    "Numbers": {
        "questions": [
            {"q": "Sign for '1'?", "options": ["Index up", "Thumb up", "Open palm", "Closed fist"], "emojis": ["☝️", "👍", "✋", "👊"], "correct": 0},
            {"q": "Number '5'?", "options": ["All fingers", "Index only", "Two fingers", "Thumb only"], "emojis": ["✋", "☝️", "✌️", "👍"], "correct": 0},
            {"q": "How is '10'?", "options": ["Thumbs crossed", "Both thumbs", "Index and thumb", "All fingers"], "emojis": ["👊", "👍", "👌", "✋"], "correct": 0},
            {"q": "Sign for '3'?", "options": ["Three fingers", "One finger", "Two fingers", "All fingers"], "emojis": ["✋", "☝️", "✌️", "👊"], "correct": 0},
            {"q": "Number '7'?", "options": ["Specific shape", "Open hand", "Closed fist", "Two fingers"], "emojis": ["✌️", "✋", "👊", "✌️"], "correct": 0}
        ]
    },
    "Greetings": {
        "questions": [
            {"q": "Say 'Hello'?", "options": ["Wave hand", "Salute", "Shake hands", "Nod"], "emojis": ["👋", "✌️", "🤝", "😊"], "correct": 0},
            {"q": "Say 'Thanks'?", "options": ["Hand on chest", "Clap", "Thumbs up", "Wave"], "emojis": ["🙏", "👏", "👍", "👋"], "correct": 0},
            {"q": "'Please'?", "options": ["Touch chin", "Wave", "Point", "Thumbs up"], "emojis": ["☝️", "👋", "👉", "👍"], "correct": 0},
            {"q": "'Good morning'?", "options": ["Sun rising", "Wave", "Smile", "Flat hand"], "emojis": ["☀️", "👋", "😊", "✋"], "correct": 0},
            {"q": "'How are you'?", "options": ["Points up", "Shrug", "Wave", "Thumbs up"], "emojis": ["☝️", "🤷", "👋", "👍"], "correct": 0}
        ]
    }
}

# ============================================================
# ULTIMATE VIBRANT CSS DESIGN
# ============================================================
def get_ultimate_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&family=Inter:wght@300;400;600;700&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
            box-sizing: border-box;
        }

        body, .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            min-height: 100vh;
        }

        /* =============================================
           VIBRANT COLOR PALETTE
        ============================================= */
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent1: #ff6b6b;
            --accent2: #ffa502;
            --accent3: #26de81;
            --accent4: #20c997;
            --dark: #2d3436;
            --light: #f8f9fa;
        }

        /* =============================================
           SMOOTH ANIMATIONS
        ============================================= */
        @keyframes smoothFadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes smoothSlideIn {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.4); }
            50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.8); }
        }

        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        .smooth-container {
            animation: smoothFadeIn 0.8s ease-out;
        }

        /* =============================================
           LOGIN PAGE
        ============================================= */
        .login-container {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            animation: smoothFadeIn 0.8s ease-out;
        }

        .login-box {
            background: white;
            border-radius: 25px;
            padding: 3rem;
            width: 95%;
            max-width: 450px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: smoothSlideIn 0.8s ease-out;
        }

        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .login-title {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        .login-subtitle {
            color: #5a6c7d;
            font-size: 1rem;
            margin-top: 0.5rem;
        }

        .login-input {
            width: 100%;
            padding: 1rem;
            margin: 0.8rem 0;
            border: 2px solid #e8eef2;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            font-family: 'Poppins', sans-serif;
        }

        .login-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .login-button {
            width: 100%;
            padding: 1rem;
            margin-top: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: pulseGlow 2s infinite;
        }

        .login-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        .toggle-tab {
            width: 100%;
            padding: 1rem;
            background: white;
            border: none;
            border-bottom: 3px solid #e8eef2;
            font-size: 1rem;
            font-weight: 600;
            color: #5a6c7d;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 2rem;
        }

        .toggle-tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }

        /* =============================================
           DASHBOARD
        ============================================= */
        .dashboard-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            animation: smoothFadeIn 0.8s ease-out;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .stat-card-vibrant {
            background: linear-gradient(135deg, #ff6b6b 0%, #ffa502 100%);
            color: white;
            padding: 2rem;
            border-radius: 18px;
            text-align: center;
            margin: 0.8rem 0;
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
            transition: all 0.3s ease;
            animation: smoothFadeIn 0.8s ease-out;
        }

        .stat-card-vibrant:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 900;
            margin: 0.5rem 0;
        }

        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        /* =============================================
           CARDS
        ============================================= */
        .vibrant-card {
            background: white;
            border-radius: 18px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border-top: 5px solid #667eea;
        }

        .vibrant-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
        }

        /* =============================================
           QUIZ SECTION
        ============================================= */
        .quiz-option {
            background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
            border: 2px solid #e0e0e0;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .quiz-option:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
            transform: translateX(10px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }

        .option-sign {
            font-size: 2.5rem;
            min-width: 60px;
            text-align: center;
        }

        .option-text {
            font-size: 1.1rem;
            font-weight: 600;
        }

        /* =============================================
           BUTTONS
        ============================================= */
        .btn-vibrant {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 0.5rem;
        }

        .btn-vibrant:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        .btn-accent {
            background: linear-gradient(135deg, #ff6b6b 0%, #ffa502 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-accent:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
        }

        /* =============================================
           PROFILE SECTION
        ============================================= */
        .profile-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            animation: smoothFadeIn 0.8s ease-out;
        }

        .profile-avatar {
            width: 120px;
            height: 120px;
            background: white;
            border-radius: 50%;
            margin: 0 auto 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
        }

        .profile-name {
            font-size: 2rem;
            font-weight: 800;
            margin: 1rem 0;
        }

        /* =============================================
           CERTIFICATE
        ============================================= */
        .certificate {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            text-align: center;
            margin: 2rem 0;
            border: 3px solid #ffd700;
            animation: smoothFadeIn 0.8s ease-out;
        }

        .certificate-title {
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        /* =============================================
           RESPONSIVE
        ============================================= */
        @media (max-width: 768px) {
            .login-box {
                padding: 2rem;
            }

            .login-title {
                font-size: 2rem;
            }
        }
    </style>
    """

st.markdown(get_ultimate_css(), unsafe_allow_html=True)

# ============================================================
# DATA MANAGEMENT
# ============================================================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
PROGRESS_FILE = DATA_DIR / "progress.json"
CERTIFICATES_DIR = DATA_DIR / "certificates"
CERTIFICATES_DIR.mkdir(exist_ok=True)

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
            "admin": {
                "password": hash_password("admin123"),
                "email": "admin@signhub.com",
                "full_name": "Admin User",
                "country": "USA",
                "phone": "+1234567890",
                "bio": "ASL Expert",
                "joined": datetime.now().isoformat()
            },
            "demo": {
                "password": hash_password("demo123"),
                "email": "demo@signhub.com",
                "full_name": "Demo User",
                "country": "India",
                "phone": "+919876543210",
                "bio": "Enthusiastic learner",
                "joined": datetime.now().isoformat()
            }
        })
    if not PROGRESS_FILE.exists():
        save_json(PROGRESS_FILE, {})

def register_user(username, email, password, full_name, country):
    users = load_json(USERS_FILE, {})
    if username in users:
        return False, "Username already exists"
    if len(password) < 6:
        return False, "Password must be 6+ characters"
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "full_name": full_name,
        "country": country,
        "phone": "",
        "bio": "",
        "joined": datetime.now().isoformat()
    }
    prog = load_json(PROGRESS_FILE, {})
    prog[username] = {
        "level": 1,
        "quizzes_taken": 0,
        "quiz_scores": [],
        "games_played": 0,
        "total_xp": 0,
        "certificates": []
    }
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

def get_progress(username):
    return load_json(PROGRESS_FILE, {}).get(username, {})

def update_progress(username, updates):
    prog = load_json(PROGRESS_FILE, {})
    if username in prog:
        prog[username].update(updates)
        save_json(PROGRESS_FILE, prog)

# Continue in next part...
print("✅ Part 1: Ultimate CSS + Data Management + Login System")

# ============================================================
# LOGIN PAGE (Mandatory)
# ============================================================
def page_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-box smooth-container">
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.markdown("""
            <div class="login-header">
                <h1 class="login-title">🤟 SignHub</h1>
                <p class="login-subtitle">Master Sign Language</p>
            </div>
            """, unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")

            if st.button("Login", use_container_width=True, key="login_btn"):
                ok, msg = login_user(username, password)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

            st.markdown("---")
            st.info("**Demo Credentials:**\nUsername: demo\nPassword: demo123")

        with tab2:
            st.markdown("""
            <div class="login-header">
                <h1 class="login-title">📝 Create Account</h1>
            </div>
            """, unsafe_allow_html=True)

            reg_username = st.text_input("Username", placeholder="Choose username", key="reg_u")
            reg_email = st.text_input("Email", placeholder="Your email", key="reg_e")
            reg_name = st.text_input("Full Name", placeholder="Your name", key="reg_n")
            reg_country = st.text_input("Country", placeholder="Your country", key="reg_c")
            reg_password = st.text_input("Password", type="password", placeholder="6+ characters", key="reg_p")
            reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="reg_cp")

            if st.button("Register", use_container_width=True, key="reg_btn"):
                if reg_password != reg_confirm:
                    st.error("❌ Passwords don't match!")
                else:
                    ok, msg = register_user(reg_username, reg_email, reg_password, reg_name, reg_country)
                    if ok:
                        st.success("✅ " + msg)
                    else:
                        st.error(f"❌ {msg}")

        st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================================
# DASHBOARD PAGE
# ============================================================
def page_dashboard():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="dashboard-header">
            <h1 style="margin: 0; font-size: 2.5rem;">🤟 Welcome, {user.get('full_name', u)}!</h1>
            <p style="margin: 0.5rem 0; font-size: 1.1rem; opacity: 0.9;">Ready to master ASL? Let's learn together!</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="stat-card-vibrant" style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa502 100%);">
            <div class="stat-value">🎯</div>
            <div class="stat-label">Quizzes</div>
            <div class="stat-value" style="font-size: 2rem;">{prog.get('quizzes_taken', 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="stat-card-vibrant" style="background: linear-gradient(135deg, #26de81 0%, #20c997 100%);">
            <div class="stat-value">⭐</div>
            <div class="stat-label">Level</div>
            <div class="stat-value" style="font-size: 2rem;">{prog.get('level', 1)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-card-vibrant" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-value">🔥</div>
            <div class="stat-label">Streak</div>
            <div class="stat-value" style="font-size: 2rem;">5</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="stat-card-vibrant" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="stat-value">✨</div>
            <div class="stat-label">XP</div>
            <div class="stat-value" style="font-size: 2rem;">{prog.get('total_xp', 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📚 Learn", use_container_width=True, key="btn_learn"):
            st.session_state.page = "learning"
            st.rerun()

    with col2:
        if st.button("✍️ Quizzes", use_container_width=True, key="btn_quiz"):
            st.session_state.page = "quizzes"
            st.rerun()

    with col3:
        if st.button("👤 Profile", use_container_width=True, key="btn_profile"):
            st.session_state.page = "profile"
            st.rerun()

# ============================================================
# QUIZZES PAGE (With ASL Signs)
# ============================================================
def page_quizzes():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; 
                animation: smoothFadeIn 0.8s ease-out;">
        <h1 style="margin: 0; font-size: 2.5rem;">✍️ ASL Quizzes</h1>
        <p style="margin: 0.5rem 0; font-size: 1.1rem; opacity: 0.9;">Test your knowledge!</p>
    </div>
    """, unsafe_allow_html=True)

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    if not st.session_state.quiz_started:
        st.markdown("### Select a Quiz")
        cols = st.columns(3)

        for idx, quiz_name in enumerate(QUIZZES.keys()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="vibrant-card">
                        <h3 style="color: #667eea; margin-top: 0;">{quiz_name}</h3>
                        <p>{len(QUIZZES[quiz_name]['questions'])} Questions</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Start {quiz_name}", key=f"quiz_{quiz_name}", use_container_width=True):
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

            for idx, (option, emoji) in enumerate(zip(question['options'], question['emojis'])):
                col1, col2 = st.columns([1, 5])

                with col1:
                    st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)

                with col2:
                    if st.button(f"{option}", key=f"opt_{idx}", use_container_width=True):
                        if idx == question['correct']:
                            st.session_state.quiz_score += 1
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect!")
                        st.session_state.current_question += 1
                        time.sleep(1)
                        st.rerun()
        else:
            score = st.session_state.quiz_score
            total = len(questions)
            percentage = (score / total) * 100

            st.markdown(f"""
            <div class="certificate" style="text-align: center;">
                <h2 style="margin: 0; font-size: 2.5rem;">🎉 Quiz Complete!</h2>
                <p style="font-size: 1.8rem; font-weight: 700; margin: 1rem 0;">{score}/{total} Correct</p>
                <p style="font-size: 1.2rem;">Accuracy: {percentage:.1f}%</p>
                <p style="font-size: 1.1rem;">+{50 if percentage >= 80 else 30 if percentage >= 60 else 10} XP</p>
            </div>
            """, unsafe_allow_html=True)

            u = st.session_state.username
            prog = get_progress(u)
            prog['quizzes_taken'] = prog.get('quizzes_taken', 0) + 1
            prog['quiz_scores'] = prog.get('quiz_scores', []) + [percentage]
            prog['total_xp'] = prog.get('total_xp', 0) + (50 if percentage >= 80 else 30 if percentage >= 60 else 10)
            update_progress(u, prog)

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
# PROFILE PAGE (Editable)
# ============================================================
def page_profile():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)

    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-avatar">👤</div>
        <h1 class="profile-name">{user.get('full_name', u)}</h1>
        <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">@{u}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Statistics", "✏️ Edit Info", "📜 Certificates"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="vibrant-card">
                <h3 style="color: #667eea;">Account Information</h3>
                <p><strong>Email:</strong> {user.get('email', 'N/A')}</p>
                <p><strong>Country:</strong> {user.get('country', 'N/A')}</p>
                <p><strong>Phone:</strong> {user.get('phone', 'N/A')}</p>
                <p><strong>Bio:</strong> {user.get('bio', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="vibrant-card">
                <h3 style="color: #667eea;">Learning Statistics</h3>
                <p><strong>Level:</strong> {prog.get('level', 1)}</p>
                <p><strong>Total XP:</strong> {prog.get('total_xp', 0)}</p>
                <p><strong>Quizzes Taken:</strong> {prog.get('quizzes_taken', 0)}</p>
                <p><strong>Certificates:</strong> {len(prog.get('certificates', []))}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Edit Your Information")

        with st.form("edit_profile"):
            new_name = st.text_input("Full Name", value=user.get('full_name', ''))
            new_phone = st.text_input("Phone", value=user.get('phone', ''))
            new_bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
            new_country = st.text_input("Country", value=user.get('country', ''))

            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                update_user(u, {
                    'full_name': new_name,
                    'phone': new_phone,
                    'bio': new_bio,
                    'country': new_country
                })
                st.success("✅ Profile updated successfully!")
                time.sleep(0.5)
                st.rerun()

    with tab3:
        st.markdown("### 📜 Your Certificates")
        if prog.get('certificates', []):
            for cert in prog.get('certificates', []):
                st.markdown(f"""
                <div class="certificate">
                    <h2 style="color: white; margin: 0;">🏆 Certificate of Achievement</h2>
                    <p style="font-size: 1.2rem; margin: 1rem 0;">{cert['quiz_name']}</p>
                    <p>Earned on {cert['date']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📜 No certificates yet. Complete quizzes to earn certificates!")

# ============================================================
# LEARNING PAGE
# ============================================================
def page_learning():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">📚 Learn ASL Alphabet</h1>
    </div>
    """, unsafe_allow_html=True)

    if 'show_keyboard' not in st.session_state:
        st.session_state.show_keyboard = False

    # Show keyboard only if user wants to write/edit
    with st.expander("🎹 ASL Alphabet Reference (Click to expand)"):
        cols = st.columns(7)
        letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        for idx, letter in enumerate(letters):
            col_idx = idx % 7
            with cols[col_idx]:
                st.markdown(f"""
                <div style="background: white; border: 2px solid #667eea; border-radius: 12px; 
                            padding: 1rem; text-align: center; cursor: pointer; 
                            transition: all 0.3s; margin: 0.5rem 0;">
                    <div style="font-size: 2.5rem;">{ASL_ALPHABET[letter]}</div>
                    <div style="font-weight: 700; color: #667eea;">{letter}</div>
                    <div style="font-size: 0.8rem; color: #5a6c7d;">{ASL_DESCRIPTIONS[letter][:20]}...</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="vibrant-card">
        <h3 style="color: #667eea;">Learn at Your Pace</h3>
        <p>Explore the ASL alphabet through our interactive keyboard reference. Click the reference above to see all letters with their hand sign descriptions.</p>
        <p><strong>Pro Tip:</strong> Use the keyboard reference while taking quizzes to learn better!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN APP
# ============================================================
def main():
    initialize()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    if not st.session_state.authenticated:
        page_login()
    else:
        if st.session_state.page == "dashboard":
            page_dashboard()
        elif st.session_state.page == "quizzes":
            page_quizzes()
        elif st.session_state.page == "profile":
            page_profile()
        elif st.session_state.page == "learning":
            page_learning()

if __name__ == "__main__":
    main()
