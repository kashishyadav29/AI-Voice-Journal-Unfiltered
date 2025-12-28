import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import backend
import database

# Initialize database
database.init_db()

st.set_page_config(page_title="🎙️ Unfiltered - AI Voice Journal", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION SCREEN ---
def auth_screen():
    st.title("🧠 Welcome to Unfiltered")
    st.markdown("### Your personal AI-powered voice journal for self-reflection and growth 🌱")
    
    auth_option = st.radio("Choose an option:", ["Login", "Sign Up"])

    if auth_option == "Sign Up":
        with st.form("signup_form"):
            st.subheader("📝 Create an Account")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Create Account ✨")
            if submitted:
                database.create_user(name, email, password)
                st.success("🎉 Account created successfully! Please login now.")

    else:
        with st.form("login_form"):
            st.subheader("🔑 Login to Continue")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login 🚀")
            if submitted:
                user = database.login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome back, {user[1]} 🌟")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

# --- MAIN DASHBOARD ---
def main_dashboard():
    st.sidebar.title("🧭 Navigation")
    menu = st.sidebar.radio("Go to:", ["🎤 New Entry", "📖 My Journal", "📊 Dashboard", "🚪 Logout"])

    user = st.session_state.user
    st.sidebar.markdown(f"**Logged in as:** {user[1]}")

    # --- NEW ENTRY ---
    if menu == "🎤 New Entry":
        st.title("🎙️ Record Your Thoughts")
        st.write("Reflect on your day, express freely — your voice matters 💬")

        if st.button("🎧 Start Recording"):
            with st.spinner("Listening... Speak your heart out 💭"):
                text = backend.record_and_convert()

            if text.strip() == "" or "Sorry" in text:
                st.warning("⚠️ Could not capture your voice clearly. Try again.")
            else:
                st.success("Voice captured successfully!")
                st.markdown("### 🧠 Transcript:")
                st.write(f"“{text}”")

                mood = backend.analyze_mood(text)
                keywords = backend.extract_keywords(text)
                insight = backend.generate_insight_card(mood, keywords)

                st.markdown("---")
                st.markdown(
                 f"""
                    <div style="background-color:#cce7ff;padding:15px;border-radius:10px;box-shadow:2px 2px 10px #999;">
                        <h3 style="color:#0b3d91;">💡 Insight Card</h3>
                        <h4 style="color:#0b3d91;">Mood: <span style='color:{"green" if mood=="Positive" else "red" if mood=="Negative" else "gray"}'>{insight["Mood"]}</span></h4>
                        <p style="color:#0b3d91;"><b>Keywords:</b> {insight["Keywords"]}</p>
                        <p style="color:#0b3d91;">{insight["Suggestion"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                database.save_entry(user[0], str(date.today()), text, mood, ", ".join(keywords), str(insight))

    # --- VIEW JOURNAL ---
    elif menu == "📖 My Journal":
        st.title("📅 Your Journal Entries")
        entries = database.get_entries(user[0])
        if not entries:
            st.info("No entries yet. Start recording your first one today! 🌼")
        else:
            for e in entries:
                st.markdown(
                    f"""
                    <div style='background-color:#cce7ff;padding:15px;border-radius:10px;margin-bottom:15px;'>
                        <h4 style="color:#0b3d91;">🗓️ {e[2]} | Mood: {e[4]}</h4>
                        <p style="color:#0b3d91;"><b>📝 Transcript:</b> {e[3]}</p>
                        <p style="color:#0b3d91;"><b>💬 Keywords:</b> {e[5]}</p>
                        <p style="color:#0b3d91;"><b>💡 Insight:</b> {e[6]} </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # --- DASHBOARD ---
    elif menu == "📊 Dashboard":
        st.title("📈 Mood Dashboard")
        entries = database.get_entries(user[0])
        if entries:
            moods = [e[4] for e in entries]
            mood_counts = {
                "Positive": moods.count("Positive"),
                "Neutral": moods.count("Neutral"),
                "Negative": moods.count("Negative")
            }
            fig1, ax1 = plt.subplots()
            ax1.pie(mood_counts.values(), labels=mood_counts.keys(), autopct='%1.1f%%', startangle=90)
            st.pyplot(fig1)

            st.success("🌤️ Keep tracking your emotions to build emotional awareness and balance!")

        else:
            st.info("No data yet. Record a few entries to see your progress!")

    # --- LOGOUT ---
    elif menu == "🚪 Logout":
        st.session_state.user = None
        st.success("You've logged out successfully. Take care 💚")
        st.rerun()


# --- APP LOGIC ---
if st.session_state.user is None:
    auth_screen()
else:
    main_dashboard()