import streamlit as st

name = 'Eyal Kirsh'

def display_introduction(name):
    st.markdown('''<h1 style="text-align: center;">Welcome to {name}'s Interactive CV</h1>'''.format(name=name), unsafe_allow_html=True)
             #f"Welcome to {name}'s Interactive CV")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
        <p style="text-align: left; font-size: large; color: black;">
            Please feel free to browse the different sections about {name}.<br>
            The Chatbot is here to help you get any additional information you might be interested in that is not explicitly writtin in the CV</b>.
        </p>
    </div>
    """.format(name=name), unsafe_allow_html=True)