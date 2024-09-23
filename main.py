from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import os
from autogen.agentchat import GroupChat, AssistantAgent, GroupChatManager
from autogen.oai.openai_utils import config_list_from_dotenv
 
# Mem = []
 
# Relv = """School Secondary level till Post Graduation,
# covering all disciplines, to be made available
# on the SWAYAM platform. ii. Repurposing of
# e-content courses already developed under
# NMEICT to fit into SWAYAM Pedagogy /
# Andra gogy. iii. Develop India MOOCs platform
# named as SWAYAM (Study Webs  of Active -
# learning  for Young  Aspiring  Minds) for hosting
# and running thousands of courses
# simultaneously. iv. Provide robust Internet
# Cloud (with CDN) and sufficient bandwidth for
 
# ALL INDIA COUNCIL FOR TECHNICAL EDUCATION (AICTE ), NEW DELHI  
# SWAYAM Cell  
# FREQUENT LY ASKED QUESTION S (FAQ)  
# Sl.
# No. Question s Answer s
# [A] ABOUT SWAYAM  
# 1.  What is SWAYAM?  
# SWAYAM (Study Webs of Active -learning for
# Young Aspiring Minds); India Chapter of
# Massive Open Online Courses. SWAYAM is an
# indigenous developed IT platform, initiated by
# Government of India, which is instrumental
# for self -actualisation providing opportunities
# for a life -long learning.
 
# all disciplines. ii. Repurposing of e -content
# courses numbering 1400 already developed
# under NMEICT to fit into SWAYAM Pedagogy /
# Andragogy. iii. Develop India MOOCs platform
# named as SWAYAM (Study Webs  of Active -
# learning  for Young  Aspiring  Minds) for hosting
# and running about 2000 courses and
# repeating  it three times during a year. iv.
# INFO:sentence_transformers.SentenceTransformer:Use pytorch device_name: mps
# INFO:sentence_transformers.SentenceTransformer:Load pretrained SentenceTransformer: sentence-transformers/all-mpnet-base-v2"""
 
 
# PROBLEM = """Question:"what is swayam?" Answer :"SWAYAM stands for Study Webs of Active-learning for
# Young [pause 2sec] Aspiring umm Minds is is India Chapter of
# Massive Open Online Courses  [Unintelligible] is an
# indigenous developed mm mm IT platform, initiated by
# Government of India [pause 4.2sec] which is instrumental
# for self-actualisation providing opportunities
# for a for a life-long learning" """
 
# # PROBLEM = """Question:"what is swayam?" Answer :"My name is Nooh Ali, I'm working as a datascience intern at SWAYAM"""
 
# doc = """School Secondary level till Post Graduation,
# covering all disciplines, to be made available
# on the SWAYAM platform. ii. Repurposing of
# e-content courses already developed under
# NMEICT to fit into SWAYAM Pedagogy /
# Andra gogy. iii. Develop India MOOCs platform
# named as SWAYAM (Study Webs  of Active -
# learning  for Young  Aspiring  Minds) for hosting
# and running thousands of courses
# simultaneously. iv. Provide robust Internet
# Cloud (with CDN) and sufficient bandwidth for
 
# ALL INDIA COUNCIL FOR TECHNICAL EDUCATION (AICTE ), NEW DELHI  
# SWAYAM Cell  
# FREQUENT LY ASKED QUESTION S (FAQ)  
# Sl.
# No. Question s Answer s
# [A] ABOUT SWAYAM  
# 1.  What is SWAYAM?  
# SWAYAM (Study Webs of Active -learning for
# Young Aspiring Minds); India Chapter of
# Massive Open Online Courses. SWAYAM is an
# indigenous developed IT platform, initiated by
# Government of India, which is instrumental
# for self -actualisation providing opportunities
# for a life -long learning.
 
# all disciplines. ii. Repurposing of e -content
# courses numbering 1400 already developed
# under NMEICT to fit into SWAYAM Pedagogy /
# Andragogy. iii. Develop India MOOCs platform
# named as SWAYAM (Study Webs  of Active -
# learning  for Young  Aspiring  Minds) for hosting
# and running about 2000 courses and
# repeating  it three times during a year. iv.
# INFO:sentence_transformers.SentenceTransformer:Use pytorch device_name: mps
# INFO:sentence_transformers.SentenceTransformer:Load pretrained SentenceTransformer: sentence-transformers/all-mpnet-base-v2"""
 
def output(Mem,PROBLEM,doc,
           Relv):
    config_list = [
        {"api_type": "groq", "model": "llama3-70b-8192", "api_key": os.getenv("Groq_API"), "cache_seed": None}
    ]
    
    def termination_msg(x):
        return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
    
    llm_config = {"config_list": config_list, "timeout": 60, "temperature": 0.8, "seed": 1234}
    
    Boss = RetrieveUserProxyAgent(
        name="Boss",
        is_termination_msg=termination_msg,
        system_message= "You retrieve information whenever TruthChecker agent wants it.",
        human_input_mode="NEVER",
        default_auto_reply="Reply `TERMINATE` if the task is done.",
        max_consecutive_auto_reply=3,
        retrieve_config={
            "task": "qa",
            "docs_path": doc,
            "chunk_token_size": 1000,
            "model": config_list[0]["model"],
            "collection_name": "groupchat",
            "get_or_create": True,
        },
        code_execution_config=False,
        description="""Can retrieve extra content for solving difficult problems.
        Provide retrieved information to `TruthChecker` only.""")
    
    RelevanceVerifier = RetrieveUserProxyAgent(
        name="RelevanceVerifier",
        is_termination_msg=termination_msg,
        system_message=""" You retrieve information whenever RelevanceAgent wants it.""",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        retrieve_config={
            "task": "qa",
            "docs_path": Relv,
            "chunk_token_size": 1000,
            "model": config_list[0]["model"],
            "collection_name": "groupchat",
            "get_or_create": True,
        },
        code_execution_config=False,
        description= """Can retrieve extra content for solving difficult problems.
        Acts immediately after Boss"""
    )
    
    RelevanceAgent = AssistantAgent(
        name="RelevanceAgent",
        is_termination_msg=termination_msg,
        system_message="""RelavanceVerifier:
        Need to verify that the ANSWER given in `Boss`  is relevant
        to the QUESTION according to the data you will get from `RelevanceVerifier`
    
        If the answer's is relavency less than 20%, output format is:
        "IRRELAVENT"
    
        If the answer is relavent more than 20%, output format is:
        "Relavance Score: <20.01 - 100> / 100
        * <if there is any irrelavent content in the answer, List them and suggest them to remove it.
        Else don't give this point>
        * <if there is any relavent content missing in the answer, List them and suggest them to add it.
        Else don't give this point>"
 
        Note Before:
        - Ignore square brackets in the answer part and content in it.
        - Do not comment on filler words or grammer mistakes or pauses.
        """,
        llm_config=llm_config,
        description="""Take information from RelevanceVerifier only. Acts immediately after Relevance Verifier.""",
    )
    
    TruthChecker = AssistantAgent(
        name="TruthChecker",
        is_termination_msg=termination_msg,
        system_message="""Truthfulness Checker:
        `Boss` have a DOCUMENT and `Boss` message have PROBLEM. PROBLEM contains Question
        and Answer (answer is text converted from audio). Document contains part
        of texts relavent to given question from reliable source, retrieve information from it.
    
        Verify the answer's truthfulness against the document.
        Provide a score out of 100 based on accuracy and truthfulness.
    
        Output Format:
        "Truthfulness score: <1.00-99.99>/100
        * <If there is any factually in correct statements:
        List each factaully incorrect statements and mention the statement
        from the document which is contradictory to the incorrect statement.
        Else don't give this point>
        * <If there is any statement which can't be verified: Assume its true
        and mention you have assumed so. Else don't give this point>
        * <If there is any contradictory statement with in the answer:
        point out these statements from answer are contradictory,
        Else don't give this point>"
        *<points in the output of `RelevanceAgent`, if there exists. Else don't give this point>
    
        **Note Before:**
        - Ignore square brackets in the answer part and content in it.
        - Always ensure you include the points in RelevanceAgent in your output.
        - Do not summarise or comment on other agents' feedback excluding `RelevanceAgent`. Stick strictly to truthfulness assessment. """,
        llm_config=llm_config,
        description=""" I can only speak 2 times and I am **ONLY** allowed to speak in two cases:
        - immediately after `RelevanceAgent` if output of `RelevanceAgent` is  "RELEVANT"
        - immediately after `CommunicationCoach` **only** if value of alpha is not three""",
    )   
    
    FluencyReviewer = AssistantAgent(
        name="FluencyReviewer",
        is_termination_msg=termination_msg,
        system_message=f"""Fluency Reviewer:
        `Boss` message have PROBLEM. PROBLEM contains Question
        and Answer (answer is text converted from audio).
        Review the Answer text converted from audio to verify its fluency and clarity.
        
        In both cycles:
        1. Point out any filler words, repetitive words, pauses, or unclear phrases.
        2. Provide a fluency score out of 100.
        
        Output format:
        "Fluency score: <0.00-100>/100
        * <list filler words and suggest alternatives if filler word exists. Else don't give this point.>
        * <list Repetitive words and suggest alternatives if repetitive word exist. Else don't give this point.>
        * <pause in square bracket means there is pause of specified length.
        list pauses with their length and position (Mention phrase before and after it),
        if pause exists. Else don't give this point. >
        * <unIntelligible in square bracket means phrase there is not clear. list all the places where
        phrases were unclear if unclear phrase exists. Else don't give this point.>
    
        Note: Don't give any other comments, stick to what is instructed.""",
        llm_config=llm_config,
        description="I am **ONLY** allowed to speak immediately after `TruthChecker`",
    )
    
    CommunicationCoach = AssistantAgent(
        name="CommunicationCoach",
        is_termination_msg=termination_msg,
        system_message=""" Communication Coach: Review the text converted from audio focusing on
        language appropriateness, grammar, engagement, and positivity.
        
        In both cycles:
        1. Identify cuss words, inappropriate language, or informal words.
        2. Correct any grammar errors.
        3. Provide suggestions to enhance engagement and positivity if needed.
        4. Increment the value of alpha by one
        
        Output format:
        "Communication Score: <0.00-100>/100
        * <list inappropriate words and suggest its alternatives, if inappropriate word exists. Else don't give this point>
        * <list the informal phrase and suggest its alternatives, if informal phrase exists. Else don't give this point>
        * <list grammatical errors and corrections, if grammer error exists. Else don't give this point>
        * <if the answer is either boring or negative, suggest how to make it engaging and positive. Else don't give this point>
    
        Note Before:
        - Ignore square brackets and content within them.
        - Do not summarise or comment on other agents' feedback. Stick strictly to instructions.
        """,
        llm_config=llm_config,
        description="I am **ONLY** allowed to speak **immediately** after `FluencyReviewer`.",
    )
    
    Club_up = AssistantAgent(
        name="Club_up",
        is_termination_msg=termination_msg,
        system_message=f"""Club_up Agent: Club up all the reviews from other agents.
        if `CommunicationCoach` was the previous Agent:
        Mem = {Mem}
            Tasks:
            1. Give an overall score.
            2. Compile all results from TruthChecker, FluencyReviewer, and CommunicationCoach.
            3. If `Mem` is not empty, compare the current review with previous reviews. Provide an analysis of
            progress or regress, noting repeated mistakes or improvements.
    
            Output format:
            "Overall Score: <Average of Truthfulness score, Fluency score, Communication Score> / 100
            Truthfulness score <Truthfulness score> / 100 | Fluency score : <Fluency score> / 100 | Communication Score : <Communication score> / 100
            * <list all the points in `TruthChecker` agent without mentioning the score>
            * <list all the points in `FluencyReviewer` agent without mentioning the score>
            * <list all the points in `CommunicationCoach` agent without mentioning the score>
            * <`Mem` contains the prevoius summary. if `Mem` is empty, don't give this point.
            Else, compare the current review with previous reviews. Provide an analysis of
            progress or regress, noting repeated mistakes or improvements.>"
        if `RelevanceAgent` is the previous agent and it output was "IRRELEVANT":
            Give the below output as it:
                "Your answer is completely irrelevant to the question you have selected. Recheck your question or answer and Try again"
        Note Before: Don't speak anything beyound output format. Don't speak things like this is the case so output is this, just stick to output format
        """,
        llm_config=llm_config,
        description=""" I am **ONLY** allowed to speak in two cases:
        - **immediately** after `RelevanceAgent` if output of `RelevanceAgent` is "IRRELEVANT"
        - **immediately** after `CommunicationCoach` if value of alpha is three""",
    
    )
    
    
    graph_dict = {}
    graph_dict[Boss] = [RelevanceVerifier]
    graph_dict[RelevanceVerifier] = [RelevanceAgent]
    graph_dict[RelevanceAgent] = [Club_up,TruthChecker]
    graph_dict[TruthChecker] = [FluencyReviewer]
    graph_dict[FluencyReviewer] = [CommunicationCoach]
    graph_dict[CommunicationCoach] = [Club_up,TruthChecker]
    
    agents = [Boss,RelevanceVerifier,RelevanceAgent,TruthChecker,FluencyReviewer,CommunicationCoach,Club_up]
    
    group_chat = GroupChat(agents=agents, messages=[], max_round=10, allowed_or_disallowed_speaker_transitions=graph_dict, speaker_transitions_type="allowed")
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        system_message= """You are deciding whom to speak next. Follow the below instructions and select whom to speak:
        - first go through `RelevanceVerifier` and `RelevanceAgent`.
        - if `RelevanceAgent`'s output is "IRRELEVANT", go to `Club_up`.
        - Else go in the following order: `TruthChecker` then `FluencyReviewer` then `CommunicationCoach` then `TruthChecker`
        then `FluencyReviewer` then `CommunicationCoach` then `Club_up`.
        Note before: `TruthChecker` can speak only 2 times. If `CommunicationCoach` speak twice, then `Club_up` should speak. """
    )
    
    chat_hist = Boss.initiate_chat(
        manager,
        message=f"""Please review the following answer to the question in two cycles:
    
            {PROBLEM}
            
 
            alpha is a variable and its value is integer one
            First, `RelevanceAgent` will speak.
            
            If the `RelevanceAgent`'s output is not "IRRELEVANT":
    
                Cycle 1: `TruthChecker`, `FluencyReviewer`, and `CommunicationCoach`, please review this original answer independently.
                Cycle 2: `TruthChecker`, `FluencyReviewer`, and `CommunicationCoach` review the original answer again, providing an updated analysis.
        
                After both cycless, `Club_up` will club up all the points from the last cycle and
                if `Mem` is not empty, give an comparison analysis.
                Then terminates
    
            If the `RelevanceAgent`'s output is not "IRRELEVANT":
                immediately go to `Club_up` and it will terminates. """,
        clear_history=True
    )
    return chat_hist