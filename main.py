from all_cv_text import all_text
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

import sections
from sections.home import display_introduction
from sections.professional import display_cv

from sections.contact import display_contact
from sections.chatbot import ChatBot
from sections.job_matching import JobMatcher


# Streamlit app layout
def main():
    side_bar = {'menu_title': 'Eyal Kirsh CV',
                'options': ['Home', 'Chat with Eyal', 'Professional Experience', 'Role Match', 'Contact info'],
                'icons': ['house', 'robot', 'briefcase', 'robot', 'phone']
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
        st.image('Linkedin_photo.jpg', width=277)
        display_introduction()
    elif selected == "Chat with Eyal":
        st.markdown(
            '''<h1 style="text-align: center; font-family: monospace;">Chat with Eyal </h1>''',
            unsafe_allow_html=True)

        chat_bot_class = ChatBot()
        st.markdown("")
        chat_bot_class.run_chat()

    elif selected == "Professional Experience":
        display_cv()
    # elif selected == "Education":
    #     display_education()
    # elif selected == "Skills & Hobbies":
    #     display_skills()
    elif selected == "Contact info":
        display_contact()

    elif selected == "Role Match":
        JobMatcher.intro()
        st.markdown("")
        txt = st.text_area("Paste the job description here:",height=300, placeholder="")

        # job_description = st.text_input("Paste the job description here:")
        send_button = st.button("Get score")
        if send_button:
            job_seekers_info = all_text
            matcher = JobMatcher(txt, job_seekers_info)
            # try:
            matcher.show_matching_gouge()
            # except:
            #     st.header("Seems we ran in to a problem, let's try this again")
            # st.markdown(str(matcher.get_matching_scores()))


if __name__ == "__main__":
    main()