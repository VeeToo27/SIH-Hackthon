import streamlit as st
import pandas as pd

# Hide sidebar
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Load user credentials from CSV
@st.cache_data
def load_users():
    df = pd.read_csv("data/users.csv")  # Must contain columns: username, password, admin
    return df

users_df = load_users()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

def login():
    """Check credentials against CSV and update session state."""
    username = st.session_state.username
    password = st.session_state.password

    # Match user
    user = users_df[
        (users_df["username"] == username) &
        (users_df["password"] == password)
    ]

    if not user.empty:
        st.session_state.logged_in = True
        st.session_state.is_admin = bool(user.iloc[0]["admin"])

        # Redirect based on role
        if st.session_state.is_admin:
            st.switch_page("pages/admin_landing_page.py")
        else:
            st.switch_page("pages/user_landing_page.py")

        st.rerun()
    else:
        st.error("❌ Invalid username or password")

# Show login form only if not logged in
if not st.session_state.logged_in:
    st.title("🔑 Login Page")

    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=login)

else:
    # Already logged in → redirect based on role
    if st.session_state.is_admin:
        st.switch_page("pages/admin_landing_page.py")
    else:
        st.switch_page("pages/user_landing_page.py")
    st.rerun()
