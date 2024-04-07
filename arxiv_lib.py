import arxiv

client = arxiv.Client()

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
