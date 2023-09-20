# import streamlit as st
# import sqlite3
# import bcrypt
# from pytube import YouTube

# # Connect to the SQLite database
# conn = sqlite3.connect('user_data.db')
# c = conn.cursor()

# # Create a table to store user data if it doesn't exist
# c.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')

# # User Authentication
# def authenticate_user(username, password):
#     c.execute('SELECT password FROM users WHERE username = ?', (username,))
#     stored_password = c.fetchone()

#     if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
#         return True
#     else:
#         return False

# # Streamlit app title
# st.title("YouTube Video Downloader")

# # Login Page
# def login():
#     st.title("Login")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if authenticate_user(username, password):
#             st.success("Logged in as: " + username)
#             download_video()
#         else:
#             st.error("Access Denied. Invalid credentials.")

# # Function to download the video
# def download_video():
#     st.subheader("YouTube Video Downloader")
#     video_url = st.text_input("Enter YouTube video URL")

#     if st.button("Download Video"):
#         try:
#             yt = YouTube(video_url)
#             st.subheader("Video Title:")
#             st.write(yt.title)

#             # Display video thumbnail
#             st.image(yt.thumbnail_url)

#             # Choose video stream and resolution
#             video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
#             st.subheader("Available Resolutions:")
#             st.write(video_stream.resolution)

#             # Download button
#             if st.button("Download Video"):
#                 st.info("Downloading... Please wait.")
#                 video_stream.download()
#                 st.success("Video Downloaded Successfully!")

#         except Exception as e:
#             st.error("An error occurred: " + str(e))

# # Check if the user is logged in
# if 'username' not in st.session_state:
#     login()
# else:
#     st.success("Logged in as: " + st.session_state.username)
#     download_video()




import streamlit as st
import sqlite3
import bcrypt
from pytube import YouTube

# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Create a table to store user data if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# User Authentication
def authenticate_user(username, password):
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    stored_password = c.fetchone()

    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
        return True
    else:
        return False

# User Registration
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# Streamlit app title
st.title("YouTube Video Downloader")

# Login Page
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="login_button"):
        if authenticate_user(username, password):
            st.session_state.username = username
            st.success("Logged in as: " + username)
            download_video()
        else:
            st.error("Access Denied. Invalid credentials.")

# Signup Page
def signup():
    st.title("Sign Up")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    
    # Check if the "Sign Up" button is clicked
    if st.button("Sign Up", key="signup_button"):
        # Check if both username and password are provided
        if new_username and new_password:
            register_user(new_username, new_password)
            st.success("Account created successfully. You can now log in.")
        else:
            st.warning("Please enter both a new username and a new password.")

# Function to download the video
def download_video():
    st.subheader("YouTube Video Downloader")
    video_url = st.text_input("Enter YouTube video URL")

    if st.button("Download Video", key="download_button"):
        try:
            yt = YouTube(video_url)
            st.subheader("Video Title:")
            st.write(yt.title)

            # Display video thumbnail
            st.image(yt.thumbnail_url)

            # Choose video stream and resolution
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            st.subheader("Available Resolutions:")
            st.write(video_stream.resolution)

            # Download button
            if st.button("Download Video", key="download_button"):
                st.info("Downloading... Please wait.")
                video_stream.download()
                st.success("Video Downloaded Successfully!")

        except Exception as e:
            st.error("An error occurred: " + str(e))

# Check if the user is logged in
if 'username' not in st.session_state:
    login()
else:
    st.success("Logged in as: " + st.session_state.username)
    download_video()

# Add a link to the signup page
st.sidebar.write("Don't have an account? Sign up here:")
if st.sidebar.button("Sign Up"):
    signup()
