import arxiv

class ArxivTool:
    def __init__(self):
        self.client = arxiv.Client()

    def search_papers(self, query: str, max_results: int = 10):
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        # FIX: API mới của ArXiv yêu cầu dùng client.results()
        return list(self.client.results(search))