import streamlit as st

# Apply custom CSS to make the text input larger
st.markdown("""
    <style>
    .big-input input {
        font-size: 20px !important;
        height: 1000px !important;
        width: 500px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.title("Large Text Input Example")

# Create a larger text input field
large_text_input = st.text_input(key="large_input", help="Type something", placeholder="Type your text here...", label_visibility="visible", label="Your Text")

# Apply the custom CSS class
st.markdown('<div class="big-input"></div>', unsafe_allow_html=True)

# Display the entered text
st.write("You entered:")
st.write(st.session_state.large_input)
