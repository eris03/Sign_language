"""
SignHub - Ultimate Professional Gen-Z Edition
Beautiful Login + Professional Dashboard + Advanced Features
"""

import streamlit as st
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="SignHub - Master Sign Language",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# Learning Levels - Basic to Advanced
LEARNING_LEVELS = {
    "Basic": {
        "title": "Level 1: Basic Alphabet",
        "description": "Learn A-Z signs",
        "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "youtube": "https://www.youtube.com/watch?v=v1desDduz5M"
    },
    "Intermediate": {
        "title": "Level 2: Common Words",
        "description": "Everyday vocabulary",
        "words": ["Hello", "Thanks", "Please", "Sorry", "Help"],
        "youtube": "https://www.youtube.com/watch?v=v1desDduz5M"
    },
    "Advanced": {
        "title": "Level 3: Sentences",
        "description": "Full conversations",
        "sentences": ["How are you?", "Nice to meet you", "What is your name?"],
        "youtube": "https://www.youtube.com/watch?v=v1desDduz5M"
    }
}

QUIZZES = {
    "ASL Alphabet Quiz": {
        "questions": [
            {"q": "What does letter 'A' look like?", "options": ["Closed fist", "Open palm", "Point finger", "Peace"], "emojis": ["👊", "✋", "☝️", "✌️"], "correct": 0, "points": 10},
            {"q": "How to sign 'B'?", "options": ["Flat hand", "Closed fist", "Two fingers", "Thumb between"], "emojis": ["✋", "👊", "✌️", "🤏"], "correct": 0, "points": 10},
            {"q": "Which is 'C'?", "options": ["C shape", "Open palm", "Pointing", "Peace sign"], "emojis": ["👌", "✋", "☝️", "✌️"], "correct": 0, "points": 10},
            {"q": "Sign for 'D'?", "options": ["Index up", "Closed fist", "Flat hand", "Pinky up"], "emojis": ["☝️", "👊", "✋", "🤙"], "correct": 0, "points": 10},
            {"q": "How is 'E' signed?", "options": ["Fingers curled", "Open palm", "Two fingers", "Thumb up"], "emojis": ["✊", "✋", "✌️", "👍"], "correct": 0, "points": 10}
        ]
    },
    "Numbers Quiz": {
        "questions": [
            {"q": "Sign for '1'?", "options": ["Index up", "Thumb up", "Open palm", "Closed fist"], "emojis": ["☝️", "👍", "✋", "👊"], "correct": 0, "points": 10},
            {"q": "Number '5'?", "options": ["All fingers", "Index only", "Two fingers", "Thumb only"], "emojis": ["✋", "☝️", "✌️", "👍"], "correct": 0, "points": 10},
            {"q": "Sign for '3'?", "options": ["Three fingers", "One finger", "Two fingers", "All fingers"], "emojis": ["✋", "☝️", "✌️", "👊"], "correct": 0, "points": 10},
        ]
    },
    "Greetings Quiz": {
        "questions": [
            {"q": "Say 'Hello'?", "options": ["Wave hand", "Salute", "Shake hands", "Nod"], "emojis": ["👋", "✌️", "🤝", "😊"], "correct": 0, "points": 10},
            {"q": "Say 'Thanks'?", "options": ["Hand on chest", "Clap", "Thumbs up", "Wave"], "emojis": ["🙏", "👏", "👍", "👋"], "correct": 0, "points": 10},
        ]
    }
}

GAMES = [
    {
        "name": "Fingerspelling Challenge",
        "icon": "🔤",
        "description": "Spell words using ASL alphabet",
        "difficulty": "Easy"
    },
    {
        "name": "Sign Memory",
        "icon": "🧠",
        "description": "Match signs with letters",
        "difficulty": "Medium"
    },
    {
        "name": "Speed Recognition",
        "icon": "⚡",
        "description": "Quick sign identification",
        "difficulty": "Hard"
    },
    {
        "name": "Story Builder",
        "icon": "📖",
        "description": "Create sentences with signs",
        "difficulty": "Expert"
    }
]

# ============================================================
# PROFESSIONAL GEN-Z CSS
# ============================================================
def get_professional_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        /* Hide Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}

        :root {
            --primary: #2E7867;
            --primary-light: #3a9178;
            --accent: #a8d5ba;
            --bg: #f0f4f1;
            --text: #1a1a1a;
            --text-light: #6b7280;
            --border: #e5e7eb;
            --shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
        }

        .main {
            background: var(--bg) !important;
            padding: 0 !important;
        }

        /* =============================================
           EXACT LOGIN PAGE DESIGN
        ============================================= */
        .login-container-exact {
            display: flex;
            width: 900px;
            max-width: 95%;
            min-height: 550px;
            margin: 50px auto;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            overflow: hidden;
            background: var(--primary);
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Welcome Side - LEFT */
        .welcome-side-exact {
            flex: 1;
            position: relative;
            padding: 40px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            clip-path: ellipse(70% 100% at 0 50%);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: inset 10px 0 20px rgba(0,0,0,0.1);
        }

        .welcome-text-exact {
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: 6px;
            color: white;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
            line-height: 1;
        }

        .welcome-illustration {
            width: 100%;
            height: 280px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 350"><defs><linearGradient id="g1" x1="0" x2="0" y1="1" y2="0"><stop offset="0%25" stop-color="%232a6f64"/><stop offset="100%25" stop-color="%2397bb72"/></linearGradient></defs><rect width="400" height="350" fill="url(%23g1)" rx="20"/><circle cx="320" cy="90" r="25" fill="%23fff" opacity="0.7"/><circle cx="280" cy="120" r="35" fill="%23e8f0de"/><rect x="170" y="150" width="70" height="40" fill="%23e6daca" rx="5"/><rect x="230" y="180" width="70" height="40" fill="%23c8d6c2" rx="5"/><polygon points="60,270 75,250 95,270 75,300" fill="%231f3a33"/></svg>') center/contain no-repeat;
            margin-top: auto;
        }

        /* Form Side - RIGHT */
        .form-side-exact {
            flex: 1.3;
            padding: 50px 50px;
            background: var(--primary);
            display: flex;
            flex-direction: column;
            color: white;
            overflow-y: auto;
        }

        .form-title-exact {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 30px;
            line-height: 1.4;
            color: white;
        }

        /* Social Buttons */
        .social-buttons-exact {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
        }

        .social-btn-exact {
            flex: 1;
            border: none;
            border-radius: 12px;
            padding: 12px 16px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .social-btn-exact:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        .google-btn { background: #e8f0fe; color: #4285f4; }
        .facebook-btn { background: #3b5998; color: white; }
        .twitter-btn { background: #1da1f2; color: white; }

        /* OR Divider */
        .or-divider-exact {
            display: flex;
            align-items: center;
            margin: 25px 0;
            gap: 15px;
            color: #aad5bd;
        }

        .or-divider-exact span {
            flex: 1;
            height: 1.5px;
            background: #aad5bd;
        }

        /* Input Fields */
        .input-exact {
            width: 100%;
            padding: 14px 18px;
            border-radius: 12px;
            border: 2px solid #aad5bd;
            background: transparent;
            color: white;
            font-size: 14px;
            font-weight: 500;
            outline: none;
            transition: all 0.3s;
            margin-bottom: 16px;
        }

        .input-exact::placeholder {
            color: #88c0a0;
        }

        .input-exact:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(168, 213, 186, 0.15);
        }

        /* Primary Button */
        .btn-primary-exact {
            background: var(--accent);
            color: var(--primary);
            font-weight: 700;
            border: none;
            border-radius: 12px;
            padding: 14px;
            width: 100%;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(168, 213, 186, 0.3);
            transition: all 0.3s;
            margin-top: 10px;
        }

        .btn-primary-exact:hover {
            background: #99bfaa;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(168, 213, 186, 0.4);
        }

        /* Toggle Link */
        .toggle-text-exact {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #aad5bd;
        }

        .toggle-link-exact {
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
        }

        .toggle-link-exact:hover {
            text-decoration: underline;
        }

        /* =============================================
           PROFESSIONAL DASHBOARD - GEN Z VIBE
        ============================================= */
        .dashboard-nav {
            background: white;
            padding: 1.5rem 2rem;
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 16px;
        }

        .dashboard-title {
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--text);
            margin: 0;
        }

        .btn-modern {
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-back {
            background: #f3f4f6;
            color: var(--text);
        }

        .btn-back:hover {
            background: #e5e7eb;
        }

        .btn-logout {
            background: #fee2e2;
            color: #dc2626;
        }

        .btn-logout:hover {
            background: #fecaca;
        }

        /* Stat Cards - Modern */
        .stat-card-modern {
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: var(--shadow);
            text-align: center;
            transition: all 0.3s;
            border-left: 4px solid var(--primary);
        }

        .stat-card-modern:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }

        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            color: var(--text);
            margin: 0.5rem 0;
        }

        .stat-label {
            font-size: 0.875rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        /* Action Cards */
        .action-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: var(--shadow);
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            border-top: 3px solid var(--primary);
        }

        .action-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
        }

        .action-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .action-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.5rem;
        }

        .action-desc {
            font-size: 0.875rem;
            color: var(--text-light);
        }

        /* Quiz Slideshow */
        .quiz-slide {
            background: white;
            padding: 3rem;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .quiz-option-modern {
            background: #f9fafb;
            border: 2px solid var(--border);
            padding: 1.25rem;
            margin: 1rem 0;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .quiz-option-modern:hover {
            background: #f0f9ff;
            border-color: var(--primary);
            transform: translateX(8px);
        }

        /* Game Cards */
        .game-card-slide {
            background: white;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            text-align: center;
            animation: slideInRight 0.6s;
        }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* Certificate Card */
        .certificate-modern {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            text-align: center;
            border: 4px solid #ffd700;
        }

        /* Responsive */
        @media (max-width: 900px) {
            .login-container-exact {
                flex-direction: column;
                height: auto;
            }

            .welcome-side-exact {
                clip-path: none;
                min-height: 200px;
            }

            .form-side-exact {
                padding: 30px;
            }
        }
    </style>
    """

st.markdown(get_professional_css(), unsafe_allow_html=True)

print("✅ Part 1: Professional CSS + Data Structures")

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
            "admin": {"password": hash_password("admin123"), "email": "admin@signhub.com", "full_name": "Admin User", "country": "USA", "phone": "", "bio": "", "joined": datetime.now().isoformat()},
            "demo": {"password": hash_password("demo123"), "email": "demo@signhub.com", "full_name": "Demo User", "country": "India", "phone": "", "bio": "", "joined": datetime.now().isoformat()}
        })
    if not PROGRESS_FILE.exists():
        save_json(PROGRESS_FILE, {})

def register_user(name, email, password, password2):
    if password != password2:
        return False, "Passwords do not match"
    if len(password) < 6:
        return False, "Password must be 6+ characters"

    users = load_json(USERS_FILE, {})
    for username, data in users.items():
        if data.get('email') == email:
            return False, "Email already registered"

    username = email.split('@')[0].lower()
    counter = 1
    original = username
    while username in users:
        username = f"{original}{counter}"
        counter += 1

    users[username] = {"password": hash_password(password), "email": email, "full_name": name, "country": "", "phone": "", "bio": "", "joined": datetime.now().isoformat()}
    prog = load_json(PROGRESS_FILE, {})
    prog[username] = {"level": 1, "quizzes_taken": 0, "quiz_scores": {}, "total_points": 0, "certificates": []}
    save_json(USERS_FILE, users)
    save_json(PROGRESS_FILE, prog)
    return True, f"Success! Your username is: {username}"

def login_user(email, password):
    users = load_json(USERS_FILE, {})
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

def get_progress(username):
    return load_json(PROGRESS_FILE, {}).get(username, {})

def update_progress(username, updates):
    prog = load_json(PROGRESS_FILE, {})
    if username in prog:
        prog[username].update(updates)
        save_json(PROGRESS_FILE, prog)

# ============================================================
# EXACT LOGIN PAGE - RIGHT SIDE FORM
# ============================================================
def page_login():
    """Exact login design with form on RIGHT side"""

    if 'login_mode' not in st.session_state:
        st.session_state.login_mode = 'login'

    st.markdown("""
    <div class="login-container-exact">
        <!-- LEFT: Welcome Side -->
        <div class="welcome-side-exact">
            <div class="welcome-text-exact">WELCOME</div>
            <div class="welcome-illustration"></div>
        </div>

        <!-- RIGHT: Form Side -->
        <div class="form-side-exact">
    """, unsafe_allow_html=True)

    # Tab Selection
    col1, col2 = st.columns(2)
    with col1:
        if st.button("LOGIN", use_container_width=True, key="tab_login"):
            st.session_state.login_mode = 'login'
            st.rerun()
    with col2:
        if st.button("REGISTER", use_container_width=True, key="tab_register"):
            st.session_state.login_mode = 'register'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.login_mode == 'login':
        # LOGIN FORM
        st.markdown('<div class="form-title-exact">Welcome Back!<br>Please login to your account</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="Enter your email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")

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

        st.markdown('<div class="toggle-text-exact">Don\'t have an account? <span class="toggle-link-exact">Click REGISTER above</span></div>', unsafe_allow_html=True)
        st.info("**Demo:** demo@signhub.com / demo123")

    else:
        # REGISTER FORM
        st.markdown('<div class="form-title-exact">Hello!<br>We are glad to see you :)</div>', unsafe_allow_html=True)

        # Social Buttons
        st.markdown("""
        <div class="social-buttons-exact">
            <button class="social-btn-exact google-btn"><span style="font-weight:900;">G</span> Google</button>
            <button class="social-btn-exact facebook-btn"><span style="font-weight:900;">f</span> Facebook</button>
            <button class="social-btn-exact twitter-btn"><span style="font-weight:900;">t</span> Twitter</button>
        </div>
        <div class="or-divider-exact"><span></span><small>Or</small><span></span></div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name", placeholder="Your name")
            with col2:
                email = st.text_input("Email", placeholder="Your email")

            col3, col4 = st.columns(2)
            with col3:
                password = st.text_input("Password", type="password", placeholder="Min 6 characters")
            with col4:
                password2 = st.text_input("Repeat Password", type="password", placeholder="Confirm password")

            agreed = st.checkbox("I agree to Terms of Service and Privacy Policy")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("Sign Up", use_container_width=True)

            if submit:
                if not agreed:
                    st.error("❌ You must agree to Terms")
                else:
                    ok, msg = register_user(name, email, password, password2)
                    if ok:
                        st.success("✅ " + msg)
                    else:
                        st.error("❌ " + msg)

        st.markdown('<div class="toggle-text-exact">Already have an account? <span class="toggle-link-exact">Click LOGIN above</span></div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

print("✅ Part 2: Data + Exact Login Page")

# ============================================================
# PROFESSIONAL DASHBOARD WITH BACK BUTTON
# ============================================================
def page_dashboard():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)

    # Navigation
    st.markdown(f"""
    <div class="dashboard-nav">
        <h1 class="dashboard-title">🤟 SignHub</h1>
        <div style="display: flex; gap: 10px;">
            <button class="btn-modern btn-logout" onclick="location.reload()">Logout</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", key="logout_btn"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown(f"### Welcome back, **{user.get('full_name', u)}**! 👋")
    st.markdown("<br>", unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">{prog.get('quizzes_taken', 0)}</div>
            <div class="stat-label">Quizzes</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">⭐</div>
            <div class="stat-value">{prog.get('level', 1)}</div>
            <div class="stat-label">Level</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">{len(prog.get('certificates', []))}</div>
            <div class="stat-label">Certificates</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">✨</div>
            <div class="stat-value">{prog.get('total_points', 0)}</div>
            <div class="stat-label">Points</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Actions
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">📚</div>
            <div class="action-title">Learn</div>
            <div class="action-desc">Basic to Advanced</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Learning", key="btn_learn", use_container_width=True):
            st.session_state.page = "learning"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">✍️</div>
            <div class="action-title">Quizzes</div>
            <div class="action-desc">Test knowledge</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Take Quiz", key="btn_quiz", use_container_width=True):
            st.session_state.page = "quizzes"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">🎮</div>
            <div class="action-title">Games</div>
            <div class="action-desc">Fun challenges</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play Games", key="btn_games", use_container_width=True):
            st.session_state.page = "games"
            st.rerun()

    with col4:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">📜</div>
            <div class="action-title">Results</div>
            <div class="action-desc">View scores</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Results", key="btn_results", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

# ============================================================
# LEARNING PAGE - BASIC TO ADVANCED + YOUTUBE
# ============================================================
def page_learning():
    # Back Button
    if st.button("← Back to Dashboard", key="back_learn"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("# 📚 Learn ASL - Basic to Advanced")
    st.markdown("Progress through levels: **Basic → Intermediate → Advanced**")
    st.markdown("<br>", unsafe_allow_html=True)

    # Level Tabs
    level = st.radio("Select Level:", ["Basic", "Intermediate", "Advanced"], horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    level_data = LEARNING_LEVELS[level]

    st.markdown(f"### {level_data['title']}")
    st.markdown(f"*{level_data['description']}*")
    st.markdown("<br>", unsafe_allow_html=True)

    # YouTube Link
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4>📺 Watch Video Tutorial</h4>
        <p>Learn ASL with step-by-step video guidance</p>
        <a href="{level_data['youtube']}" target="_blank" style="color: #2E7867; font-weight: 600;">
            ▶️ Open YouTube Tutorial
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Keyboard on demand (only when user wants to write)
    if st.button("🎹 Show ASL Keyboard Reference"):
        st.session_state.show_keyboard = not st.session_state.get('show_keyboard', False)

    if st.session_state.get('show_keyboard', False):
        st.markdown("### ASL Alphabet Reference")
        cols = st.columns(7)
        for idx, letter in enumerate(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')):
            with cols[idx % 7]:
                st.markdown(f"""
                <div style="background: white; border: 2px solid #2E7867; border-radius: 10px; padding: 1rem; text-align: center;">
                    <div style="font-size: 2rem;">{ASL_ALPHABET[letter]}</div>
                    <div style="font-weight: 700; color: #2E7867;">{letter}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Content based on level
    if level == "Basic":
        st.markdown("### Alphabet Practice")
        st.info("Click 'Show ASL Keyboard Reference' above to see all 26 letters with their signs")

    elif level == "Intermediate":
        st.markdown("### Common Words")
        words = level_data.get('words', [])
        for word in words:
            st.markdown(f"- **{word}**")

    else:  # Advanced
        st.markdown("### Full Sentences")
        sentences = level_data.get('sentences', [])
        for sentence in sentences:
            st.markdown(f"- **{sentence}**")

# ============================================================
# QUIZ PAGE - SLIDESHOW STYLE + DIRECT RESULTS ACCESS
# ============================================================
def page_quizzes():
    # Back Button
    if st.button("← Back to Dashboard", key="back_quiz"):
        st.session_state.page = "dashboard"
        st.session_state.quiz_started = False
        st.rerun()

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    if not st.session_state.quiz_started:
        st.markdown("# ✍️ ASL Quizzes")
        st.markdown("Test your knowledge and earn points!")
        st.markdown("<br>", unsafe_allow_html=True)

        for quiz_name in QUIZZES.keys():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="action-card">
                    <h3>{quiz_name}</h3>
                    <p>{len(QUIZZES[quiz_name]['questions'])} questions • {sum(q['points'] for q in QUIZZES[quiz_name]['questions'])} points</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(f"Start", key=f"start_{quiz_name}"):
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
            # Quiz Slideshow
            question = questions[current_q]

            st.progress((current_q + 1) / len(questions))
            st.markdown(f"**Question {current_q + 1} of {len(questions)}**")

            st.markdown(f"""
            <div class="quiz-slide">
                <h2>{question['q']}</h2>
            </div>
            """, unsafe_allow_html=True)

            # Options with ASL signs
            for idx, (option, emoji) in enumerate(zip(question['options'], question['emojis'])):
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
                with col2:
                    if st.button(option, key=f"opt_{idx}", use_container_width=True):
                        if idx == question['correct']:
                            st.session_state.quiz_score += question['points']
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect")
                        st.session_state.current_question += 1
                        time.sleep(1)
                        st.rerun()
        else:
            # Quiz Complete - Direct Results
            total_points = sum(q['points'] for q in questions)
            score = st.session_state.quiz_score
            percentage = (score / total_points) * 100

            # Save results
            u = st.session_state.username
            prog = get_progress(u)
            prog['quizzes_taken'] = prog.get('quizzes_taken', 0) + 1
            scores = prog.get('quiz_scores', {})
            scores[quiz_name] = {"score": score, "total": total_points, "percentage": percentage, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
            prog['quiz_scores'] = scores
            prog['total_points'] = prog.get('total_points', 0) + score

            # Certificate
            cert = {"quiz": quiz_name, "score": f"{score}/{total_points}", "percentage": f"{percentage:.1f}%", "date": datetime.now().strftime("%Y-%m-%d")}
            prog['certificates'] = prog.get('certificates', []) + [cert]

            update_progress(u, prog)

            st.markdown(f"""
            <div class="certificate-modern">
                <h1>🎉 Quiz Complete!</h1>
                <h2>{score}/{total_points} Points</h2>
                <h3>{percentage:.1f}% Accuracy</h3>
                <p>Certificate Earned! 🏆</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Retake", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.rerun()
            with col2:
                if st.button("📊 View All Results", use_container_width=True):
                    st.session_state.page = "results"
                    st.session_state.quiz_started = False
                    st.rerun()
            with col3:
                if st.button("🏠 Dashboard", use_container_width=True):
                    st.session_state.page = "dashboard"
                    st.session_state.quiz_started = False
                    st.rerun()

print("✅ Part 3: Dashboard, Learning, Quiz Pages")

# ============================================================
# GAMES PAGE - ATTRACTIVE SLIDESHOW
# ============================================================
def page_games():
    # Back Button
    if st.button("← Back to Dashboard", key="back_games"):
        st.session_state.page = "dashboard"
        st.session_state.current_game = 0
        st.rerun()

    if 'current_game' not in st.session_state:
        st.session_state.current_game = 0

    st.markdown("# 🎮 ASL Games")
    st.markdown("Learn through fun challenges!")
    st.markdown("<br>", unsafe_allow_html=True)

    # Game Navigation
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("◀ Previous", key="prev_game"):
            st.session_state.current_game = max(0, st.session_state.current_game - 1)
            st.rerun()

    with col2:
        st.markdown(f"<div style='text-align: center; font-weight: 600;'>Game {st.session_state.current_game + 1} of {len(GAMES)}</div>", unsafe_allow_html=True)

    with col3:
        if st.button("Next ▶", key="next_game"):
            st.session_state.current_game = min(len(GAMES) - 1, st.session_state.current_game + 1)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Display Current Game
    game = GAMES[st.session_state.current_game]

    st.markdown(f"""
    <div class="game-card-slide">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{game['icon']}</div>
        <h2>{game['name']}</h2>
        <p style="color: #6b7280; margin: 1rem 0;">{game['description']}</p>
        <div style="display: inline-block; background: #f0f9ff; color: #0369a1; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
            {game['difficulty']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("▶️ Play This Game", use_container_width=True, key=f"play_{game['name']}"):
        st.success(f"Starting {game['name']}...")
        st.info("Game functionality coming soon! This is a demo version.")

# ============================================================
# RESULTS PAGE - CERTIFICATES AND MARKS
# ============================================================
def page_results():
    # Back Button
    if st.button("← Back to Dashboard", key="back_results"):
        st.session_state.page = "dashboard"
        st.rerun()

    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)

    st.markdown("# 📊 Your Results & Certificates")
    st.markdown(f"### {user.get('full_name', u)}'s Learning Progress")
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📈 Quiz Scores", "🏆 Certificates"])

    with tab1:
        st.markdown("### Quiz Performance")

        scores = prog.get('quiz_scores', {})

        if scores:
            for quiz_name, data in scores.items():
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h3 style="margin: 0; color: #2E7867;">{quiz_name}</h3>
                    <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                        <div>
                            <strong>Score:</strong> {data['score']}/{data['total']}
                        </div>
                        <div>
                            <strong>Accuracy:</strong> {data['percentage']}
                        </div>
                        <div>
                            <strong>Date:</strong> {data['date']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 No quiz scores yet. Take a quiz to see your results here!")

    with tab2:
        st.markdown("### Earned Certificates")

        certs = prog.get('certificates', [])

        if certs:
            for cert in certs:
                st.markdown(f"""
                <div class="certificate-modern" style="margin: 1.5rem 0;">
                    <h2>🏆 Certificate of Achievement</h2>
                    <h3>{cert['quiz']}</h3>
                    <p style="font-size: 1.2rem; margin: 1rem 0;">Score: {cert['score']} ({cert['percentage']})</p>
                    <p>Earned on {cert['date']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🏆 No certificates yet. Complete quizzes to earn certificates!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Overall Stats
    st.markdown("### 📊 Overall Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">✍️</div>
            <div class="stat-value">{prog.get('quizzes_taken', 0)}</div>
            <div class="stat-label">Quizzes Taken</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">{len(certs)}</div>
            <div class="stat-label">Certificates</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-icon">✨</div>
            <div class="stat-value">{prog.get('total_points', 0)}</div>
            <div class="stat-label">Total Points</div>
        </div>
        """, unsafe_allow_html=True)

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
        elif st.session_state.page == "learning":
            page_learning()
        elif st.session_state.page == "quizzes":
            page_quizzes()
        elif st.session_state.page == "games":
            page_games()
        elif st.session_state.page == "results":
            page_results()

if __name__ == "__main__":
    main()
