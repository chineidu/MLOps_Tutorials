"""
Streamlit Callbacks

- Callbacks are essential in Streamlit because they enable interactivity and state management in the application. 

- Streamlit, by design, re-runs the entire script from top to bottom every time a user interacts with a widget. 

- Callbacks offer a way to execute a specific, small piece of code only when a widget changes, which provides 
several key benefits.

- They're used with session state to persist data across reruns without re-executing heavy computations or side effects.
"""

import time
from functools import partial

import streamlit as st


def _init_session_state() -> None:
    """Initialize session state variables if they don't exist."""
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "submitted_name" not in st.session_state:
        st.session_state.submitted_name = ""
    if "last_heavy_result" not in st.session_state:
        st.session_state.last_heavy_result = None


def increment(step: int = 1) -> None:
    """Increment counter stored in session_state."""
    st.session_state.counter += step

def reset_counter() -> None:
    """Reset the counter stored in session_state."""

def set_name(name: str) -> None:
    """Set the submitted name (simple validation)."""
    cleaned = name.strip()
    if cleaned:
        st.session_state.submitted_name = cleaned
    else:
        st.warning("Cannot submit an empty name")


def heavy_operation(n: int = 1000) -> None:
    """Simulate heavier work; keep short in examples."""
    time.sleep(0.05)
    st.session_state.last_heavy_result = sum(i * i for i in range(n))


def main() -> None:
    """Main Streamlit app function."""
    _init_session_state()

    st.title("Streamlit callbacks — example")
    st.header("Buttons with on_click")
    st.write("Counter:", st.session_state.counter)

    # =====================================
    # ============= CALLBACKS =============
    # =====================================
    
    # These callbacks only run when the user clicks the corresponding button.
    st.button("Increment +1", on_click=increment, args=(1,))
    st.button("Increment +10", on_click=partial(increment, 10))
    # OR
    # st.button("Increment +10", on_click=increment, args=(10,))
    st.button("Reset Counter", on_click=reset_counter)

    st.divider()

    st.header("Form with on_submit callback")
    st.write("Submitted name:", st.session_state.submitted_name or "(none)")
    with st.form("name_form"):
        name = st.text_input("Your name")
        # Passing `name` as an arg captures the current input value at submit.
        st.form_submit_button("Submit", on_click=set_name, args=(name,))

    st.divider()

    st.header("Heavy operation (triggered)")
    st.write("Last heavy result:", st.session_state.last_heavy_result)
    # Heavy computations should be triggered explicitly via callbacks.
    st.button("Run heavy op", on_click=partial(heavy_operation, 5000))

    st.divider()

    st.markdown(
        """
        Notes:
        - Streamlit reruns your script on many interactions. Putting heavy or
          side-effecting code at top-level makes the UI sluggish.
        - Callbacks let you isolate those operations and run them only when
          the user explicitly requests them.
        - Use `st.session_state` to persist results across reruns.
        """
    )



if __name__ == "__main__":
    main()
