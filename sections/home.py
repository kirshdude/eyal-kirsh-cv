import streamlit as st

name = 'Eyal Kirsh'

def display_introduction():
    st.markdown('''<h1 style="text-align: center; font-family: monospace;">Eyal's Interactive CV</h1>'''.format(name=name), unsafe_allow_html=True)
             #f"Welcome to {name}'s Interactive CV")
    st.markdown("""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
            <p style="text-align: left; font-size: large; color: black; font-family: monospace;">
                This app is meant to help you, the employer, get to know me better.<br>
                <br>
                I'll just start off by saying that I'm a data scientist passionate about building cool products, <br>
                and I'm highly motivated to work in a startup
            </p>
        </div>
        """, unsafe_allow_html=True)