class Pagination:
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 1

    def total_pages(self):
        return (len(self.items) + self.items_per_page - 1) // self.items_per_page

    def get_page_items(self, page_number):
        if page_number < 1 or page_number > self.total_pages():
            return []
        start = (page_number - 1) * self.items_per_page
        end = start + self.items_per_page
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

    def start (self):
        start_index = (self.current_page - 1) * self.items_per_page
        return start_index
    
    def end (self):
        end_index = self.start() + self.items_per_page
        return end_index
