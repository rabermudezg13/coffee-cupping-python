import streamlit as st
from datetime import datetime, date

# Page configuration
st.set_page_config(
    page_title="Coffee Cupping App",
    page_icon="☕",
    layout="wide"
)

# Hide Streamlit branding
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {display: none;}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("☕ Coffee Cupping App")
    
    # Simple login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if email == "demo@coffee.com" and password == "demo123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Use: demo@coffee.com / demo123")
    else:
        show_app()

def show_app():
    st.success("✅ App is working!")
    
    # Sidebar
    with st.sidebar:
        page = st.radio("Pages", ["Dashboard", "Coffee Reviews"])
    
    if page == "Dashboard":
        st.header("Dashboard")
        st.metric("Total Reviews", "5", "2")
        
    elif page == "Coffee Reviews":
        st.header("Coffee Reviews")
        
        with st.form("coffee_review"):
            name = st.text_input("Coffee Name")
            rating = st.selectbox("Rating", [1,2,3,4,5])
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Save"):
                st.success(f"Saved review for {name} with {rating} stars!")

if __name__ == "__main__":
    main()