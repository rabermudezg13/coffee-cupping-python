import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json

# Page configuration
st.set_page_config(
    page_title="Coffee Cupping App - Professional SCA Protocol",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit branding and add responsive CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    
    /* Responsive Design */
    .main-header {
        background: linear-gradient(135deg, #8B4513, #D2B48C);
        padding: clamp(1rem, 3vw, 2rem);
        border-radius: 15px;
        margin-bottom: clamp(1rem, 3vw, 2rem);
        text-align: center;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.3);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: clamp(1.5rem, 5vw, 3rem);
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .coffee-card {
        background: linear-gradient(145deg, #F5F5DC, #E6E6D3);
        padding: clamp(1rem, 3vw, 2rem);
        border-radius: 15px;
        border-left: 5px solid #8B4513;
        margin: clamp(0.5rem, 2vw, 1rem) 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .coffee-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #FFFFFF, #F8F8F8);
        padding: clamp(1rem, 2.5vw, 1.5rem);
        border-radius: 12px;
        text-align: center;
        border: 2px solid #8B4513;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #8B4513, #A0522D);
        color: white;
        border-radius: 25px;
        border: none;
        padding: clamp(0.5rem, 2vw, 0.8rem) clamp(1rem, 3vw, 1.5rem);
        font-size: clamp(0.8rem, 2vw, 1rem);
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #A0522D, #CD853F);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(139, 69, 19, 0.4);
    }
    
    .language-selector {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 999;
        background: rgba(139, 69, 19, 0.95);
        padding: 0.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .language-selector {
            position: relative;
            top: auto;
            right: auto;
            margin-bottom: 1rem;
            width: 100%;
        }
        
        .stColumns > div {
            margin-bottom: 1rem;
        }
        
        .main-header {
            margin-bottom: 1rem;
        }
    }
    
    /* Tablet Responsive */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
    }
    
    /* Desktop Responsive */
    @media (min-width: 1025px) {
        .main-header {
            padding: 2rem;
        }
    }
    
    .flavor-category {
        background: linear-gradient(145deg, #FFF8DC, #F0E68C);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #DAA520;
    }
    
    .sca-scoring {
        background: linear-gradient(145deg, #E6F3FF, #CCE7FF);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4169E1;
    }
</style>
""", unsafe_allow_html=True)

# Language management
def get_language():
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    return st.session_state.language

def get_text(key):
    translations = {
        'en': {
            'app_title': '☕ Professional Coffee Cupping App',
            'subtitle': 'SCA Protocol Implementation',
            'login': 'Login',
            'logout': 'Logout',
            'email': 'Email Address',
            'password': 'Password',
            'demo_credentials': 'Demo Credentials',
            'dashboard': 'Dashboard',
            'cupping_sessions': 'Cupping Sessions', 
            'profile': 'My Profile',
            'flavor_wheel': 'SCA Flavor Wheel',
            'analytics': 'Analytics',
            'total_sessions': 'Total Sessions',
            'average_score': 'Average Score',
            'coffee_origins': 'Coffee Origins',
            'badges_earned': 'Badges Earned',
            'create_new_session': 'Create New Session',
            'session_name': 'Session Name',
            'cupping_date': 'Cupping Date',
            'number_of_samples': 'Number of Samples',
            'cups_per_sample': 'Cups per Sample',
            'welcome_user': 'Welcome',
            'new_session': 'New Session',
            'my_sessions': 'My Sessions',
            'analysis': 'Analysis',
            'recent_sessions': 'Recent Sessions',
            'score_trends': 'Score Trends',
            'flavor_profile': 'Flavor Profile Distribution'
        },
        'es': {
            'app_title': '☕ App Profesional de Cata de Café',
            'subtitle': 'Implementación Protocolo SCA',
            'login': 'Iniciar Sesión',
            'logout': 'Cerrar Sesión',
            'email': 'Correo Electrónico',
            'password': 'Contraseña',
            'demo_credentials': 'Credenciales Demo',
            'dashboard': 'Panel Principal',
            'cupping_sessions': 'Sesiones de Cata',
            'profile': 'Mi Perfil',
            'flavor_wheel': 'Rueda de Sabores SCA',
            'analytics': 'Analíticas',
            'total_sessions': 'Total Sesiones',
            'average_score': 'Puntaje Promedio',
            'coffee_origins': 'Orígenes de Café',
            'badges_earned': 'Insignias Obtenidas',
            'create_new_session': 'Crear Nueva Sesión',
            'session_name': 'Nombre de la Sesión',
            'cupping_date': 'Fecha de Cata',
            'number_of_samples': 'Número de Muestras',
            'cups_per_sample': 'Tazas por Muestra',
            'welcome_user': 'Bienvenido',
            'new_session': 'Nueva Sesión',
            'my_sessions': 'Mis Sesiones',
            'analysis': 'Análisis',
            'recent_sessions': 'Sesiones Recientes',
            'score_trends': 'Tendencias de Puntaje',
            'flavor_profile': 'Distribución de Perfil de Sabor'
        }
    }
    return translations.get(get_language(), {}).get(key, key)

def main():
    # Language selector
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col2:
            language_options = {"🇺🇸 English": "en", "🇪🇸 Español": "es"}
            selected_lang = st.selectbox(
                "🌐",
                options=list(language_options.keys()),
                index=0 if get_language() == 'en' else 1,
                key="language_selector"
            )
            if language_options[selected_lang] != get_language():
                st.session_state.language = language_options[selected_lang]
                st.rerun()
    
    # Header
    st.markdown(f'''
    <div class="main-header">
        <h1>{get_text("app_title")}</h1>
        <p style="color: #F5F5DC; margin: 0; font-size: 1.2rem;">{get_text("subtitle")}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_login()
    else:
        show_main_app()
    
    # Footer with copyright - appears on all pages including login
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem; padding: 1rem;'>"
        "© 2025 Rodrigo Bermudez - Cafe Cultura LLC. All rights reserved."
        "</div>", 
        unsafe_allow_html=True
    )

def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
        
        # Tabs for Login and Register
        tab1, tab2, tab3 = st.tabs([
            f"🔐 {get_text('login')}", 
            f"🆕 {get_text('register')}", 
            "👥 Guest"
        ])
        
        with tab1:
            show_login_form()
        
        with tab2:
            show_register_form()
        
        with tab3:
            show_guest_mode()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_login_form():
    st.markdown("### 🔐 Login to Your Account")
    
    st.info(f"**{get_text('demo_credentials')}:**\n\nEmail: demo@coffee.com\nPassword: demo123")
    
    email = st.text_input(get_text("email"), key="login_email")
    password = st.text_input(get_text("password"), type="password", key="login_password")
    remember_me = st.checkbox("🔒 Remember me", key="remember_login")
    
    if st.button(f"🚀 {get_text('login')}", use_container_width=True, key="login_btn"):
        # Check demo credentials
        if email == "demo@coffee.com" and password == "demo123":
            st.session_state.logged_in = True
            st.session_state.user_data = {
                'name': 'Demo User',
                'email': email,
                'company': 'Coffee Cultura LLC',
                'role': 'Q Grader',
                'member_since': 'January 2025',
                'user_type': 'demo'
            }
            st.success("✅ Demo login successful!")
            st.rerun()
        
        # Check registered users
        elif 'registered_users' in st.session_state and email in st.session_state.registered_users:
            stored_user = st.session_state.registered_users[email]
            if stored_user['password'] == password:  # In production, use hashed passwords
                st.session_state.logged_in = True
                st.session_state.user_data = {
                    'name': stored_user['name'],
                    'email': email,
                    'company': stored_user['company'],
                    'role': stored_user['role'],
                    'member_since': stored_user['member_since'],
                    'user_type': 'registered'
                }
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password")
        else:
            st.error("❌ User not found. Please register first or use demo credentials.")

def show_register_form():
    st.markdown("### 🆕 Create New Account")
    
    with st.form("registration_form"):
        st.markdown("#### 👤 Personal Information")
        full_name = st.text_input("Full Name *", help="Your full name as it will appear in the app")
        email = st.text_input("Email Address *", help="This will be your login username")
        
        st.markdown("#### 🔐 Security")
        password = st.text_input("Password *", type="password", help="Minimum 6 characters")
        confirm_password = st.text_input("Confirm Password *", type="password")
        
        st.markdown("#### ☕ Professional Information")
        company = st.text_input("Company/Organization", help="Optional: Your workplace or organization")
        role = st.selectbox("Your Role", [
            "Coffee Enthusiast",
            "Home Barista", 
            "Professional Barista",
            "Q Grader",
            "Coffee Roaster",
            "Café Owner",
            "Coffee Trader",
            "Coffee Producer",
            "Coffee Consultant",
            "Other"
        ])
        
        st.markdown("#### ☕ Coffee Experience")
        experience_level = st.selectbox("Cupping Experience", [
            "Beginner (New to cupping)",
            "Intermediate (Some experience)",
            "Advanced (Regular cupper)",
            "Expert (Professional level)"
        ])
        
        favorite_origins = st.multiselect("Favorite Coffee Origins", [
            "Ethiopia", "Colombia", "Brazil", "Guatemala", "Kenya", 
            "Costa Rica", "Jamaica", "Yemen", "Panama", "Honduras",
            "El Salvador", "Nicaragua", "Peru", "Bolivia", "Mexico"
        ])
        
        st.markdown("#### 📋 Preferences")
        newsletter = st.checkbox("📧 Subscribe to cupping tips and updates")
        public_profile = st.checkbox("🌐 Make my profile visible to other users", value=True)
        
        terms_accepted = st.checkbox("✅ I agree to the Terms of Service and Privacy Policy *")
        
        submit_button = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        if submit_button:
            # Validation
            errors = []
            
            if not full_name.strip():
                errors.append("❌ Full name is required")
            
            if not email.strip():
                errors.append("❌ Email is required")
            elif "@" not in email or "." not in email:
                errors.append("❌ Please enter a valid email address")
            
            if not password:
                errors.append("❌ Password is required")
            elif len(password) < 6:
                errors.append("❌ Password must be at least 6 characters")
            
            if password != confirm_password:
                errors.append("❌ Passwords don't match")
            
            if not terms_accepted:
                errors.append("❌ You must accept the Terms of Service")
            
            # Check if email already exists
            if 'registered_users' in st.session_state and email in st.session_state.registered_users:
                errors.append("❌ Email already registered. Please use a different email or login.")
            
            # Check if demo email
            if email == "demo@coffee.com":
                errors.append("❌ This email is reserved for demo purposes. Please use a different email.")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Initialize registered users if not exists
                if 'registered_users' not in st.session_state:
                    st.session_state.registered_users = {}
                
                # Create new user
                new_user = {
                    'name': full_name.strip(),
                    'password': password,  # In production, hash this!
                    'company': company.strip() if company else "Independent",
                    'role': role,
                    'experience_level': experience_level,
                    'favorite_origins': favorite_origins,
                    'newsletter': newsletter,
                    'public_profile': public_profile,
                    'member_since': datetime.now().strftime('%B %Y'),
                    'registration_date': datetime.now().isoformat(),
                    'total_sessions': 0,
                    'average_score': 0,
                    'badges': []
                }
                
                # Store user
                st.session_state.registered_users[email] = new_user
                
                st.success("✅ Account created successfully!")
                st.success("🎉 Welcome to the Coffee Cupping Community!")
                st.info("You can now login with your new credentials in the Login tab.")
                
                # Show registration summary
                st.markdown("### 📋 Registration Summary")
                st.markdown(f"**Name:** {full_name}")
                st.markdown(f"**Email:** {email}")
                st.markdown(f"**Role:** {role}")
                st.markdown(f"**Experience:** {experience_level}")
                if favorite_origins:
                    st.markdown(f"**Favorite Origins:** {', '.join(favorite_origins)}")

def show_guest_mode():
    st.markdown("### 👥 Guest Mode")
    
    st.info("""
    **Guest Mode Features:**
    - ✅ Full app functionality
    - ✅ Create cupping sessions
    - ✅ Use flavor wheel
    - ✅ View analytics
    - ⚠️ Data not saved permanently
    - ⚠️ Limited to current session
    """)
    
    guest_name = st.text_input("Your Name (Optional)", placeholder="Coffee Lover")
    
    if st.button("🚀 Enter as Guest", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.user_data = {
            'name': guest_name if guest_name else 'Guest User',
            'email': 'guest@demo.com',
            'company': 'Guest Session',
            'role': 'Coffee Enthusiast',
            'member_since': 'Today',
            'user_type': 'guest'
        }
        st.success("✅ Welcome, Guest!")
        st.rerun()

def show_main_app():
    user_data = st.session_state.get('user_data', {})
    
    # Header with user info
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"## 👋 {get_text('welcome_user')}, {user_data.get('name', 'User')}!")
        
    with col2:
        st.markdown(f"📧 **{user_data.get('email', '')}**")
        st.markdown(f"🏢 **{user_data.get('company', '')}**")
    
    with col3:
        if st.button(get_text("logout")):
            st.session_state.logged_in = False
            st.rerun()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### ☕ Navigation")
        
        pages = [
            f"📊 {get_text('dashboard')}",
            f"☕ {get_text('cupping_sessions')}",
            f"👤 {get_text('profile')}",
            f"📈 {get_text('analytics')}"
        ]
        
        selected_page = st.radio("", pages, key="navigation")
        
        st.markdown("---")
        
        # User stats in sidebar
        st.markdown("### 📊 Quick Stats")
        st.metric(get_text("total_sessions"), "15", "3")
        st.metric(get_text("average_score"), "87.2", "2.1")
        st.metric(get_text("badges_earned"), "8", "2")
    
    # Main content routing
    if selected_page.endswith(get_text('dashboard')):
        show_dashboard()
    elif selected_page.endswith(get_text('cupping_sessions')):
        show_cupping_sessions()
    elif selected_page.endswith(get_text('profile')):
        show_profile()
    elif selected_page.endswith(get_text('analytics')):
        show_analytics()

def show_dashboard():
    st.title(f"📊 {get_text('dashboard')}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        (get_text("total_sessions"), "15", "3", "↗️"),
        (get_text("average_score"), "87.2", "2.1", "📈"),
        (get_text("coffee_origins"), "12", "2", "🌍"),
        (get_text("badges_earned"), "8", "2", "🏆")
    ]
    
    for i, (metric, value, delta, icon) in enumerate(metrics_data):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="margin: 0; color: #8B4513;">{icon}</h3>
                <h2 style="margin: 0; color: #2C1810;">{value}</h2>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">{metric}</p>
                <p style="margin: 0; color: #28a745; font-size: 0.8rem;">+{delta}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📅 {get_text('recent_sessions')}")
        
        # Sample recent sessions data
        recent_sessions = [
            {"name": "Ethiopian Yirgacheffe", "date": "2025-01-15", "score": 89.5, "origin": "Ethiopia"},
            {"name": "Colombian Supremo", "date": "2025-01-12", "score": 85.2, "origin": "Colombia"},
            {"name": "Brazilian Santos", "date": "2025-01-10", "score": 82.8, "origin": "Brazil"},
            {"name": "Guatemalan Antigua", "date": "2025-01-08", "score": 91.0, "origin": "Guatemala"},
        ]
        
        for session in recent_sessions:
            st.markdown(f'''
            <div class="coffee-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h4 style="margin: 0; color: #8B4513;">☕ {session["name"]}</h4>
                        <p style="margin: 0; color: #666;">🌍 {session["origin"]} | 📅 {session["date"]}</p>
                    </div>
                    <div style="text-align: right;">
                        <h3 style="margin: 0; color: #2C1810;">⭐ {session["score"]}</h3>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        if st.button("🆕 New Cupping Session", use_container_width=True):
            st.switch_page("streamlit_app.py")
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.success("Switching to Analytics...")
        
        if st.button("🎨 Flavor Wheel", use_container_width=True):
            st.success("Opening Flavor Wheel...")
        
        st.markdown("---")
        
        st.subheader("🏆 Latest Achievement")
        st.markdown('''
        <div style="background: linear-gradient(45deg, #FFD700, #FFA500); padding: 1rem; border-radius: 10px; text-align: center; color: white;">
            <h3 style="margin: 0;">🏅 Master Cupper</h3>
            <p style="margin: 0;">Completed 10 sessions with 85+ score</p>
        </div>
        ''', unsafe_allow_html=True)

def show_cupping_sessions():
    st.title(f"☕ {get_text('cupping_sessions')}")
    
    # Tabs for different session views
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text("new_session"),
        get_text("my_sessions"), 
        get_text("analysis"),
        get_text("flavor_wheel")
    ])
    
    with tab1:
        show_new_session_form()
    
    with tab2:
        show_my_sessions()
    
    with tab3:
        show_session_analysis()
    
    with tab4:
        show_flavor_wheel()

def show_new_session_form():
    st.subheader(f"🆕 {get_text('create_new_session')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sca-scoring">', unsafe_allow_html=True)
        st.markdown("### 📋 Session Details")
        
        session_name = st.text_input(get_text("session_name"))
        cupping_date = st.date_input(get_text("cupping_date"), value=date.today())
        num_samples = st.number_input(get_text("number_of_samples"), 1, 8, 3)
        cups_per_sample = st.number_input(get_text("cups_per_sample"), 3, 5, 5)
        
        st.markdown("### ⚙️ Session Settings")
        evaluation_type = st.selectbox("Evaluation Protocol", ["SCA Standard", "COE Protocol", "Custom"])
        is_blind = st.checkbox("Blind Cupping", value=True)
        allow_notes = st.checkbox("Allow Tasting Notes", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="sca-scoring">', unsafe_allow_html=True)
        st.markdown("### 🌱 Sample Information")
        
        samples_data = []
        for i in range(num_samples):
            st.markdown(f"**Sample {i+1}:**")
            sample_name = st.text_input(f"Name", key=f"sample_name_{i}")
            origin = st.text_input(f"Origin", key=f"origin_{i}")
            process = st.selectbox(f"Process", ["Washed", "Natural", "Honey", "Pulped Natural"], key=f"process_{i}")
            
            samples_data.append({
                'name': sample_name,
                'origin': origin,
                'process': process
            })
            
            if i < num_samples - 1:
                st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button(f"🚀 {get_text('create_new_session')}", use_container_width=True):
        if session_name:
            st.success(f"✅ Created session: '{session_name}' with {num_samples} samples")
            st.balloons()
            
            # Store session in session state
            if 'cupping_sessions' not in st.session_state:
                st.session_state.cupping_sessions = []
            
            new_session = {
                'name': session_name,
                'date': cupping_date.strftime('%Y-%m-%d'),
                'samples': samples_data,
                'type': evaluation_type,
                'created': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            
            st.session_state.cupping_sessions.append(new_session)
        else:
            st.error("❌ Please enter a session name")

def show_my_sessions():
    st.subheader(f"📋 {get_text('my_sessions')}")
    
    if 'cupping_sessions' in st.session_state and st.session_state.cupping_sessions:
        for i, session in enumerate(st.session_state.cupping_sessions):
            st.markdown(f'''
            <div class="coffee-card">
                <h4 style="margin: 0; color: #8B4513;">☕ {session["name"]}</h4>
                <p style="margin: 0; color: #666;">📅 {session["date"]} | 🌱 {len(session["samples"])} samples | 🔬 {session["type"]}</p>
                <p style="margin: 0; color: #888; font-size: 0.8rem;">Created: {session["created"]}</p>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("📝 No sessions yet. Create your first cupping session!")

def show_session_analysis():
    st.subheader(f"📊 {get_text('analysis')}")
    
    # Sample analysis data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Score Distribution")
        
        # Sample data for score distribution
        scores = [82, 85, 87, 89, 91, 84, 86, 88, 90, 83, 85, 87]
        score_df = pd.DataFrame({'Session': range(1, len(scores)+1), 'Score': scores})
        
        fig = px.line(score_df, x='Session', y='Score', 
                     title='Cupping Scores Over Time',
                     markers=True)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🌍 Origin Distribution")
        
        # Sample data for origins
        origins = ['Ethiopia', 'Colombia', 'Brazil', 'Guatemala', 'Kenya', 'Costa Rica']
        counts = [4, 3, 2, 2, 2, 2]
        
        fig = px.pie(values=counts, names=origins, title='Coffee Origins Cupped')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)

def show_flavor_wheel():
    st.subheader(f"🎨 {get_text('flavor_wheel')}")
    
    st.success("✅ SCA Flavor Wheel - Professional Implementation")
    
    # SCA Flavor Wheel Categories
    flavor_categories = {
        "🍊 Fruity": {
            "Citrus Fruit": ["Grapefruit", "Orange", "Lemon", "Lime"],
            "Berry": ["Blackberry", "Raspberry", "Blueberry", "Strawberry"],
            "Dried Fruit": ["Raisin", "Prune", "Fig", "Date"],
            "Other Fruit": ["Coconut", "Cherry", "Pomegranate", "Pineapple"]
        },
        "🌸 Floral": {
            "Black Tea": ["Black Tea"],
            "Floral": ["Chamomile", "Rose", "Jasmine", "Lavender"]
        },
        "🍯 Sweet": {
            "Brown Sugar": ["Molasses", "Maple Syrup", "Caramelized", "Honey"],
            "Vanilla": ["Vanilla"],
            "Cocoa": ["Chocolate", "Dark Chocolate"]
        },
        "🥜 Nutty/Cocoa": {
            "Nutty": ["Peanuts", "Hazelnut", "Almond", "Walnut"],
            "Cocoa": ["Cocoa", "Dark Chocolate"]
        },
        "🌿 Green/Vegetative": {
            "Olive Oil": ["Olive Oil"],
            "Raw": ["Green", "Underripe"],
            "Beany": ["Fresh", "Dark Green"]
        },
        "🔥 Roasted": {
            "Pipe Tobacco": ["Pipe Tobacco"],
            "Burnt": ["Acrid", "Ashy", "Smoky"],
            "Cereal": ["Grain", "Malt"]
        },
        "🌶️ Spices": {
            "Pungent": ["Pepper", "Brown Spice"],
            "Brown Spice": ["Anise", "Nutmeg", "Cinnamon", "Clove"]
        },
        "🧪 Other": {
            "Sour/Fermented": ["Sour", "Alcohol", "Winey", "Fermented"],
            "Chemical": ["Bitter", "Salty", "Medicinal", "Petroleum"]
        }
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Select Flavor Descriptors")
        
        selected_flavors = []
        
        for main_category, subcategories in flavor_categories.items():
            with st.expander(f"{main_category}", expanded=False):
                for subcategory, flavors in subcategories.items():
                    st.markdown(f"**{subcategory}:**")
                    
                    # Create columns for better layout
                    cols = st.columns(min(len(flavors), 3))
                    for i, flavor in enumerate(flavors):
                        with cols[i % len(cols)]:
                            if st.checkbox(flavor, key=f"flavor_{main_category}_{subcategory}_{flavor}"):
                                selected_flavors.append(flavor)
    
    with col2:
        st.markdown("### 📋 Selected Descriptors")
        
        if selected_flavors:
            for flavor in selected_flavors:
                st.markdown(f"🏷️ **{flavor}**")
            
            st.markdown("---")
            st.markdown(f"**Total Selected:** {len(selected_flavors)}")
            
            if st.button("💾 Save Flavor Profile"):
                st.success("✅ Flavor profile saved!")
        else:
            st.info("Select flavors from the wheel to build your profile")
        
        st.markdown("---")
        st.markdown("### 📖 SCA Guidelines")
        st.markdown("""
        - **Primary flavors:** Most prominent characteristics
        - **Secondary flavors:** Supporting notes
        - **Finish:** Aftertaste descriptors
        - **Maximum 8-10 descriptors** recommended
        """)

def show_profile():
    st.title(f"👤 {get_text('profile')}")
    
    user_data = st.session_state.get('user_data', {})
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Profile Information")
        
        with st.form("profile_form"):
            name = st.text_input("Full Name", value=user_data.get('name', ''))
            email = st.text_input("Email", value=user_data.get('email', ''), disabled=True)
            company = st.text_input("Company/Organization", value=user_data.get('company', ''))
            role = st.text_input("Role/Position", value=user_data.get('role', ''))
            
            st.markdown("### ☕ Coffee Preferences")
            favorite_origin = st.selectbox("Favorite Origin", 
                ["Ethiopia", "Colombia", "Brazil", "Guatemala", "Kenya", "Costa Rica", "Other"])
            brewing_methods = st.multiselect("Preferred Brewing Methods",
                ["Pour Over", "French Press", "Espresso", "Aeropress", "Cold Brew", "Chemex"])
            
            if st.form_submit_button("💾 Update Profile"):
                st.success("✅ Profile updated successfully!")
    
    with col2:
        st.subheader("📊 Your Statistics")
        
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="margin: 0;">👤 {user_data.get("name", "User")}</h3>
            <p style="margin: 0; color: #666;">{user_data.get("role", "Coffee Enthusiast")}</p>
            <p style="margin: 0; color: #666;">📅 Member since: {user_data.get("member_since", "2025")}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.metric("Total Sessions", "15", "3")
        st.metric("Average Score", "87.2", "2.1")
        st.metric("Highest Score", "94.5", "")
        st.metric("Countries Cupped", "8", "1")
        
        st.markdown("---")
        st.subheader("🏆 Achievements")
        
        achievements = [
            ("🥇 First Cup", "Complete your first cupping"),
            ("⭐ High Scorer", "Score above 90 points"),
            ("🌍 World Explorer", "Cup from 5+ countries"),
            ("🔬 Analyst", "Complete 10+ sessions")
        ]
        
        for icon, desc in achievements:
            st.markdown(f"✅ **{icon}** {desc}")

def show_analytics():
    st.title(f"📈 {get_text('analytics')}")
    
    # Advanced analytics dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📊 {get_text('score_trends')}")
        
        # Generate sample trend data
        import numpy as np
        dates = pd.date_range('2024-12-01', '2025-01-15', freq='2D')
        scores = 85 + np.random.normal(0, 3, len(dates)).cumsum() * 0.1
        scores = np.clip(scores, 75, 95)
        
        trend_df = pd.DataFrame({'Date': dates, 'Score': scores})
        
        fig = px.line(trend_df, x='Date', y='Score', 
                     title='Your Cupping Score Evolution',
                     markers=True)
        fig.add_hline(y=85, line_dash="dash", line_color="red", 
                     annotation_text="Target: 85 points")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"🎨 {get_text('flavor_profile')}")
        
        # Sample flavor distribution
        flavors = ['Fruity', 'Floral', 'Sweet', 'Nutty', 'Spicy', 'Roasted']
        percentages = [25, 15, 20, 18, 12, 10]
        
        fig = px.bar(x=flavors, y=percentages, 
                    title='Your Most Used Flavor Categories',
                    color=percentages,
                    color_continuous_scale='Viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analytics
    st.markdown("---")
    st.subheader("📋 Detailed Performance Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 SCA Categories Average")
        categories = ['Fragrance/Aroma', 'Flavor', 'Aftertaste', 'Acidity', 'Body', 'Balance', 'Overall']
        scores = [8.2, 8.5, 8.1, 8.7, 8.3, 8.4, 8.6]
        
        for cat, score in zip(categories, scores):
            st.metric(cat, f"{score}/10", f"+{round(score-8, 1)}")
    
    with col2:
        st.markdown("### 🌍 Origin Performance")
        origins = ['Ethiopia', 'Colombia', 'Brazil', 'Guatemala']
        avg_scores = [89.2, 87.5, 84.8, 91.0]
        
        for origin, score in zip(origins, avg_scores):
            st.metric(f"{origin}", f"{score}", f"+{round(score-85, 1)}")
    
    with col3:
        st.markdown("### 📅 Monthly Progress")
        months = ['Nov 2024', 'Dec 2024', 'Jan 2025']
        monthly_avg = [84.2, 86.1, 87.8]
        
        for month, avg in zip(months, monthly_avg):
            st.metric(month, f"{avg}", f"+{round(avg-84, 1)}")

if __name__ == "__main__":
    main()