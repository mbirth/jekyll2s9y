import os
from .jekyllarticle import JekyllArticle

class JekyllReader():

    def __init__(self, src_dir: str):
        self.src_dir = src_dir
        self.file_list = []
        self.find_articles()

    def find_articles(self):
        for root, dirs, files in os.walk(self.src_dir):
            if root.split("/")[-1] in ["assets", "css", "images", "fonts", "javascripts", "_includes", "_layouts", self.src_dir]:
                continue
            for f in files:
                if f.split(".")[-1] != "md":
                    continue
                filepath = "{}/{}".format(root, f)
                self.file_list.append(filepath)

    def len(self):
        return len(self.file_list)

    def get(self, idx: int):
        return JekyllArticle(self.file_list[idx], self.src_dir)
