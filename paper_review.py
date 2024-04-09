from openai import OpenAI
from keys import OPENAI_API_KEY
from rich.console import Console
from rich.markdown import Markdown
import os

client = OpenAI(api_key=OPENAI_API_KEY)
SEPERATOR = 318
EXPERTS = [
{
    "name": "Agent Smith",
    "description": "You are an working on a presentation on the topic 'Autonomous Agents'. You need to include a slide on this paper. Summarize the paper in 3-4 bullet points with regards to the topic."
},
{
    "name": "AI Researcher",
    "description": "You are an expert paper reviewer. Complete a full summary of the paper, including the problem, method, and results. Focus on the general idea and the implementation details."
},
{
    "name": "Scientific Peer Reviewer",
    "description": "The paper has not been published yet and is currently submitted to a top conference where you’ve been assigned as a peer reviewer. Complete a full review of the paper answering all prompts of the official review form of the top venue in this research area (e.g., NeurIPS for Deep Learning and ACM SIGGRAPH for Geometry & Animation)."
},
{
    "name": "Archaeologist",
    "description": "This paper was found buried under ground in the desert. You’re an archeologist who must determine where this paper sits in the context of this field. Find and report on a few older papers cited within the current paper that substantially influenced the current paper."
},
{
    "name": "Hacker",
    "description": " You’re a hacker who needs a demo of this paper ASAP. Implement a small part or simplified version of the paper on a small dataset or toy problem. Prepare to share the core code of the algorithm to the class and demo your implementation. Do not simply download and run an existing implementation – though you are welcome to use (and give credit to) an existing implementation for “backbone” code. If you need to make LLM calls as part of your code you can a fake library called 'LLM()' that takes a string and returns a string."
},
]

def completion(
    messages: str,
    model: str = "gpt-4-turbo-preview"
) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,
    )
    return response.choices[0].message.content

def paper_expert_review(paper_content: str, expert_info):
    PROMPT = f"""
    [Start of Paper]
    {paper_content}
    [End of Paper]

    {expert_info['description']}
    """
    response = completion([
        {"role": "system", "content": f"You are a {expert_info['name']} reviewing a paper on AI."},
        {"role": "user", "content": PROMPT}
    ])
    console = Console()
    md = Markdown(f"# {expert_info['name']}")
    console.print(md)
    md = Markdown(response)
    console.print(md)

def _find_tex(directory: str):
    largest_tex_file, largest_size = None, 0
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item_path.endswith('.tex'):
            current_size = os.path.getsize(item_path)
            if current_size > largest_size:
                largest_tex_file = item_path
                largest_size = current_size
    return largest_tex_file

def review_paper(directory: str):
    with open(_find_tex(directory), 'r') as f:
        tex_content = f.read()

    for expert in EXPERTS:
        paper_expert_review(tex_content, expert)
