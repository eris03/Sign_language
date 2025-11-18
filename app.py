"""
SignHub - Ultimate Version with Beautiful Login Design
All 8 Corrections + Stunning React-Style Login/Register
"""

import streamlit as st
import json
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
# BEAUTIFUL REACT-STYLE CSS + ALL ANIMATIONS
# ============================================================
def get_beautiful_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
            box-sizing: border-box;
        }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .main {
            background: #f0f4f1 !important;
            padding: 0 !important;
        }

        /* =============================================
           BEAUTIFUL LOGIN/REGISTER CONTAINER
        ============================================= */
        .login-main-container {
            display: flex;
            width: 900px;
            max-width: 95%;
            height: 550px;
            margin: 50px auto;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            overflow: hidden;
            background: #2E7867;
            animation: slideIn 0.8s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Welcome Side with SVG Background */
        .welcome-side {
            flex: 1;
            position: relative;
            padding: 40px 30px;
            background: linear-gradient(135deg, #2E7867 0%, #3a9178 100%);
            clip-path: ellipse(70% 100% at 0 50%);
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: space-between;
            box-shadow: inset 10px 0 20px rgba(0,0,0,0.15);
        }

        .welcome-text {
            font-size: 3.5rem;
            font-weight: 900;
            letter-spacing: 5px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }

        .welcome-illustration {
            width: 100%;
            height: 250px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 350"><defs><linearGradient id="g1" x1="0" x2="0" y1="1" y2="0"><stop offset="0%25" stop-color="%232a6f64"/><stop offset="100%25" stop-color="%2397bb72"/></linearGradient></defs><rect width="400" height="350" fill="url(%23g1)" rx="20"/><circle cx="320" cy="90" r="25" fill="%23fff" opacity="0.7"/><circle cx="280" cy="120" r="35" fill="%23e8f0de"/><rect x="170" y="150" width="70" height="40" fill="%23e6daca" rx="5"/><rect x="230" y="180" width="70" height="40" fill="%23c8d6c2" rx="5"/><polygon points="60,270 75,250 95,270 75,300" fill="%231f3a33"/><polygon points="90,280 100,260 115,280" fill="%231f3a33"/></svg>') center/contain no-repeat;
            margin-top: auto;
        }

        /* Form Container */
        .form-side {
            flex: 1.3;
            padding: 50px 45px;
            background: #2E7867;
            display: flex;
            flex-direction: column;
            color: white;
            overflow-y: auto;
        }

        .form-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 30px;
            line-height: 1.4;
        }

        /* Social Buttons */
        .social-buttons {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .social-btn {
            flex: 1;
            min-width: 140px;
            border: none;
            border-radius: 20px;
            padding: 10px 15px;
            font-weight: 600;
            font-size: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            gap: 8px;
        }

        .social-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .google-btn {
            background: #e8f0fe;
            color: #4285f4;
        }

        .facebook-btn {
            background: #3b5998;
            color: white;
        }

        .twitter-btn {
            background: #1da1f2;
            color: white;
        }

        /* OR Divider */
        .or-divider {
            display: flex;
            align-items: center;
            margin: 25px 0;
            gap: 15px;
            color: #aad5bd;
        }

        .or-divider span {
            flex: 1;
            height: 2px;
            background: #aad5bd;
            border-radius: 2px;
        }

        /* Input Fields */
        .field-row {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }

        .field {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .field label {
            font-weight: 500;
            font-size: 13px;
            margin-bottom: 8px;
            color: #aad5bd;
        }

        .field input {
            padding: 12px 16px;
            border-radius: 20px;
            border: 2px solid #aad5bd;
            background: transparent;
            color: white;
            font-weight: 500;
            outline: none;
            transition: all 0.3s ease;
            font-size: 14px;
        }

        .field input::placeholder {
            color: #88c0a0;
        }

        .field input:focus {
            border-color: #98c9a3;
            box-shadow: 0 0 0 3px rgba(168, 213, 186, 0.1);
        }

        /* Terms Checkbox */
        .terms-box {
            margin: 20px 0;
            font-size: 13px;
            color: #aad5bd;
        }

        .terms-box label {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }

        .terms-box input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }

        .terms-box a {
            color: #98c9a3;
            text-decoration: none;
            font-weight: 600;
        }

        .terms-box a:hover {
            text-decoration: underline;
        }

        /* Primary Button */
        .primary-btn {
            background: #a8d5ba;
            color: #2E7867;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            padding: 14px 0;
            width: 100%;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 6px 15px rgba(158, 208, 186, 0.4);
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        .primary-btn:hover {
            background: #99bfaa;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(158, 208, 186, 0.5);
        }

        /* Toggle Link */
        .toggle-link {
            text-align: center;
            margin-top: 25px;
            font-size: 14px;
            color: #aad5bd;
        }

        .toggle-link button {
            background: none;
            border: none;
            color: #a8d5ba;
            text-decoration: underline;
            cursor: pointer;
            font-weight: 700;
            padding: 0;
            margin-left: 5px;
            font-size: 14px;
        }

        .toggle-link button:hover {
            color: #98c9a3;
        }

        /* =============================================
           DASHBOARD & OTHER PAGES
        ============================================= */
        .dashboard-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .stat-card-vibrant {
            background: linear-gradient(135deg, #ff6b6b 0%, #ffa502 100%);
            color: white;
            padding: 2rem;
            border-radius: 18px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
            transition: all 0.3s ease;
            animation: fadeIn 0.8s ease-out;
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
            opacity: 0.95;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        /* Quiz Cards */
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

        /* Quiz Options with ASL Signs */
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
            gap: 1.5rem;
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

        /* Profile Card */
        .profile-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            animation: fadeIn 0.8s ease-out;
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
            font-size: 3.5rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        .profile-name {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 1rem 0;
        }

        /* Certificate */
        .certificate {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            text-align: center;
            margin: 2rem 0;
            border: 4px solid #ffd700;
            box-shadow: 0 15px 35px rgba(245, 87, 108, 0.3);
            animation: fadeIn 0.8s ease-out;
        }

        .certificate-title {
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        /* Responsive */
        @media (max-width: 900px) {
            .login-main-container {
                flex-direction: column;
                height: auto;
                margin: 20px auto;
            }

            .welcome-side {
                clip-path: none;
                height: 200px;
            }

            .form-side {
                padding: 30px 25px;
            }

            .field-row {
                flex-direction: column;
            }

            .social-buttons {
                flex-direction: column;
            }
        }
    </style>
    """

st.markdown(get_beautiful_css(), unsafe_allow_html=True)

# Continue in next part...
print("✅ Part 1: Beautiful React-Style CSS + Data Setup")

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

def register_user(name, email, password, password2):
    if password != password2:
        return False, "Passwords do not match"
    if len(password) < 6:
        return False, "Password must be 6+ characters"

    users = load_json(USERS_FILE, {})

    # Check if email already exists
    for username, data in users.items():
        if data.get('email') == email:
            return False, "Email already registered"

    # Generate username from email
    username = email.split('@')[0].lower()
    counter = 1
    original_username = username
    while username in users:
        username = f"{original_username}{counter}"
        counter += 1

    users[username] = {
        "password": hash_password(password),
        "email": email,
        "full_name": name,
        "country": "",
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
    return True, f"Registration successful! Your username is: {username}"

def login_user(email, password):
    users = load_json(USERS_FILE, {})

    # Find user by email
    username = None
    for uname, data in users.items():
        if data.get('email') == email:
            username = uname
            break

    if not username:
        return False, None, "User not found"

    if users[username]["password"] != hash_password(password):
        return False, None, "Incorrect password"

    return True, username, "Login successful"

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

# ============================================================
# BEAUTIFUL LOGIN/REGISTER PAGE
# ============================================================
def page_login():
    """Beautiful React-style login and register page"""

    # Initialize session state for tab
    if 'login_tab' not in st.session_state:
        st.session_state.login_tab = 'login'  # 'login' or 'register'

    st.markdown("""
    <div class="login-main-container">
        <!-- Welcome Side -->
        <div class="welcome-side">
            <div class="welcome-text">WELCOME</div>
            <div class="welcome-illustration"></div>
        </div>

        <!-- Form Side -->
        <div class="form-side">
    """, unsafe_allow_html=True)

    # Tab buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="tab_login", use_container_width=True):
            st.session_state.login_tab = 'login'
            st.rerun()
    with col2:
        if st.button("Sign Up", key="tab_register", use_container_width=True):
            st.session_state.login_tab = 'register'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.login_tab == 'login':
        # LOGIN FORM
        st.markdown("""
        <div class="form-title">
            Welcome Back!<br>
            Please login to your account
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("Log In", use_container_width=True)

            if submit:
                ok, username, msg = login_user(email, password)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ " + msg)
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ " + msg)

        st.markdown("""
        <div class="toggle-link">
            Don't have an account? Click "Sign Up" above
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("**Demo Login:**\nEmail: demo@signhub.com\nPassword: demo123")

    else:
        # REGISTER FORM
        st.markdown("""
        <div class="form-title">
            Hello!<br>
            We are glad to see you :)
        </div>
        """, unsafe_allow_html=True)

        # Social buttons (decorative - not functional in this demo)
        st.markdown("""
        <div class="social-buttons">
            <button class="social-btn google-btn">
                <span style="font-weight:900;">G</span> Sign up with Google
            </button>
            <button class="social-btn facebook-btn">
                <span style="font-weight:900;">f</span> Sign up with Facebook
            </button>
            <button class="social-btn twitter-btn">
                <span style="font-weight:900;">t</span> Sign up with Twitter
            </button>
        </div>

        <div class="or-divider">
            <span></span>
            <small>Or</small>
            <span></span>
        </div>
        """, unsafe_allow_html=True)

        with st.form("register_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name", placeholder="Your full name")
            with col2:
                email = st.text_input("Email Address", placeholder="Your email")

            col3, col4 = st.columns(2)
            with col3:
                password = st.text_input("Password", type="password", placeholder="Create password (6+ chars)")
            with col4:
                password2 = st.text_input("Repeat Password", type="password", placeholder="Confirm password")

            agreed = st.checkbox("I agree to Terms of Service and Privacy Policy")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("Sign Up", use_container_width=True)

            if submit:
                if not agreed:
                    st.error("❌ You must agree to the Terms of Service and Privacy Policy")
                else:
                    ok, msg = register_user(name, email, password, password2)
                    if ok:
                        st.success("✅ " + msg)
                        st.info("Now you can login with your email and password!")
                    else:
                        st.error("❌ " + msg)

        st.markdown("""
        <div class="toggle-link">
            Already have an account? Click "Login" above
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# Continue to dashboard and other pages...
print("✅ Part 2: Data Management + Beautiful Login/Register Page")

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

    # Stats Cards
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

    # Quick Actions
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
                animation: fadeIn 0.8s ease-out;">
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
                        <p style="color: #5a6c7d;">{len(QUIZZES[quiz_name]['questions'])} Questions • Earn XP</p>
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
            st.markdown("<br>", unsafe_allow_html=True)

            question = questions[current_q]
            st.markdown(f"### {question['q']}")
            st.markdown("<br>", unsafe_allow_html=True)

            # Display options with ASL signs
            for idx, (option, emoji) in enumerate(zip(question['options'], question['emojis'])):
                col1, col2 = st.columns([1, 5])

                with col1:
                    st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)

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
                <h2 class="certificate-title">🎉 Quiz Complete!</h2>
                <p style="font-size: 1.8rem; font-weight: 700; margin: 1rem 0;">{score}/{total} Correct</p>
                <p style="font-size: 1.2rem;">Accuracy: {percentage:.1f}%</p>
                <p style="font-size: 1.1rem;">+{50 if percentage >= 80 else 30 if percentage >= 60 else 10} XP</p>
            </div>
            """, unsafe_allow_html=True)

            # Update progress
            u = st.session_state.username
            prog = get_progress(u)
            prog['quizzes_taken'] = prog.get('quizzes_taken', 0) + 1
            prog['quiz_scores'] = prog.get('quiz_scores', []) + [percentage]
            prog['total_xp'] = prog.get('total_xp', 0) + (50 if percentage >= 80 else 30 if percentage >= 60 else 10)

            # Add certificate
            cert = {
                'quiz_name': quiz_name,
                'score': f"{score}/{total}",
                'percentage': f"{percentage:.1f}%",
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            prog['certificates'] = prog.get('certificates', []) + [cert]

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
        certs = prog.get('certificates', [])
        if certs:
            for cert in certs:
                st.markdown(f"""
                <div class="certificate">
                    <h2 style="color: white; margin: 0;">🏆 Certificate of Achievement</h2>
                    <p style="font-size: 1.5rem; margin: 1rem 0; font-weight: 700;">{cert['quiz_name']}</p>
                    <p style="font-size: 1.2rem;">Score: {cert['score']} ({cert['percentage']})</p>
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
        <p style="margin: 0.5rem 0; opacity: 0.9;">Master the ASL alphabet step by step</p>
    </div>
    """, unsafe_allow_html=True)

    # Keyboard only appears on demand (expandable)
    with st.expander("🎹 ASL Alphabet Reference (Click to expand)"):
        cols = st.columns(7)
        letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        for idx, letter in enumerate(letters):
            col_idx = idx % 7
            with cols[col_idx]:
                st.markdown(f"""
                <div style="background: white; border: 2px solid #667eea; border-radius: 12px; 
                            padding: 1rem; text-align: center; margin: 0.5rem 0;">
                    <div style="font-size: 2.5rem;">{ASL_ALPHABET[letter]}</div>
                    <div style="font-weight: 700; color: #667eea; font-size: 1.2rem;">{letter}</div>
                    <div style="font-size: 0.75rem; color: #5a6c7d;">{ASL_DESCRIPTIONS[letter][:25]}...</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="vibrant-card">
        <h3 style="color: #667eea;">Learn at Your Pace</h3>
        <p style="color: #5a6c7d;">Explore the ASL alphabet through our interactive keyboard reference. Click the reference above to see all letters with their hand sign descriptions.</p>
        <p style="color: #5a6c7d;"><strong>Pro Tip:</strong> Use the keyboard reference while taking quizzes to learn better!</p>
    </div>
    """, unsafe_allow_html=True)

print("✅ Part 3: Dashboard, Quiz, Profile, Learning Pages")

# ============================================================
# MAIN APPLICATION
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
