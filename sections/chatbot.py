import streamlit as st
from all_cv_text import all_text
from connectors.connection_manager import ConnectionManager

connection_manager = ConnectionManager()
open_ai = connection_manager.open_ai_connection

def create_prompt(all_text, query):
    main_prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant, help the employer with any question they have about the  candidates CV "
        },
        {
            "role": "user",
            "content": f"This is the cv: {all_text} please answer the following question: {query}. Please try to answer in a clean and clear manner using bullet points if needed"
        }
    ]
    return main_prompt

def chat_with_gpt(query):
    prompt = create_prompt(all_text, query)
    chat_reply = open_ai.get_gpt_reply(prompt=prompt)

    return chat_reply

def show_faq():
    faq = '''
    Here are some ideas of questions you can ask about Eyal:
    - What are Eyal's Professional strengths?
    - What education does Eyal have?
    - Why would Eyal be/not be a good fit for role X? 
    - What is Eyal's phone number?
    - Describe Eyal in 3 sentences
        '''


    st.markdown("""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
            <p style="text-align: left; font-size: large; color: black; font-family: monospace;">
                The Chatbot is here to help you get any additional information you might be interested in that is not explicitly writtin in the CV.<br>
           <p style="text-align: left; font-size: large; color: black; font-family: monospace;">    
    <b>Here are some ideas of questions you can ask about Eyal:</b><br>
    1. What are Eyal's Professional strengths? <br>
    2. What education does Eyal have? <br>
    3. Why would Eyal be/not be a good fit for role X? <br>
    4. Give me Eyal's GitHub URL<br>
    5. Describe Eyal in 3 sentences<br>
         </b>
            </p>
        </div>
        """, unsafe_allow_html=True)


    # st.write(faq)