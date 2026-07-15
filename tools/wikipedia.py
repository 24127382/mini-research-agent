import wikipediaapi

class WikipediaTool:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en', 
            user_agent=self.user_agent
        )

    def search(self, query: str):
        page = self.wiki_wiki.page(query)
        if page.exists():
            # Trả về chuỗi kết hợp thay vì dict, hoặc có thể format lại tùy LLM
            summary = page.summary[:1000] + "..." if len(page.summary) > 1000 else page.summary
            return f"Tiêu đề: {page.title}\nTóm tắt: {summary}\nURL: {page.fullurl}"
        else:
            # FIX: Báo lỗi rõ ràng để LLM tự sửa sai (thử từ khóa khác)
            return f"LỖI: Không tìm thấy trang Wikipedia nào khớp hoàn toàn với từ khóa '{query}'. Hãy thử một từ khóa khác hoặc chung chung hơn."