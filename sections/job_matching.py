import plotly.graph_objects as go
import streamlit as st
from connectors.connection_manager import ConnectionManager
import json
import time



connection_manager = ConnectionManager(model='gpt-4o')
open_ai = connection_manager.open_ai_connection


class JobMatcher:
    def __init__(self, job_description, job_candidate_info) -> None:
        self.job_recruiter_info = job_description
        self.job_candidate_info = job_candidate_info
        self.general_qualifications = ['professional experience', 'educational qualifications', 'professional skills and abilities', 'Personality profile']
        self.progress_text = "This will take a few moments, thank you for your patience"
        self.my_bar = st.progress(0, text=self.progress_text)

        self.job_recruiter_requirements = self.find_all_relevant_parts(is_candidate=False)
        self.my_bar.progress(30, text="Analyzing job requirements")

        self.job_candidates_qualifications = self.find_all_relevant_parts(is_candidate=True)
        self.my_bar.progress(60, text="Analyzing candidate's info")





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
            '''<h1 style="text-align: center; font-family: monospace;"> Role & Candidate Match</h1>''',
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

    def create_requirement_finder_prompt(self, qualification: str, is_candidate: bool, requirements=None):
        system_content = "You are a helpful assistant, please do what is asked from you without doing anything else"
        if is_candidate:
            user_content = """Here is info about a job candidate: {candidate_info} 
                         Follow the following steps to complete the task:
                        1. find the information about the job candidate that contain information about his {qualification}
                            that is relevant for these requirements: {requirements}
                            *try to infer if the information is not explicitly written (for example, if you need to find professional skills look for skills in all parts of the iformation and not just in the parts that excplicitly say skills)
                        2. summarize the information
                        3. return in an organized format the information that was collected and summarized 
                       If there is nothing mentioned about it in the job requirements please return only the word - None
                       """.format(candidate_info=self.job_candidate_info, qualification=qualification, requirements=requirements)

        else:
             user_content = "Here is a job requirements file: {job_description} \
                        please find and return only the parts that contain the job's {qualification} requirements. \
                        If there is nothing mentioned about it in the job requirements please return only the word - None".format(
                        job_description=self.job_recruiter_info, qualification=qualification)

        prompt = self.create_prompt(system_content=system_content, user_content=user_content)

        return prompt

    def get_job_qualification(self, qualification, is_candidate, requirements):
        prompt = self.create_requirement_finder_prompt(qualification=qualification, is_candidate=is_candidate, requirements=requirements)
        llm_reply = self.get_llm_reply(prompt=prompt)
        return llm_reply

    def find_all_relevant_parts(self, is_candidate):
        job_qualifications = {}
        for qual in self.general_qualifications:
            if is_candidate:
                job_qualifications[qual] = self.get_job_qualification(qualification=qual, is_candidate=is_candidate, requirements=self.job_recruiter_requirements[qual])
            else:
                job_qualifications[qual] = self.get_job_qualification(qualification=qual, is_candidate=is_candidate, requirements=None)
        return job_qualifications

    def match_score_prompt(self, criteria, job_recruiter_requirement, job_candidates_qualification):
        response_format = '''{"criteria match": <matching percentage>, "reason": <the reason for the percentage>}'''
        system_content = "You are a job recruiter, please be helpful"
        user_content = """I have a job requirement about {criteria} and a job candidate's qualifications. 
                            Here are the job recruiter's requirement: {job_recruiter_requirement} 
                            Here are the job candidate's qualifications: {job_candidates_qualification} 
                            Please return a percentage between 0 and 100 that represents the amount that the job candidate matches the jobs requirements and the reason why. 
                            
                            If the job recruiter's requirement is None and the job's candidate's qualifications is not None then return 100% and in the reason just write: Candidate meets the requierments  
                            If the job recruiter's requirement is NOT none and the job's candidate's qualifications is None then return 0%and in the reason just write: Candidate doesn't meets the requierments
                            If the job recruiter's requirement and the job's candidate's qualifications are None then return 100% and in the reason just write: Candidate meets the requierments  
                            
                            Return only in the following json format: {response_format}

                            """.format(criteria=criteria,
                                       job_recruiter_requirement=job_recruiter_requirement,
                                       job_candidates_qualification=job_candidates_qualification,
                                       response_format=response_format)

        prompt = self.create_prompt(system_content=system_content, user_content=user_content)
        return prompt

    def json_verifier(self, input_string):
        input_string = str(input_string)
        # Find the start and end of the JSON content
        start_index = input_string.find('{')
        end_index = input_string.rfind('}') + 1
        # Extract the JSON content
        json_content = input_string[start_index:end_index]
        # Convert the JSON string to a dictionary
        try:
            input_dict = json.loads(json_content)
        except:
            fixed_json_content = self.llm_json_verifier(json_content)
            input_dict = json.loads(fixed_json_content)
        return input_dict

    def llm_json_verifier(self, json):
        system_content = "You are a quality assurance specialist"
        user_content = """Please make sure the following is in a proper json format, if not fix it:
                          {json}
                          return only the json and nothing else
                            """.format(json=json)
        prompt = self.create_prompt(system_content=system_content, user_content=user_content)
        verified_output = self.get_llm_reply(prompt)
        return verified_output

    def get_match_score(self, criteria, job_recruiter_requirement, job_candidates_qualification):
        prompt = self.match_score_prompt(criteria, job_recruiter_requirement, job_candidates_qualification)
        llm_reply = self.get_llm_reply(prompt=prompt)
        clean_output = self.json_verifier(llm_reply)
        return clean_output

    def get_matching_scores(self):
        matches = {}
        for qual in self.general_qualifications:
            matches[qual] = self.get_match_score(qual, self.job_recruiter_requirements[qual], self.job_candidates_qualifications[qual])
        self.my_bar.progress(90, text="Calculating the match")
        return matches

    def show_matching_gouge(self):
        matches = self.get_matching_scores()
        print(matches)
        self.my_bar.progress(100, text="Finalizing a fewe things")
        time.sleep(1)
        self.my_bar.empty()
        score = sum(
            criteria["criteria match"] if isinstance(criteria, dict) else dict(criteria)["criteria match"]
            for criteria in matches.values()
        ) / len(matches)
        # score = sum(criteria["criteria match"]  for criteria in matches.values() ) / len(matches.values())

        st.title("Eyal's match for this job")
        st.plotly_chart(self.create_gauge_chart(score))
        st.header('Score Explanation')
        for criteria in matches.keys():
            st.header(criteria.capitalize())
            st.write('<p style="font-size: Medium;">Score: {the_score}</p>'.format(the_score=str(matches[criteria]['criteria match'])), unsafe_allow_html=True)
            # st.write('Matching score:' + str(matches[criteria]['criteria match']))
            st.write('<p style="font-size: Medium;">Reason: \n {reason}</p>'.format(reason=str(matches[criteria]['reason'])), unsafe_allow_html=True)

            # st.write('Reason:'+str(matches[criteria]['reason']))





