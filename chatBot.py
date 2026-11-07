from dotenv import load_dotenv
load_dotenv()

import json

from fastapi import FastAPI
from langserve import add_routes
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_keenable import KeenableSearch, KeenableFetch
from langchain.tools import tool



search = KeenableSearch()
fetch = KeenableFetch()

@tool
def web_search(query: str) -> str:
    """Search the internet and return up to five relevant results."""

    results = search.invoke({
        "query": query
    })

    # Limit search results
    if isinstance(results, list):
        results = results[:5]

    return json.dumps(
        results,
        default=str
    )[:5000]


# Custom webpage fetch tool
@tool
def web_fetch(url: str) -> str:
    """Fetch and read a webpage using its URL."""

    page = fetch.invoke({
        "url": url
    })

    # Extract Markdown content
    markdown = getattr(page, "markdown", None)

    if markdown is not None: 
        content = getattr(markdown, "data", str(markdown))
    else:
        content = str(page)

    # Limit webpage content
    return str(content)[:6000]


# Register custom tools
tools = [web_search, web_fetch]



llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# tools = [search, fetch]
prompt ="""
You are an AI research assistant.

You have access to two tools:

1. web_search:
   Searches the internet for relevant information.

2. web_fetch:
   Retrieves webpage content from a URL.

Instructions:

- Use web_search for current information.
- Search for reliable and relevant sources.
- Read at most two relevant webpages using web_fetch.
- Do not fetch unnecessary webpages.
- Base your answers on retrieved information.
- Include source URLs in your answers.
- Never invent facts or sources.
- Clearly mention when information cannot be verified.

IMPORTANT RESPONSE RULES:

-Never repeat or paraphrase the user's question unnecessarily.
-Never announce that you are calling, using, or invoking a tool.
-Never describe your internal workflow or intermediate steps.
-Do not display search queries, tool execution logs, or fetched webpage contents directly.
-Use available tools silently whenever required.
-After gathering information, provide only the final synthesized answer.
-Include relevant source URLs when using web search.
-Avoid unnecessary introductions and repetitive conclusions.
-Keep answers focused on what the user actually asked.
-If information is unavailable, clearly say so rather than inventing an answer.
-Your internal tool execution should remain separate from your user-facing response.
"""
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt
)

app = FastAPI(
    title="agentic ai with fastapi"
)

add_routes(
    app,
    agent,
    path="/agent",
    enabled_endpoints=[
    "invoke",
    "batch",
    "stream",
    "stream_log",
    "playground",
    "input_schema",
    "output_schema"
    ]
)

# query = "what is the date today?"

# response = agent.invoke(
#     {"messages":[
#         {"role": "user",
#          "content":query}]}
# )

# print(response["messages"][-1].content)

query = "Explain how FastAPI works"

inputs = {
    "messages": [
        {
            "role": "user",
            "content": query
        }
    ]
}

print("\nAI Response:\n")

for message_chunk, metadata in agent.stream(
    inputs,
    stream_mode="messages"
):

    # Ignore tool execution messages
    if metadata.get("langgraph_node") != "model":
        continue

    # Ignore tool calls
    if getattr(message_chunk, "tool_call_chunks", None):
        continue

    content = message_chunk.content

    if isinstance(content, str) and content:
        print(content, end="", flush=True)

    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block.get("text", ""), end="", flush=True)

print("\n")