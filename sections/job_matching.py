import plotly.graph_objects as go
import streamlit as st
from all_cv_text import all_text
from connectors.connection_manager import ConnectionManager
import json


connection_manager = ConnectionManager(model='gpt-4o')
open_ai = connection_manager.open_ai_connection


class JobMatcher:
    def __init__(self, job_description, job_seeker_info) -> None:
        self.job_recruiter_info = job_description
        self.job_seeker_info = job_seeker_info
        self.general_qualifications = ['professional experience', 'educational qualifications', 'professional skills and abilities', 'Personality profile']
        self.job_recruiter_requirements = self.find_all_relevant_parts(is_seeker=False)
        self.job_seekers_qualifications = self.find_all_relevant_parts(is_seeker=True)
        # self.matching_scores = self.get_matching_scores()

    def get_llm_reply(self, prompt):
        return open_ai.get_gpt_reply(prompt=prompt)

    def create_prompt(self, system_content, user_content):
        prompt = [
                    {
                        "role": "system",
                        "content": system_content
                    },
                    {
                        "role": "user",
                        "content": user_content

                    }
                ]
        return prompt


    @staticmethod
    def intro():
        st.markdown(
            '''<h1 style="text-align: center; font-family: monospace;"> Job Match Score CV</h1>''',
            unsafe_allow_html=True)
        # f"Welcome to {name}'s Interactive CV")
        st.markdown("""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
                    <p style="text-align: left; font-size: large; color: black; font-family: monospace;">
                        This tool analyzes my resume against a job description to provide a compatibility score. </br>
                        <br>
                        This helps you quickly see how well I match the job requirements and if it's a good fit.</br> 
                        <br> 
                        Enjoy! </br> 
                         </p>
                </div>
                """, unsafe_allow_html=True)



# Function to create a gauge chart
    def create_gauge_chart(self, percentage):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=percentage,
            number={'suffix': "%"},  # Add percentage symbol
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "black"},
                   'steps': [{'range': [0, 20], 'color': 'red'},
                             {'range': [20, 40], 'color': 'orange'},
                             {'range': [40, 60], 'color': 'yellow'},
                             {'range': [60, 80], 'color': 'lightgreen'},
                             {'range': [80, 100], 'color': 'green'}],
                   'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.80, 'value': percentage}}))

        fig.update_layout(width=500, height=400)
        return fig

    def create_requirement_finder_prompt(self, qualification: str, is_seeker: bool, requirements=None):
        system_content = "You are a helpful assistant, please do what is asked from you without doing anything else"
        if is_seeker:
            user_content = """Here is info about a job seeker: {seeker_info} 
                         Follow the following steps to complete the task:
                        1. find the information about the job seeker that contain information about his {qualification}
                            that is relevant for these requirements: {requirements}
                            *try to infer if the information is not explicitly written (for example, if you need to find professional skills look for skills in all parts of the iformation and not just in the parts that excplicitly say skills)
                        2. summarize the information
                        3. return in an organized format the information that was collected and summarized 
                       If there is nothing mentioned about it in the job requirements please return only the word - None
                       """.format(seeker_info=self.job_seeker_info, qualification=qualification, requirements=requirements)

        else:
             user_content = "Here is a job requirements file: {job_description} \
                        please find and return only the parts that contain the job's {qualification} requirements. \
                        If there is nothing mentioned about it in the job requirements please return only the word - None".format(
                        job_description=self.job_recruiter_info, qualification=qualification)

        prompt = self.create_prompt(system_content=system_content, user_content=user_content)

        return prompt

    def get_job_qualification(self, qualification, is_seeker, requirements):
        prompt = self.create_requirement_finder_prompt(qualification=qualification, is_seeker=is_seeker, requirements=requirements)
        llm_reply = self.get_llm_reply(prompt=prompt)
        # print('-------------------------------------------------------------------------')
        # print(qualification, ':', llm_reply )
        return llm_reply

    def find_all_relevant_parts(self, is_seeker):
        job_qualifications = {}
        for qual in self.general_qualifications:
            if is_seeker:
                job_qualifications[qual] = self.get_job_qualification(qualification=qual, is_seeker=is_seeker, requirements=self.job_recruiter_requirements[qual])
            else:
                job_qualifications[qual] = self.get_job_qualification(qualification=qual, is_seeker=is_seeker, requirements=None)
        return job_qualifications

    def match_score_prompt(self, criteria, job_recruiter_requirement, job_seekers_qualification):
        response_format = '''{"criteria match": <matching percentage>, "reason": <the reason for the percentage>}'''
        system_content = "You are a job recruiter, please be helpful"
        user_content = """I have a job requirement about {criteria} and a job seeker's qualifications. 
                            Here are the job recruiter's requirement: {job_recruiter_requirement} 
                            Here are the job seeker's qualifications: {job_seekers_qualification} 
                            Please return a percentage between 0 and 100 that represents the amount that the job seeker matches the jobs requirements and the reason why. 
                            
                            If the job recruiter's requirement is None and the job's seeker's qualifications is not None then return 100% 
                            If the job recruiter's requirement is NOT none and the job's seeker's qualifications is None then return 0%
                            If the job recruiter's requirement and the job's seeker's qualifications are None then return 100%
                            
                            Return only in the following json format: {response_format}

                            """.format(criteria=criteria,
                                       job_recruiter_requirement=job_recruiter_requirement,
                                       job_seekers_qualification=job_seekers_qualification,
                                       response_format=response_format)

        prompt = self.create_prompt(system_content=system_content, user_content=user_content)
        return prompt

    # def llm_verifier(self, input, output):
    #     system_content = "You are a quality assurance specialist"
    #     user_content = """You will be provided with a task and an output from another LLM for that task.
    #                     You need to verify the output is in the format that was specified in the original task requierments.
    #                     If the output is not in the proper format (for example: json, list function ect.) fix the output and return it with no additional info.
    #                     If everything is correct just return the original output
    #                     Do not explain your output and don't add any additional text that is not specifically needed for the original task.
    #                     Here hs the task: {input}
    #                     And here is the original output: {output}
    #                     """.format(input=input, output=output)
    #     prompt = self.create_prompt(system_content=system_content, user_content=user_content)
    #     verified_output = self.get_llm_reply(prompt)
    #     return verified_output

    def json_verifier(self, input_string):
        input_string = str(input_string)
        # Find the start and end of the JSON content
        start_index = input_string.find('{')
        end_index = input_string.rfind('}') + 1
        # Extract the JSON content
        json_content = input_string[start_index:end_index]
        # Convert the JSON string to a dictionary
        input_dict = json.loads(json_content)
        return input_dict

    def get_match_score(self, criteria, job_recruiter_requirement, job_seekers_qualification):
        prompt = self.match_score_prompt(criteria, job_recruiter_requirement, job_seekers_qualification)
        llm_reply = self.get_llm_reply(prompt=prompt)
        clean_output = self.json_verifier(llm_reply)
        return clean_output

    def get_matching_scores(self):
        matches = {}
        for qual in self.general_qualifications:
            matches[qual] = self.get_match_score(qual, self.job_recruiter_requirements[qual], self.job_seekers_qualifications[qual])
        return matches

    def show_matching_gouge(self):
        matches = self.get_matching_scores()
        score = sum(i["criteria match"] for i in matches.values()) / len(matches.values())
        print('the score is:', score)
        st.plotly_chart(self.create_gauge_chart(score))




