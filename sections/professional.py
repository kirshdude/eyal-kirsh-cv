import streamlit as st

professional_header = "Professional Experience"

professional_experiences = [{'experience': "Data Scientist, Wix.com",
                             "time": "**2022-Present**",
                             "description": """
Managed multiple end-to-end AI & Machine Learning projects, resulting in significant improvement to the business KPIs.
- **Marketplace recommendation system** - Partnered with the product team to build a recommendation system- matching web professionals with clients in Wix’s Marketplace, increasing target KPI (projects’ completion rate) by 15%.
- **AI products** – Took part in internal research and implementation of AI driven applications, such as:
  - **Analytics assistant** – Started as internal research and continued as a personal project to help stakeholders interact with data without the need of an analyst. Developed using the advanced GPT-3.5 Turbo model and a custom-built RAG framework. [GitHub repo](https://github.com/kirshdude/Insight)
  - **Templates quality validation** - Ongoing research to validate templates’ visual and textual quality before approving it for selling in the Templates Marketplace. The research includes the use of advanced image and text models along with classical ML models.
- **Professional user detection** - Implemented a Catboost model with BERT LLM to increase the detection accuracy of professional users (Design agencies & freelancers) by 25% and reducing detection time to minutes from signup.
"""},

{'experience': "Data Analyst, Wix.com",
                             "time": "**2021-2022**",
                             "description": """
    - Created in depth analysis of key business questions, producing insights that had major impact on the business.
    - Ran, monitored, and analyzed numerous A/B tests.
    - Created and owned data pipelines for several projects using SQL and Python.
    """},


{'experience': "Co-Founder & CEO, Ayalim",
                             "time": "**2017-2021**",
                             "description": """
    - Founded Ayalim, an English and math tutoring school. Developed and scaled it to hundreds of memberships over a few locations.
    - Developed the business strategy, which allowed for speedy growth (40% YoY), while staying highly profitable.
    - Sold the company in July 2021 after handling in-depth negotiations and oversaw the legal and financial due diligence.
    """},


{'experience': "Military Service, Yahalom Special Unit Forces",
                             "time": "**2012-2015**",
                             "description": """
    - Served in the Bomb Squad as a combat field commander in complex operational missions. Ranked first in my program.
    - Led a team of soldiers in the battle of Tzuk Eitan and received a medal of honor for outstanding leadership and courage.
    """}

                            ]


def display_cv():
    st.title(professional_header)
    for exp in professional_experiences:
        st.header(exp['experience'])
        time = exp["time"]
        st.write('<p style="font-size: large;">{time}</p>'.format(time=time), unsafe_allow_html=True)

        description = exp['description']
        st.write(description)