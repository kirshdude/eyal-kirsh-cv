from all_cv_text import all_text
import streamlit as st
from streamlit_option_menu import option_menu

import sections
from sections.home import display_introduction
from sections.professional import display_cv
from sections.education import display_education
from sections.skills import display_skills
from sections.contact import display_contact
from sections.chatbot import chat_with_gpt, show_faq


# Streamlit app layout
def main():
    side_bar = {'menu_title': 'Eyal Kirsh CV',
                'options': ['Home', 'Chatbot', 'Professional Experience', 'Contact info'],
                'icons': ['house', 'robot', 'briefcase', 'phone']
                }

    with st.sidebar:
        selected = option_menu(
            menu_title=side_bar['menu_title'],
            options=side_bar['options'],
            icons=side_bar['icons'],
            menu_icon="cast",
            default_index=0,
        )
    # st.sidebar.title("Navigation")
    # page = st.sidebar.radio("Go to", ["CV", "Chatbot"])

    if selected == "Home":
        display_introduction()
    elif selected == "Chatbot":
        st.markdown(
            '''<h1 style="text-align: center; font-family: monospace;">CV Chatbot</h1>''',
            unsafe_allow_html=True)
        show_faq()
        user_input = st.text_input("")
        send_button = st.button("Get to know Eyal")
        if send_button:
            response = chat_with_gpt(user_input)
            st.write(response)
    elif selected == "Professional Experience":
        display_cv()
    elif selected == "Education":
        display_education()
    elif selected == "Skills & Hobbies":
        display_skills()
    elif selected == "Contact info":
        display_contact()


if __name__ == "__main__":
    main()