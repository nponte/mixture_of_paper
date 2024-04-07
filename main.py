import click
import arxiv
import os
import tempfile

### arxiv library ###
#####################

def pprint_result(paper):
    string = f"[{str(paper.published)[:10]}] {paper.title} -- {paper.entry_id}"
    print("-"*len(string))
    print(string)
    print("-"*len(string))

def arxiv_keyword_search(keyword: str, max_results: int = 5):
    search = arxiv.Search(
        query=keyword,
        max_results=max_results,
        sort_by = arxiv.SortCriterion.Relevance,
    )
    for paper in client.results(search):
        pprint_result(paper)
        if input("Download? (y)") == "y":
            name = paper.title.lower().replace(' ', '_')
            paper.download_source(dirpath="./papers", filename=f"{name}.tar.gz")

### paper review tools ###
##########################

### click ###
#############

@click.group()
def cli():
    pass

@click.command()
@click.option('--r', default=5, help="number of results")
@click.argument('keyword')
def find(r: int, keyword: str):
    arxiv_keyword_search(keyword, r)

@click.command()
def review():
    for _, _, filenames in os.walk('./papers'):
        paper_map = {}
        print('-'*20)
        for i, f in enumerate(filenames):
            print(f"{i}: {f[:-7]}")
            paper_map[str(i)] = f
        print('-'*20)
            
    try:
        file = paper_map[input("Review? (#)")]
        with tempfile.TemporaryDirectory() as tmpdir:
            os.system(f"tar -xvf ./papers/{file} -C {tmpdir} > /dev/null 2>&1")
            
    except:
        print("Invalid input -- exiting")
        return

cli.add_command(find)
cli.add_command(review)

if __name__ == '__main__':
    client = arxiv.Client()
    cli()
