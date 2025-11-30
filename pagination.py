class Pagination:
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 1

    def _index_range(self, page):
        start = (page - 1) * self.items_per_page
        end = start + self.items_per_page
        return start, end

    def total_pages(self):
        if not self.items:
            return 1
        return (len(self.items) - 1) // self.items_per_page + 1

    def get_page_items(self, page):
        if page < 1 or page > self.total_pages():
            return []
        start, end = self._index_range(page)
        return self.items[start:end]

    def next_page(self):
        if self.current_page < self.total_pages():
            self.current_page += 1
        return self.get_page_items(self.current_page)

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
        return self.get_page_items(self.current_page)

    def reset(self):
        self.current_page = 1

    def start(self):
        return self._index_range(self.current_page)[0]

    def end(self):
        return self._index_range(self.current_page)[1]
