import streamlit as st
from services.persistence.exercise_repository import get_or_create_user

# by default, the user is not logged in. They must enter a username to start the session. Once they enter a username, we will store it in the session state and use it for the rest of the session.

# in streamlit, it runs the python script from top to bottom every time the user interacts with the app (that is, presses any button, types any letter, etc). So we need to check if the user is logged in or not at the start of the script. If they are not logged in, we will show the login wall. If they are logged in, we will show the rest of the app.

# the submit button returns a boolean value indicating whether the form was submitted or not, once it is clicked and the script is rerun. If the form was submitted, we will check if the username is empty or not. If it is empty, we will show an error message. If it is not empty, we will create a new user in the database and store the user id and username in the session state. Then we will rerun the script to show the rest of the app.

def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True
    
    st.title("🏋️‍♂️ AI Real-time GYM Trainer")
    st.markdown("### Welcome! Please enter a username to start.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Name (unique)", placeholder="unique name e.g. John Smith")
        submit_button = st.form_submit_button("Start Session", width="stretch")

    if submit_button:
        if not username:
            st.error("Name cannot be empty.")
            return False
        
        user = get_or_create_user(username)
    
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]

        st.rerun()

    return False