from openai import OpenAI
from keys import OPENAI_API_KEY
from rich.console import Console
from rich.markdown import Markdown

client = OpenAI(api_key=OPENAI_API_KEY)
SEPERATOR = 318
EXPERTS = [
{
    "name": "Scientific Peer Reviewer",
    "description": "The paper has not been published yet and is currently submitted to a top conference where you’ve been assigned as a peer reviewer. Complete a full review of the paper answering all prompts of the official review form of the top venue in this research area (e.g., NeurIPS for Deep Learning and ACM SIGGRAPH for Geometry & Animation)."
},
{
    "name": "Archaeologist",
    "description": "This paper was found buried under ground in the desert. You’re an archeologist who must determine where this paper sits in the context of this field. Find and report on a few older papers cited within the current paper that substantially influenced the current paper."
},
{
    "name": "Academic Researcher",
    "description": "You’re a researcher who is working on a new project in this area. Propose an imaginary follow-up project not just based on the current but only possible due to the existence and success of the current paper."
},
{
    "name": "Industry Practitioner",
    "description": "You work at a company or organization developing an application or product of your choice (that has not already been suggested in a prior session). Bring a convincing pitch for why you should be paid to implement the method in the paper, and discuss at least one positive and negative impact of this application."
},
{
    "name": "Hacker",
    "description": " You’re a hacker who needs a demo of this paper ASAP. Implement a small part or simplified version of the paper on a small dataset or toy problem. Prepare to share the core code of the algorithm to the class and demo your implementation. Do not simply download and run an existing implementation – though you are welcome to use (and give credit to) an existing implementation for “backbone” code."
},
#{
#    "name": "Private Investigator",
#    "description": "You are a detective who needs to run a background check on one of the paper’s authors. Where have they worked? What did they study? What previous projects might have led to working on this one? What motivated them to work on this project?"
#}
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

def extract_basic_paper_info(paper_content: str):
    PROMPT = f"""
    [Start of Paper]
    {paper_content}
    [End of Paper]

    Give a short recap (3-4 sentences) of the paper. Start with the title.
    """
    response = completion([
        {"role": "system", "content": "You are an expert paper reviewer."},
        {"role": "user", "content": PROMPT}
    ])
    console = Console()
    md = Markdown("# Short Recap")
    console.print(md)
    print (response)

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

def review_paper(directory: str):
    with open(f"{directory}/main.tex", 'r') as f:
        tex_content = f.read()

    extract_basic_paper_info(tex_content)

    for expert in EXPERTS:
        paper_expert_review(tex_content, expert)
