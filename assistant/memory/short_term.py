class ShortTermMemory:
    def __init__(self, max_items=5):
        self.items = []
        self.max_items = max_items

    def add(self, text):
        self.items.append(text)
        self.items = self.items[-self.max_items:]

    def get(self):
        return "\n".join(self.items)
