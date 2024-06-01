import streamlit as st
from streamlit_chat import message

from all_cv_text import all_text
from connectors.connection_manager import ConnectionManager

connection_manager = ConnectionManager()
open_ai = connection_manager.open_ai_connection

from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI()

from langchain_core.prompts import ChatPromptTemplate


class ChatBot:
    def __init__(self) -> None:
        self.user_query = None
        self.submit_button = None
        self.session_state = st.session_state
        self.job_seekers_info = all_text
        self.chain = self.create_chain()
        self.greeting_message = \
""" Hey ! I'm here to help you get any additional information about me that you can't find in my CV 
    
    Here are some ideas of questions you can ask about me: 
    
    1. What are your Professional strengths?
    
    2. What education do you have?
    
    3. Why would you be/not be a good fit for role X? 
    
    4. What is your phone number?
    
    5. Describe yourself in 3 sentences
"""


        if 'history' not in self.session_state:
            self.session_state['history'] = []

        if 'generated' not in self.session_state:
            self.session_state['generated'] = [self.greeting_message]

        if 'past' not in self.session_state:
            self.session_state['past'] = [""]
            # self.session_state['past'] = ["Hey ! 👋"]

        # container for the chat history
        self.response_container = st.container()
        # container for the user's text input
        self.container = st.container()


    def create_chain(self):
        prompt = [("system", "you are Eyal, and you are having a conversation with an employer. he will ask you questions about yourself, answer in a respecful, informal and humble manner. "
                             "You can only answer questions about Eyal and not about other topics"),
                   ("user", f" You are having a conversation with a potential employer, confident and cool "
                            f"This is the information about yourself: {self.job_seekers_info}" + \
                              """please answer the following question: {question}. 
                              Please try to answer in a clean, clear and concise manner without providing unnecessary information.
                              Make it sound that you are a human talking about yourself and not a bot
                              Here is the previous chat history for some context {chat_history}
                              ** Answer only what you were asked about (don't volunteer other info)
                              ** If the question is not about Eyal please explain that you can only help for questions regarding Eyal""")

                ]

        prompt_template = ChatPromptTemplate.from_messages(prompt)
        chain = prompt_template | llm | output_parser
        return chain

    def chat_with_gpt(self):

        result = self.chain.invoke({"question": self.user_query,
                               "chat_history": self.session_state['history'][-2:]})

        st.session_state['history'].append((self.user_query, result))
        # chat_reply = open_ai.get_gpt_reply(prompt=prompt)
        return result

    def show_faq(self):
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

    def run_chat(self):
        # self.show_faq()
        with self.container:
            with st.form(key='input_form', clear_on_submit=True):
                self.user_query = st.text_input("", placeholder="Ask me anything (:", key='input')
                # self.submit_button = st.button("Send")
                self.submit_button = st.form_submit_button(label='Send')

            if self.submit_button and self.user_query:
                output = self.chat_with_gpt()
                self.session_state['past'].append(self.user_query)
                self.session_state['generated'].append(output)
                self.session_state['user_input'] = ''

            if self.session_state['generated']:
                with self.response_container:
                    for i in range(len(self.session_state['generated'])):
                        if i == 0:
                            message(self.session_state["generated"][i], is_user=False, key=str(i),
                                    avatar_style="big-smile")
                        else:
                            message(self.session_state["past"][i], is_user=True, key=str(i) + '_user',
                                    avatar_style="thumbs")
                            message(self.session_state["generated"][i], is_user=False, key=str(i),
                                    avatar_style="big-smile")










