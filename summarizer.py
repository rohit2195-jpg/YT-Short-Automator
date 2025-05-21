from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()
def summarizer(article):

    class ResearchResponse(BaseModel):
        topic: str
        summary: str
        sources: list[str]
        tools_used: list[str]


    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                Please summarize the given content and be informative about the details.
                Please summarize these news article and be informative about current events.
                Make the script engaging for short from content, like a youtube short, but don't lose a proffesional tone. 
                Your goal is reveal information little by little to get them reading to the end of the script, without them knowing it.
                Keep the script around 45 seconds to 1 minute. 
                Listen to the following instructions carefully
                Do not include any additional formatting or behind the scenes material, just write plain text for the script.
                Do not include any new lines, make it simply plain text.
                Please respond in plain text only, no formatting, no special characters like italics or bold.
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=[]
    )

    agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
    query = article
    raw_response = agent_executor.invoke({"query": query})
    print(raw_response)
    print("hellow")
    print(raw_response["output"])

    return str(raw_response["output"]) + "\n" + str(raw_response["query"])

