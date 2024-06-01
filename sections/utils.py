def llm_verifier(input, output):
    system_content = "You are a quality assurance specialist"
    user_content = """You will be provided with a task and an output from another LLM for that task.
                    You need to verify the output is in the format that was specified in the original task requierments.
                    If the output is not in the proper format (for example: json, list function ect.) fix the output and return it with no additional info.
                    If everything is correct just return the original output
                    Do not explain your output and don't add any additional text that is not specifically needed for the original task.
                    Here hs the task: {input}
                    And here is the original output: {output}
                    """.format(input=input, output=output)
    prompt = self.create_prompt(system_content=system_content, user_content=user_content)
    verified_output = self.get_llm_reply(prompt)
    return verified_output


def json_verifier(json):
    system_content = "You are a quality assurance specialist"
    user_content = """Please make sure the following is in a proper json format, if not fix it:
                      {json}
                        """.format(json=json)
    prompt = self.create_prompt(system_content=system_content, user_content=user_content)
    verified_output = self.get_llm_reply(prompt)
    return verified_output