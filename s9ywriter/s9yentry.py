class S9YEntry():
    def __init__(self):
        self.db_keys = ["id", "title", "timestamp", "body", "comments", "trackbacks", "extended", "exflag", "author", "authorid", "isdraft", "allow_comments", "last_modified", "moderate_comments"]
        self.categories = []
        self.tags = []

    def get_db_insert_values(self):
        values = []
        for k in self.db_keys:
            if hasattr(self, k):
                values.append(getattr(self, k))
            else:
                values.append(None)
        return values
