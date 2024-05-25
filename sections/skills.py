import streamlit as st

skills_title = "Skills"
skills = """
- Python, SQL, Excel, Tableau, Git
- Classification, Regression, NLP, DL
- Excellent communication skills
- Native English & Hebrew
"""

hobbies_title = "Activities & Interests"
hobbies = """
- Tennis enthusiast
- Entrepreneurship
- Dog frisbee competitions
"""

def display_skills():
    st.header(skills_title)
    st.write(skills)

    st.header(hobbies_title)
    st.write(hobbies)