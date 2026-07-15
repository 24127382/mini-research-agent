from tools.arxiv import ArxivTool
from tools.wikipedia import WikipediaTool
from agent.state import Action

class Executor:
    def __init__(self):
        self.arxiv_tool = ArxivTool()
        self.wikipedia_tool = WikipediaTool(user_agent="MyApp/0.1")

    def execute(self, action: Action) -> str:
        if action.tool == "arxiv":
            query = action.arguments.get("query", "")
            max_results = action.arguments.get("max_results", 10)
            try:
                papers = self.arxiv_tool.search_papers(query, max_results)
                if not papers:
                    return "LỖI: Không tìm thấy bài báo nào trên ArXiv với từ khóa này."
                return str([paper.title for paper in papers])
            except Exception as e:
                return f"LỖI kết nối ArXiv: {str(e)}"
                
        elif action.tool == "wikipedia":
            query = action.arguments.get("query", "")
            try:
                result = self.wikipedia_tool.search(query)
                return result
            except Exception as e:
                return f"LỖI kết nối Wikipedia: {str(e)}"
        else:
            return f"LỖI: Công cụ '{action.tool}' không hợp lệ hoặc không tồn tại."