from all_cv_text import all_text
import streamlit as st
import openai
import os
from secret_config import API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

from openai import OpenAI
client = OpenAI()
from sections import name, professional_header, professional_experiences

# Function to display the CV
def display_cv():
    st.title(name)
    st.header(professional_header)

    st.subheader(professional_experiences['experience'])
    st.write(professional_experiences['time'])
    st.write(professional_experiences['description'])

    st.subheader("Data Analyst, Wix.com")
    st.write("2021-2022")
    st.write("""
    - Created in depth analysis of key business questions, producing insights that had major impact on the business.
    - Ran, monitored, and analyzed numerous A/B tests.
    - Created and owned data pipelines for several projects using SQL and Python.
    """)

    st.subheader("Co-Founder & CEO, Ayalim")
    st.write("2017-2021")
    st.write("""
    - Founded Ayalim, an English and math tutoring school. Developed and scaled it to hundreds of memberships over a few locations.
    - Developed the business strategy, which allowed for speedy growth (40% YoY), while staying highly profitable.
    - Sold the company in July 2021 after handling in-depth negotiations and oversaw the legal and financial due diligence.
    """)

    st.subheader("Military Service, Yahalom Special Unit Forces")
    st.write("2012-2015")
    st.write("""
    - Served in the Bomb Squad as a combat field commander in complex operational missions. Ranked first in my program.
    - Led a team of soldiers in the battle of Tzuk Eitan and received a medal of honor for outstanding leadership and courage.
    """)

    st.header("Education")
    st.write("""
    - **Tel Aviv University**: Industrial Engineering & Management (B.Sc.), 2018-2022
    - **Naya College**: Practical Data Science, 2022-2023
      - Comprehensive course covering the entire data science lifecycle
      - Completed projects in regression, classification, and NLP
    """)

    st.header("Details")
    st.write("""
    - **Location**: Tel Aviv, Israel
    - **Phone**: +972-525652543
    - **Email**: kirsheyal@gmail.com
    - **LinkedIn**: [Eyal Kirsh](https://www.linkedin.com/in/eyal-kirsh-81a253a9)
    """)

    st.header("Skills")
    st.write("""
    - Python, SQL, Excel, Tableau, Git
    - Classification, Regression, NLP, DL
    - Excellent communication skills
    - Native English & Hebrew
    """)

    st.header("Activities & Interests")
    st.write("""
    - Tennis enthusiast
    - Entrepreneurship
    - Dog frisbee competitions
    """)


# Function to handle chatbot interaction
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpfull assistant, help the user with any question they have about the CV presented"},
            {"role": "user", "content": f"This is the cv: {all_text} please answer the following question: {prompt}"}
        ]
    )
    return response.choices[0].message.content


# Streamlit app layout
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["CV", "Chatbot"])

if page == "CV":
    display_cv()
elif page == "Chatbot":
    st.title("CV Chatbot")
    user_input = st.text_input("Ask a question about Eyal's CV:")
    if user_input:
        response = chat_with_gpt(user_input)
        st.write(response)
