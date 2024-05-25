from all_cv_text import all_text
import streamlit as st
from streamlit_option_menu import option_menu

import sections
from sections.home import display_introduction
from sections.professional import display_cv
from sections.education import display_education
from sections.skills import display_skills
from sections.contact import display_contact
from sections.chatbot import chat_with_gpt


# Streamlit app layout
def main():
    side_bar = {'menu_title': 'Eyal Kirsh CV',
                'options': ['Home', 'Professional Experience', 'Education', 'Skills & Hobbies', 'Contact & Social', 'Chatbot'],
                'icons': ['house', 'briefcase', 'book', 'tools', 'phone', 'robot']
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
    elif selected == "Professional Experience":
        display_cv()
    elif selected == "Education":
        display_education()
    elif selected == "Skills & Hobbies":
        display_skills()
    elif selected == "Contact & Social":
        display_contact()
    elif selected == "Chatbot":
        st.title("CV Chatbot")
        user_input = st.text_input("Ask a question about Eyal's CV:")
        if user_input:
            response = chat_with_gpt(user_input)
            st.write(response)

if __name__ == "__main__":
    main()