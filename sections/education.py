import streamlit as st

education_header = "Formal Education"

educations = """
- **Tel Aviv University**: Industrial Engineering & Management (B.Sc.), 2018-2022
- **Naya College**: Practical Data Science, 2022-2023
  - Comprehensive course covering the entire data science lifecycle
  - Completed projects in regression, classification, and NLP
"""

def display_education():
    st.header(education_header)
    st.write(educations)
