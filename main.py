from all_cv_text import all_text
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components


import sections
from sections.home import display_introduction
from sections.professional import display_cv
from sections.education import display_education
from sections.skills import display_skills
from sections.contact import display_contact
from sections.chatbot import chat_with_gpt, show_faq
from sections.job_matching import JobMatcher


# Streamlit app layout
def main():
    side_bar = {'menu_title': 'Eyal Kirsh CV',
                'options': ['Home', 'Chatbot', 'Professional Experience', 'Matching score', 'Contact info'],
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
        display_introduction()
    elif selected == "Chatbot":
        st.markdown(
            '''<h1 style="text-align: center; font-family: monospace;">CV Chatbot</h1>''',
            unsafe_allow_html=True)
        show_faq()
        st.markdown("")
        user_input = st.text_input("What would you like to know?")
        send_button = st.button("Get to know Eyal")
        if send_button:
            response = chat_with_gpt(user_input)
            st.write(response)
    elif selected == "Professional Experience":
        display_cv()
    # elif selected == "Education":
    #     display_education()
    # elif selected == "Skills & Hobbies":
    #     display_skills()
    elif selected == "Contact info":
        display_contact()

    elif selected == "Matching score":
        html_code = """
        <div style="display: flex; justify-content: left; padding: 15px; border-radius: 10px;">
            <input type="text" id="largeInput" style="width: 500px; height: 10000px; font-size: 20px; padding: 15px; border-radius: 10px;" placeholder="Enter your text here">
        </div>
        <script>
            // Get Streamlit to capture the input value
            const largeInput = document.getElementById('largeInput');
            largeInput.addEventListener('input', function() {
                window.parent.postMessage({isStreamlitMessage: true, type: 'largeInputValue', value: largeInput.value}, '*');
            });
        </script>
        """

        # Display the custom HTML
        components.html(html_code, height=300)

        job_description = st.text_input("Paste the job description here:")
        send_button = st.button("Get score")
        if send_button:
            job_seekers_info = all_text
            matcher = JobMatcher(job_description, job_seekers_info)
            st.markdown(str(matcher.matching_scores))





if __name__ == "__main__":
    main()