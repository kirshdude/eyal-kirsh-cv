import plotly.graph_objects as go
import streamlit as st
from all_cv_text import all_text
from connectors.connection_manager import ConnectionManager

connection_manager = ConnectionManager(model='gpt-4o')
open_ai = connection_manager.open_ai_connection


class JobMatcher:
    def __init__(self, job_description, job_seeker_info) -> None:
        self.job_recruiter_info = job_description
        self.job_seeker_info = job_seeker_info
        self.general_qualifications = ['professional experience', 'educational qualifications', 'professional skills and abilities', 'Personality profile']
        self.job_recruiter_requirements = self.find_all_relevant_parts(is_seeker=False)
        self.job_seekers_qualifications = self.find_all_relevant_parts(is_seeker=True)
        self.matching_scores = self.get_matching_scores()


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

    def create_requirement_finder_prompt(self, qualification: str, is_seeker: bool):
        if is_seeker:
            content = """Here is info about a job seeker: {job_description} 
                         Follow the following steps to complete the task:
                        1. find the information about the job seeker that contain informaion about his {qualification}
                            *try to infer if the information is not explicitly written (for example, if you need to find professional skills look for skills in all parts of the iformation and not just in the parts that excplicitly say skills)
                        2. summarize the information
                        3. return in an organized format the information that was collected and summarized 
                       If there is nothing mentioned about it in the job requirements please return only the word - None
                       """.format(
                job_description=self.job_seeker_info, qualification=qualification)

        else:
             content = "Here is a job requirements file: {job_description} \
                        please find and return only the parts that contain the job's {qualification} requirements. \
                        If there is nothing mentioned about it in the job requirements please return only the word - None".format(
                        job_description=self.job_recruiter_info, qualification=qualification)

        prompt = [
            {
                "role": "system",
                "content": "You are a helpful assistant, please do what is asked from you without doing anything else"
            },
            {
                "role": "user",
                "content": content

            }
        ]

        return prompt

    def get_job_qualification(self, qualification, is_seeker):
        prompt = self.create_requirement_finder_prompt(qualification, is_seeker=is_seeker)
        llm_reply = open_ai.get_gpt_reply(prompt=prompt)
        # print('-------------------------------------------------------------------------')
        # print(qualification, ':', llm_reply )
        return llm_reply

    def find_all_relevant_parts(self, is_seeker):
        job_qualifications = {}
        for qual in self.general_qualifications:
            job_qualifications[qual] = self.get_job_qualification(qual, is_seeker=is_seeker)
        return job_qualifications

    def match_score_prompt(self, criteria, job_recruiter_requirement, job_seekers_qualification):
        response_format = '''{"criteria match": <matching percentage>, "reason": <the reason for the percentage>}'''
        prompt = [
            {
                "role": "system",
                "content": "You are a job recruiter, please be helpful"
            },
            {
                "role": "user",
                "content": """I have a job requirement about {criteria} and a job seeker's qualifications. 
                            Here are the job recruiter's requirement: {job_recruiter_requirement} 
                            Here are the job seeker's qualifications: {job_seekers_qualification} 
                            Please return a percentage between 0 and 100 that represents the amount that the job seeker matches the jobs requirements and the reason why. 
                            
                            If the job recruiter's requirement is None and the job's seeker's qualifications is not None then return 100% 
                            If the job recruiter's requirement is NOT none and the job's seeker's qualifications is None then return 0%
                            If the job recruiter's requirement and the job's seeker's qualifications are None then return 0%
                            
                            Return only in the following json format: {response_format}

                            """.format(criteria=criteria,
                                       job_recruiter_requirement=job_recruiter_requirement,
                                       job_seekers_qualification=job_seekers_qualification,
                                       response_format=response_format)



            }
        ]

        return prompt

    def get_match_score(self, criteria, job_recruiter_requirement, job_seekers_qualification):
        prompt = self.match_score_prompt(criteria, job_recruiter_requirement, job_seekers_qualification)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        llm_reply = open_ai.get_gpt_reply(prompt=prompt)
        print(criteria,llm_reply)
        return llm_reply

    def get_matching_scores(self):
        matches = {}
        for qual in self.general_qualifications:
            matches[qual] = self.get_match_score(qual, self.job_recruiter_requirements[qual], self.job_seekers_qualifications[qual])




