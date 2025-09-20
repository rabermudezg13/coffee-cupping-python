import streamlit as st

st.set_page_config(page_title="Coffee App", page_icon="☕")

st.title("☕ Coffee Cupping App")
st.success("✅ App is working!")

# Login
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if email == "demo@coffee.com" and password == "demo123":
        st.success("Welcome!")
        
        st.header("Coffee Review")
        
        name = st.text_input("Coffee Name")
        rating = st.selectbox("Rating", [1,2,3,4,5])
        
        if st.button("Save Review"):
            st.success(f"Saved {name} with {rating} stars!")
    else:
        st.error("Use demo@coffee.com / demo123")

st.markdown("---")
st.markdown("© 2025 Rodrigo Bermudez - Cafe Cultura LLC")