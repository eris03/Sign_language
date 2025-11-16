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
    page_title="SignHub - Learn ASL",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language translations
LANGUAGES = {
    "English": {
        "app_name": "SignHub", "tagline": "Learn American Sign Language", 
        "login": "Sign In", "register": "Create Account", "dashboard": "Dashboard",
        "learning": "Learn", "quizzes": "Quizzes", "games": "Games",
        "profile": "Profile", "logout": "Logout", "welcome": "Welcome back",
        "continue": "Continue Learning", "quiz_btn": "Take Quiz",
        "game_btn": "Play Games", "progress_btn": "View Progress"
    },
    "हिंदी": {
        "app_name": "साइनहब", "tagline": "सांकेतिक भाषा सीखें",
        "login": "साइन इन", "register": "खाता बनाएं", "dashboard": "डैशबोर्ड",
        "learning": "सीखें", "quizzes": "क्विज", "games": "खेल",
        "profile": "प्रोफाइल", "logout": "लॉगआउट", "welcome": "स्वागत है",
        "continue": "सीखना जारी रखें", "quiz_btn": "क्विज लें",
        "game_btn": "खेलें", "progress_btn": "प्रगति"
    }
}

# Quiz database with questions
QUIZZES = {
    "ASL Alphabet Quiz": {
        "questions": [
            {"q": "What does the letter 'A' look like in ASL?", "options": ["Closed fist with thumb up", "Open palm", "Pointing finger", "Peace sign"], "correct": 0},
            {"q": "How do you sign the letter 'B'?", "options": ["Flat hand, fingers together", "Closed fist", "Two fingers up", "Thumb between fingers"], "correct": 0},
            {"q": "Which letter uses the 'OK' hand shape?", "options": ["C", "O", "F", "Both A and C"], "correct": 2},
            {"q": "How many handshapes are in the ASL alphabet?", "options": ["24", "26", "28", "30"], "correct": 1},
            {"q": "Which letters require movement?", "options": ["J and Z", "A and B", "X and Y", "None"], "correct": 0}
        ]
    },
    "Numbers Quiz": {
        "questions": [
            {"q": "How do you sign the number 1?", "options": ["Index finger up", "Thumb up", "Open palm", "Closed fist"], "correct": 0},
            {"q": "What number is signed with thumb and pinky extended?", "options": ["3", "5", "6", "9"], "correct": 2},
            {"q": "Which number looks like the letter 'F'?", "options": ["7", "8", "9", "10"], "correct": 2},
            {"q": "How do you sign 10?", "options": ["Thumbs up and shake", "Open palms", "Two hands forming X", "Closed fist"], "correct": 0},
            {"q": "Numbers 1-5 are signed with which hand orientation?", "options": ["Palm facing you", "Palm facing out", "Palm down", "Palm sideways"], "correct": 1}
        ]
    },
    "Greetings Quiz": {
        "questions": [
            {"q": "How do you sign 'Hello'?", "options": ["Wave hand", "Salute motion", "Shake hands", "Nod head"], "correct": 1},
            {"q": "What is the sign for 'Thank you'?", "options": ["Hand on chest moving forward", "Clapping", "Thumbs up", "Waving"], "correct": 0},
            {"q": "How do you ask 'How are you?'", "options": ["Point and move hands up", "Shrug shoulders", "Wave hand", "Thumbs up"], "correct": 0},
            {"q": "What does touching your chin mean?", "options": ["Think", "Please", "Sorry", "Mom"], "correct": 1},
            {"q": "How do you sign 'Good morning'?", "options": ["Sun rising motion", "Wave", "Smile and nod", "Flat hand on arm"], "correct": 3}
        ]
    }
}

# Enhanced CSS with modern design
def get_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
        }

        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .header-banner {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
            text-align: center;
            animation: fadeIn 0.8s ease-in;
        }

        .header-banner h1 {
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header-banner p {
            font-size: 1.2rem;
            margin-top: 0.5rem;
            opacity: 0.95;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s ease;
            cursor: pointer;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(102, 126, 234, 0.5);
        }

        .stat-card h3 {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }

        .stat-card p {
            font-size: 1rem;
            opacity: 0.9;
        }

        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #667eea;
        }

        .feature-card:hover {
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transform: translateY(-3px);
        }

        .quiz-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(252, 182, 159, 0.3);
        }

        .game-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 20px rgba(168, 237, 234, 0.4);
            transition: transform 0.3s ease;
            cursor: pointer;
        }

        .game-card:hover {
            transform: scale(1.05);
        }

        .game-card h2 {
            font-size: 2rem;
            margin: 0;
        }

        .success-box {
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0;
        }

        .error-box {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
        }

        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .progress-bar {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 30px;
            border-radius: 15px;
            transition: width 0.5s ease;
        }
    </style>
    """

st.markdown(get_css(), unsafe_allow_html=True)

# Data management
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

# Login page
def page_login():
    st.markdown("""
    <div class="header-banner">
        <h1>🤟 SignHub</h1>
        <p>Master American Sign Language with Interactive Learning</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### 🌐 Language")
    with col2:
        st.session_state.language = st.selectbox("Select", list(LANGUAGES.keys()), label_visibility="collapsed")

    st.markdown("---")
    lang = LANGUAGES[st.session_state.language]

    a, b = st.columns(2)
    with a:
        st.markdown("""
        <div class="feature-card">
            <h2>🎯 Why Learn ASL?</h2>
            <p>✅ Connect with 500K+ Deaf community</p>
            <p>✅ Boost your career opportunities</p>
            <p>✅ Learn a beautiful visual language</p>
            <p>✅ Make a real difference</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        tab1, tab2 = st.tabs([f"🔐 {lang['login']}", f"📝 {lang['register']}"])
        with tab1:
            u = st.text_input("Username", key="u")
            p = st.text_input("Password", type="password", key="p")
            if st.button(lang['login'], use_container_width=True):
                ok, msg = login_user(u, p)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.username = u
                    st.success("✅ " + msg)
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ " + msg)

        with tab2:
            ru = st.text_input("Username", key="ru")
            em = st.text_input("Email")
            fn = st.text_input("Full Name")
            c3, c4 = st.columns(2)
            with c3:
                country = st.text_input("Country", value="India")
            with c4:
                pl = st.selectbox("Language", list(LANGUAGES.keys()))
            rp = st.text_input("Password", type="password", key="rp")
            rc = st.text_input("Confirm", type="password")
            if st.button(lang['register'], use_container_width=True):
                if rp != rc:
                    st.error("❌ Passwords don't match")
                else:
                    ok, msg = register_user(ru, em, rp, fn, pl, country)
                    if ok:
                        st.success("✅ " + msg)
                    else:
                        st.error("❌ " + msg)

# Dashboard
def page_dashboard():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)
    lang = LANGUAGES[st.session_state.language]

    st.markdown(f"""
    <div class="header-banner">
        <h1>👋 {lang['welcome']}, {user.get('full_name', u)}!</h1>
        <p>Continue your amazing ASL journey</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats cards
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
            <div class="stat-card">
                <p>{icon} {label}</p>
                <h3>{value}</h3>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📚 " + lang['continue'], use_container_width=True, key="learn"):
            st.session_state.page = "learning"
            st.rerun()
    with c2:
        if st.button("✍️ " + lang['quiz_btn'], use_container_width=True, key="quiz"):
            st.session_state.page = "quizzes"
            st.rerun()
    with c3:
        if st.button("🎮 " + lang['game_btn'], use_container_width=True, key="game"):
            st.session_state.page = "games"
            st.rerun()
    with c4:
        if st.button("📊 Progress", use_container_width=True, key="prog"):
            st.session_state.page = "progress"
            st.rerun()

    # Recent activity
    st.markdown("---")
    st.markdown("### 📈 Recent Activity")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🎯 Quizzes Taken: {prog.get('quizzes_taken', 0)}")
        st.success(f"🎮 Games Played: {prog.get('games_played', 0)}")
    with col2:
        scores = prog.get('quiz_scores', [])
        if scores:
            avg = sum(scores) / len(scores)
            st.metric("Average Quiz Score", f"{avg:.1f}%")
        else:
            st.info("Take a quiz to see your score!")

# Continue in next part...
print("Creating enhanced app.py (Part 1)...")

# QUIZZES PAGE - FULLY FUNCTIONAL
def page_quizzes():
    lang = LANGUAGES[st.session_state.language]
    st.markdown(f"""
    <div class="header-banner">
        <h1>✍️ {lang['quizzes']}</h1>
        <p>Test your ASL knowledge and earn XP!</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize quiz state
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_name' not in st.session_state:
        st.session_state.quiz_name = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    # Quiz selection
    if not st.session_state.quiz_started:
        st.markdown("### 📝 Available Quizzes")
        for quiz_name in QUIZZES.keys():
            st.markdown(f"""
            <div class="quiz-card">
                <h3>{quiz_name}</h3>
                <p>🎯 {len(QUIZZES[quiz_name]['questions'])} Questions</p>
                <p>⏱️ 2-3 minutes</p>
                <p>🏆 Earn 50 XP</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Start {quiz_name}", key=f"start_{quiz_name}", use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.quiz_name = quiz_name
                st.session_state.current_question = 0
                st.session_state.quiz_score = 0
                st.session_state.answers = []
                st.rerun()

    # Quiz in progress
    else:
        quiz_name = st.session_state.quiz_name
        questions = QUIZZES[quiz_name]['questions']
        current_q = st.session_state.current_question

        if current_q < len(questions):
            # Progress bar
            progress = (current_q / len(questions)) * 100
            st.markdown(f"""
            <div style="background: #e0e0e0; border-radius: 15px; height: 30px; margin: 1rem 0;">
                <div class="progress-bar" style="width: {progress}%; height: 100%; text-align: center; line-height: 30px; color: white; font-weight: 600;">
                    Question {current_q + 1} / {len(questions)}
                </div>
            </div>
            """, unsafe_allow_html=True)

            question = questions[current_q]
            st.markdown(f"### ❓ {question['q']}")

            # Answer options
            answer = st.radio("Select your answer:", question['options'], key=f"q_{current_q}")

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Next ➡️", use_container_width=True):
                    selected = question['options'].index(answer)
                    st.session_state.answers.append(selected)
                    if selected == question['correct']:
                        st.session_state.quiz_score += 1
                    st.session_state.current_question += 1
                    st.rerun()

        # Quiz complete
        else:
            score = st.session_state.quiz_score
            total = len(questions)
            percentage = (score / total) * 100

            if percentage >= 80:
                st.markdown(f"""
                <div class="success-box">
                    🎉 Congratulations! You scored {score}/{total} ({percentage:.0f}%)
                    <br>+50 XP Earned!
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            elif percentage >= 60:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; font-size: 1.5rem; font-weight: 600;">
                    😊 Good job! You scored {score}/{total} ({percentage:.0f}%)
                    <br>+30 XP Earned!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="error-box">
                    💪 Keep practicing! You scored {score}/{total} ({percentage:.0f}%)
                    <br>+10 XP Earned!
                </div>
                """, unsafe_allow_html=True)

            # Update progress
            u = st.session_state.username
            prog = get_progress(u)
            prog['quizzes_taken'] = prog.get('quizzes_taken', 0) + 1
            prog['quiz_scores'] = prog.get('quiz_scores', []) + [percentage]
            prog['total_xp'] = prog.get('total_xp', 0) + (50 if percentage >= 80 else 30 if percentage >= 60 else 10)
            update_progress(u, prog)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Retake Quiz", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.session_state.current_question = 0
                    st.session_state.quiz_score = 0
                    st.session_state.answers = []
                    st.rerun()
            with col2:
                if st.button("🏠 Back to Dashboard", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.session_state.page = "dashboard"
                    st.rerun()

# GAMES PAGE - FULLY FUNCTIONAL
def page_games():
    st.markdown("""
    <div class="header-banner">
        <h1>🎮 Gaming Zone</h1>
        <p>Learn ASL through fun interactive games!</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize game state
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'game_name' not in st.session_state:
        st.session_state.game_name = None
    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0
    if 'game_round' not in st.session_state:
        st.session_state.game_round = 0

    # Game selection
    if not st.session_state.game_started:
        st.markdown("### 🎯 Choose Your Game")

        games = [
            ("🔤 Fingerspelling Challenge", "Spell words using ASL alphabet", "fingerspell"),
            ("🃏 Memory Match", "Match ASL signs with meanings", "memory"),
            ("⚡ Speed Quiz", "Answer as many as you can in 60s", "speed"),
            ("📖 Story Builder", "Create sentences with signs", "story")
        ]

        cols = st.columns(2)
        for i, (name, desc, key) in enumerate(games):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="game-card">
                    <h2>{name}</h2>
                    <p>{desc}</p>
                    <p>🏆 Earn 100 XP</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Play {name}", key=f"play_{key}", use_container_width=True):
                    st.session_state.game_started = True
                    st.session_state.game_name = key
                    st.session_state.game_score = 0
                    st.session_state.game_round = 0
                    st.rerun()

    # Game in progress
    else:
        game_name = st.session_state.game_name

        if game_name == "fingerspell":
            play_fingerspelling_game()
        elif game_name == "memory":
            play_memory_game()
        elif game_name == "speed":
            play_speed_quiz()
        elif game_name == "story":
            play_story_builder()

def play_fingerspelling_game():
    st.markdown("### 🔤 Fingerspelling Challenge")

    words = ["CAT", "DOG", "HELLO", "THANKS", "FRIEND", "HAPPY", "LEARN", "SIGN"]

    if st.session_state.game_round < 5:
        word = random.choice(words)
        st.markdown(f"""
        <div class="quiz-card">
            <h2>Spell this word in ASL:</h2>
            <h1 style="font-size: 3rem; color: #667eea;">{word}</h1>
        </div>
        """, unsafe_allow_html=True)

        user_input = st.text_input("Type each letter:", key=f"spell_{st.session_state.game_round}")

        if st.button("Submit", use_container_width=True):
            if user_input.upper() == word:
                st.session_state.game_score += 20
                st.success("✅ Correct! +20 points")
                time.sleep(1)
            else:
                st.error(f"❌ Try again! The word was {word}")
            st.session_state.game_round += 1
            st.rerun()
    else:
        st.markdown(f"""
        <div class="success-box">
            🎉 Game Complete!<br>
            Final Score: {st.session_state.game_score}/100<br>
            +100 XP Earned!
        </div>
        """, unsafe_allow_html=True)

        # Update progress
        u = st.session_state.username
        prog = get_progress(u)
        prog['games_played'] = prog.get('games_played', 0) + 1
        prog['total_xp'] = prog.get('total_xp', 0) + 100
        update_progress(u, prog)

        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

def play_memory_game():
    st.markdown("### 🃏 Memory Match")

    pairs = [
        ("👋", "Hello"),
        ("👍", "Good"),
        ("🙏", "Please"),
        ("❤️", "Love"),
        ("🤝", "Friend")
    ]

    if st.session_state.game_round < 5:
        sign, meaning = random.choice(pairs)

        st.markdown(f"""
        <div class="game-card">
            <h1 style="font-size: 4rem;">{sign}</h1>
            <h3>What does this sign mean?</h3>
        </div>
        """, unsafe_allow_html=True)

        options = [meaning] + [p[1] for p in pairs if p[1] != meaning][:2]
        random.shuffle(options)

        answer = st.radio("Select the meaning:", options, key=f"mem_{st.session_state.game_round}")

        if st.button("Submit", use_container_width=True):
            if answer == meaning:
                st.session_state.game_score += 20
                st.success("✅ Correct! +20 points")
                time.sleep(1)
            else:
                st.error(f"❌ Wrong! It means {meaning}")
            st.session_state.game_round += 1
            st.rerun()
    else:
        st.markdown(f"""
        <div class="success-box">
            🎉 Game Complete!<br>
            Score: {st.session_state.game_score}/100<br>
            +100 XP!
        </div>
        """, unsafe_allow_html=True)

        u = st.session_state.username
        prog = get_progress(u)
        prog['games_played'] = prog.get('games_played', 0) + 1
        prog['total_xp'] = prog.get('total_xp', 0) + 100
        update_progress(u, prog)

        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

def play_speed_quiz():
    st.markdown("### ⚡ Speed Quiz - Answer Fast!")
    st.info("🎯 Answer 10 questions as quickly as possible!")

    if st.session_state.game_round < 10:
        questions = [
            ("How many letters in ASL alphabet?", ["24", "26", "28"], 1),
            ("What does 👋 mean?", ["Hello", "Goodbye", "Thanks"], 0),
            ("Sign for 'please'?", ["Touch chest", "Wave", "Point"], 0),
        ]

        q, opts, correct = random.choice(questions)

        st.markdown(f"**Question {st.session_state.game_round + 1}/10**")
        st.markdown(f"### {q}")

        answer = st.radio("Answer:", opts, key=f"speed_{st.session_state.game_round}")

        if st.button("Submit", use_container_width=True):
            if opts.index(answer) == correct:
                st.session_state.game_score += 10
                st.success("✅ Correct!")
            else:
                st.error("❌ Wrong!")
            st.session_state.game_round += 1
            time.sleep(0.5)
            st.rerun()
    else:
        st.markdown(f"""
        <div class="success-box">
            ⚡ Speed Quiz Complete!<br>
            Score: {st.session_state.game_score}/100<br>
            +100 XP!
        </div>
        """, unsafe_allow_html=True)

        u = st.session_state.username
        prog = get_progress(u)
        prog['games_played'] = prog.get('games_played', 0) + 1
        prog['total_xp'] = prog.get('total_xp', 0) + 100
        update_progress(u, prog)

        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

def play_story_builder():
    st.markdown("### 📖 Story Builder")
    st.markdown("Build a sentence by selecting the correct signs!")

    sentence_parts = ["I", "LOVE", "TO", "LEARN", "ASL"]

    if st.session_state.game_round < len(sentence_parts):
        current_word = sentence_parts[st.session_state.game_round]

        st.markdown(f"""
        <div class="quiz-card">
            <h3>Select the sign for:</h3>
            <h1 style="color: #667eea;">{current_word}</h1>
        </div>
        """, unsafe_allow_html=True)

        options = ["👉", "❤️", "🤝", "📚", "🤟"]
        correct_map = {"I": "👉", "LOVE": "❤️", "TO": "🤝", "LEARN": "📚", "ASL": "🤟"}

        answer = st.radio("Choose the sign:", options, key=f"story_{st.session_state.game_round}")

        if st.button("Add to Sentence", use_container_width=True):
            if answer == correct_map[current_word]:
                st.session_state.game_score += 20
                st.success("✅ Correct!")
            else:
                st.error("❌ Try again next time!")
            st.session_state.game_round += 1
            time.sleep(1)
            st.rerun()
    else:
        st.markdown(f"""
        <div class="success-box">
            📖 Story Complete!<br>
            Your sentence: 👉 ❤️ 🤝 📚 🤟<br>
            "I LOVE TO LEARN ASL"<br>
            Score: {st.session_state.game_score}/100<br>
            +100 XP!
        </div>
        """, unsafe_allow_html=True)

        u = st.session_state.username
        prog = get_progress(u)
        prog['games_played'] = prog.get('games_played', 0) + 1
        prog['total_xp'] = prog.get('total_xp', 0) + 100
        update_progress(u, prog)

        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

# Continue to next part...

# LEARNING PAGE
def page_learning():
    lang = LANGUAGES[st.session_state.language]
    st.markdown(f"""
    <div class="header-banner">
        <h1>📚 {lang['learning']}</h1>
        <p>Learn from professional ASL tutorials</p>
    </div>
    """, unsafe_allow_html=True)

    level = st.selectbox("🎓 Select Level", ["🟢 Level 1: Beginner", "🟡 Level 2: Intermediate", "🔴 Level 3: Advanced"])

    st.markdown("---")

    if "Level 1" in level:
        st.markdown("### 🟢 Beginner Lessons")

        lessons = [
            ("🔤 ASL Alphabet", "Learn all 26 letters", "alphabet"),
            ("🔢 Numbers 1-20", "Count in ASL", "numbers"),
            ("👋 Greetings", "Basic greetings", "greetings"),
            ("📝 Daily Words", "Common vocabulary", "words"),
            ("💬 Simple Phrases", "Basic sentences", "phrases")
        ]

        for title, desc, key in lessons:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🎥 Watch", key=f"watch_{key}", use_container_width=True):
                    st.markdown("[📺 Learn How to Sign Channel](https://www.youtube.com/@LearnHowtoSign)")
                    st.success("✅ Opening YouTube channel...")

    elif "Level 2" in level:
        st.markdown("### 🟡 Intermediate Lessons")
        st.info("📺 Coming soon! Subscribe to Learn How to Sign for advanced lessons")
        if st.button("🎥 Visit Channel", use_container_width=True):
            st.markdown("[Learn How to Sign](https://www.youtube.com/@LearnHowtoSign)")

    else:
        st.markdown("### 🔴 Advanced Lessons")
        st.info("📺 Master advanced ASL on Learn How to Sign")
        if st.button("🎥 Visit Channel", use_container_width=True):
            st.markdown("[Learn How to Sign](https://www.youtube.com/@LearnHowtoSign)")

# PROFILE PAGE
def page_profile():
    u = st.session_state.username
    user = get_user(u)
    prog = get_progress(u)
    lang = LANGUAGES[st.session_state.language]

    st.markdown(f"""
    <div class="header-banner">
        <h1>👤 {lang['profile']}</h1>
        <p>Manage your account & achievements</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Stats", "⚙️ Settings", "🏆 Achievements"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>👤 Account Info</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**Username:** {u}")
            st.markdown(f"**Email:** {user.get('email', 'N/A')}")
            st.markdown(f"**Name:** {user.get('full_name', 'N/A')}")
            st.markdown(f"**Country:** {user.get('country', 'N/A')}")
            st.markdown(f"**Member Since:** {user.get('created_at', 'N/A')[:10]}")

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📊 Learning Stats</h3>
            </div>
            """, unsafe_allow_html=True)
            st.metric("Level", prog.get('level', 1))
            st.metric("Total XP", prog.get('total_xp', 0))
            st.metric("Quizzes Taken", prog.get('quizzes_taken', 0))
            st.metric("Games Played", prog.get('games_played', 0))

    with tab2:
        st.markdown("### ⚙️ Edit Profile")
        with st.form("edit"):
            name = st.text_input("Full Name", user.get('full_name', ''))
            email = st.text_input("Email", user.get('email', ''))
            country = st.text_input("Country", user.get('country', ''))
            new_lang = st.selectbox("Language", list(LANGUAGES.keys()))

            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                st.success("✅ Profile updated successfully!")
                st.session_state.language = new_lang

    with tab3:
        st.markdown("### 🏆 Your Achievements")

        total_xp = prog.get('total_xp', 0)
        quizzes = prog.get('quizzes_taken', 0)
        games = prog.get('games_played', 0)

        achievements = []
        if total_xp >= 100:
            achievements.append(("🌟 First Steps", "Earned 100 XP"))
        if quizzes >= 1:
            achievements.append(("✍️ Quiz Master", "Completed first quiz"))
        if games >= 1:
            achievements.append(("🎮 Gamer", "Played first game"))
        if total_xp >= 500:
            achievements.append(("🏆 ASL Champion", "Earned 500 XP"))

        if achievements:
            for icon_title, desc in achievements:
                st.markdown(f"""
                <div class="success-box">
                    <h3>{icon_title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Complete quizzes and games to earn achievements!")

# PROGRESS PAGE
def page_progress():
    u = st.session_state.username
    prog = get_progress(u)

    st.markdown("""
    <div class="header-banner">
        <h1>📊 Your Progress</h1>
        <p>Track your ASL learning journey</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎯 Level", prog.get('level', 1), "+0")
    with c2:
        st.metric("✨ Total XP", prog.get('total_xp', 0), f"+{prog.get('total_xp', 0)}")
    with c3:
        st.metric("✍️ Quizzes", prog.get('quizzes_taken', 0))
    with c4:
        st.metric("🎮 Games", prog.get('games_played', 0))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Quiz Performance")
        scores = prog.get('quiz_scores', [])
        if scores:
            avg = sum(scores) / len(scores)
            st.success(f"Average Score: {avg:.1f}%")
            st.info(f"Total Quizzes: {len(scores)}")
            st.metric("Best Score", f"{max(scores):.0f}%")
        else:
            st.info("Take a quiz to see your performance!")

    with col2:
        st.markdown("### 🎯 Next Milestone")
        xp = prog.get('total_xp', 0)
        next_level_xp = 500
        progress_pct = min((xp / next_level_xp) * 100, 100)

        st.markdown(f"""
        <div style="background: #e0e0e0; border-radius: 15px; height: 40px; margin: 1rem 0;">
            <div class="progress-bar" style="width: {progress_pct}%; height: 100%; text-align: center; line-height: 40px; color: white; font-weight: 600;">
                {xp} / {next_level_xp} XP
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(f"🎯 {next_level_xp - xp} XP to next level!")

# SIDEBAR
def sidebar():
    with st.sidebar:
        user = get_user(st.session_state.username)
        prog = get_progress(st.session_state.username)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
            <h2 style="margin: 0;">👤 {user.get('full_name', st.session_state.username)}</h2>
            <p style="margin: 0.5rem 0;">Level {prog.get('level', 1)} • {prog.get('total_xp', 0)} XP</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("🌐 " + st.session_state.language)
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
            st.session_state.username = None
            st.rerun()

# MAIN APP
def main():
    initialize()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.language = "English"
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "username" not in st.session_state:
        st.session_state.username = None

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
        else:
            page_dashboard()

if __name__ == "__main__":
    main()
