import streamlit as st

st.title("My First Streamlit App")

"""
For tracking data across user interactions, Streamlit provides `st.session_state`, a built-in 
dictionary-like object.
"""

if "counter" not in st.session_state:
    st.session_state.counter = 0


if st.button("Increment"):
    st.session_state.counter += 1

if st.button("Decrement"):
    st.session_state.counter -= 1

if st.button("Reset"):
    st.session_state.counter = 0


st.write("Counter:", st.session_state.counter)
