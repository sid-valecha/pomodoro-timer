import streamlit as st
import time
from datetime import datetime

def create_timer():
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "Work"
    if 'pomodoro_count' not in st.session_state:
        st.session_state.pomodoro_count = 0

    st.title("🍅 Pomodoro Timer")
    
    #timer settings in sidebar
    st.sidebar.header("Timer Settings")
    work_duration = st.sidebar.number_input("Work Duration (minutes)", 
                                          min_value=1, 
                                          max_value=60, 
                                          value=25)
    
    short_break = st.sidebar.number_input("Short Break Duration (minutes)", 
                                         min_value=1, 
                                         max_value=30, 
                                         value=5)
    
    long_break = st.sidebar.number_input("Long Break Duration (minutes)", 
                                        min_value=1, 
                                        max_value=60, 
                                        value=15)
    
    pomodoros_until_long_break = st.sidebar.number_input("Pomodoros until Long Break", 
                                                        min_value=1, 
                                                        max_value=10, 
                                                        value=4)

    #main timer display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Current Mode: {st.session_state.current_mode}")
        
    with col2:
        st.subheader(f"Pomodoros: {st.session_state.pomodoro_count}")

    #timer logic
    if not st.session_state.timer_running:
        if st.button("Start Timer"):
            st.session_state.timer_running = True
            st.rerun()
    else:
        if st.button("Stop Timer"):
            st.session_state.timer_running = False
            st.rerun()

    if st.session_state.timer_running:
        if st.session_state.current_mode == "Work":
            duration = work_duration
        elif st.session_state.current_mode == "Short Break":
            duration = short_break
        else:  #long break
            duration = long_break

        #create progress bar
        progress_bar = st.progress(0)
        timer_text = st.empty()

        total_seconds = duration * 60
        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() <= total_seconds and st.session_state.timer_running:
            elapsed_seconds = (datetime.now() - start_time).total_seconds()
            remaining_seconds = total_seconds - elapsed_seconds
            progress = elapsed_seconds / total_seconds
            
            #update progress bar and timer text
            progress_bar.progress(progress)
            mins, secs = divmod(int(remaining_seconds), 60)
            timer_text.markdown(f"## ⏱️ {mins:02d}:{secs:02d}")
            time.sleep(1)
            
            #check if we need to rerun the app
            if not st.session_state.timer_running:
                st.rerun()

        #timer completed
        if st.session_state.timer_running:
            if st.session_state.current_mode == "Work":
                st.session_state.pomodoro_count += 1
                if st.session_state.pomodoro_count % pomodoros_until_long_break == 0:
                    st.session_state.current_mode = "Long Break"
                else:
                    st.session_state.current_mode = "Short Break"
            else:
                st.session_state.current_mode = "Work"
            
            st.balloons()
            st.success(f"{st.session_state.current_mode} session completed!")
            st.session_state.timer_running = False
            st.rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="Pomodoro Timer", page_icon="🍅")
    create_timer()