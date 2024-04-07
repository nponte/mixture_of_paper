import click
import os
import tempfile
from arxiv_lib import arxiv_keyword_search
from paper_review import review_paper

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
        for i, f in enumerate(filenames):
            print(f"{i}: {f[:-7]}")
            paper_map[str(i)] = f
    
    selection = input("Review? (#)")
    if selection not in paper_map:
        print("Invalid input -- exiting")
        return
    else:
        print (f"Reviewing {paper_map[selection]}")
    file = paper_map[selection]
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f"tar -xvf ./papers/{file} -C {tmpdir}")
        review_paper(tmpdir)

cli.add_command(find)
cli.add_command(review)

if __name__ == '__main__':
    cli()
