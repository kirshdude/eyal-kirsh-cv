import streamlit as st

contact_title = "Details"
contact_details = """
- **Location**: Tel Aviv, Israel
- **Phone**: +972-525652543
- **Email**: kirsheyal@gmail.com
- **LinkedIn**: [Eyal Kirsh](https://www.linkedin.com/in/eyal-kirsh-81a253a9)
- **GitHub**: [Projects](https://github.com/kirshdude?tab=repositories)
"""

def display_contact():
    st.header(contact_title)
    st.write(contact_details)

