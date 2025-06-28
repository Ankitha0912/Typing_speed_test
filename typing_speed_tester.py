import streamlit as st
import random
import time

# Sentences by level
sentences = {
    "easy": [
        "Practice typing every day.",
        "Python is fun.",
        "You can do this."
    ],
    "medium": [
        "Typing fast is useful in many situations.",
        "Programming improves problem solving skills.",
        "Keep practicing to improve speed and accuracy."
    ],
    "hard": [
        "The quick brown fox jumps over the lazy dog multiple times without missing a beat.",
        "Persistence is the key to mastering any skill, especially programming and typing.",
        "Real developers write clean, efficient, and well-documented code consistently."
    ]
}

# --- App config ---
st.set_page_config("Typing Speed Challenge", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎮 Typing Speed Challenge</h1>", unsafe_allow_html=True)

# --- Session state initialization ---
if "sentence" not in st.session_state:
    st.session_state.sentence = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "typed" not in st.session_state:
    st.session_state.typed = ""
if "result_shown" not in st.session_state:
    st.session_state.result_shown = False
if "timer_started" not in st.session_state:
    st.session_state.timer_started = False
if "game_stats" not in st.session_state:
    st.session_state.game_stats = {
        "games_played": 0,
        "total_wpm": 0,
        "best_wpm": 0
    }

# --- Countdown logic ---
TIMER_DURATION = 60  # seconds

def remaining_time():
    if st.session_state.start_time:
        return max(0, int(TIMER_DURATION - (time.time() - st.session_state.start_time)))
    return TIMER_DURATION

# --- Difficulty and sentence ---
level = st.selectbox("Choose difficulty level:", ["easy", "medium", "hard"])

if st.button("🎲 New Sentence"):
    st.session_state.sentence = random.choice(sentences[level])
    st.session_state.start_time = None
    st.session_state.typed = ""
    st.session_state.result_shown = False
    st.session_state.timer_started = False

# Show sentence
if st.session_state.sentence:
    st.markdown("### Type this:")
    st.markdown(f"<div style='padding: 10px; background-color: #f1f1f1; border-radius: 5px;'><b>{st.session_state.sentence}</b></div>", unsafe_allow_html=True)

    # Start button
    if st.button("▶️ Start Typing"):
        st.session_state.start_time = time.time()
        st.session_state.timer_started = True
        st.session_state.typed = ""
        st.session_state.result_shown = False

    # Show countdown if timer has started
    if st.session_state.timer_started:
        time_left = remaining_time()
        st.info(f"⏳ Time remaining: **{time_left} seconds**")
        if time_left == 0 and not st.session_state.result_shown:
            st.warning("⏱️ Time's up! Submitting automatically...")
            st.session_state.result_shown = True

    # Typing box
    typed_text = st.text_area("Start typing here:", value=st.session_state.get("typed", ""), height=150)
    st.session_state.typed = typed_text

    # Manual submit
    if st.button("✅ Submit") or (st.session_state.timer_started and remaining_time() == 0 and not st.session_state.result_shown):
        if not st.session_state.start_time:
            st.warning("Please click 'Start Typing' first.")
        elif st.session_state.result_shown:
            st.info("Already submitted. Click 'New Sentence' to try again.")
        else:
            end_time = time.time()
            elapsed_time = round(end_time - st.session_state.start_time, 2)
            original = st.session_state.sentence.strip()
            typed = st.session_state.typed.strip()

            word_count = len(original.split())
            typed_word_count = len(typed.split())
            wpm = round((typed_word_count / elapsed_time) * 60, 2)

            # Accuracy
            correct_chars = sum(1 for a, b in zip(typed, original) if a == b)
            accuracy = round((correct_chars / len(original)) * 100, 2)

            st.session_state.result_shown = True

            # Game stats update
            stats = st.session_state.game_stats
            stats["games_played"] += 1
            stats["total_wpm"] += wpm
            if wpm > stats["best_wpm"]:
                stats["best_wpm"] = wpm

            # Results
            st.markdown("---")
            st.subheader("📈 Your Results")
            st.success(f"Time Taken: {elapsed_time} seconds")
            st.info(f"Speed: {wpm} WPM")
            st.warning(f"Accuracy: {accuracy}%")
            st.progress(min(wpm / 100, 1.0))

            if wpm > 80:
                st.balloons()
                st.success("🏆 You’re lightning fast!")
            elif wpm > 50:
                st.success("🔥 Great job!")
            elif wpm > 30:
                st.info("💡 Keep practicing!")
            else:
                st.error("🧱 Slow start! Try again!")

            st.caption(f"Words you typed: {typed_word_count}")

# --- Score Tracker ---
with st.expander("📊 Score Tracker"):
    stats = st.session_state.game_stats
    avg_wpm = round(stats["total_wpm"] / stats["games_played"], 2) if stats["games_played"] > 0 else 0
    st.write(f"Games Played: {stats['games_played']}")
    st.write(f"Average Speed: {avg_wpm} WPM")
    st.write(f"Best Score: {stats['best_wpm']} WPM")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit | Countdown + Score Tracker Active")
