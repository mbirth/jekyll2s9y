import sqlite3
from .s9yentry import S9YEntry


class S9YWriter():
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file)

    def __del__(self):
        self.db.close()

    def add_entry(self, entry: S9YEntry):
        keys = entry.db_keys[1:]
        placeholders = ["?"] * len(keys)
        data = entry.get_db_insert_values()[1:]
        sql = "INSERT INTO entries (" + ", ".join(keys) + ") VALUES (" + ", ".join(placeholders) + ")"
        #print(sql)
        result = self.db.execute(sql, data)
        entry_id = result.lastrowid
        print(repr(result.lastrowid))
        print(entry.title)

        # Add permission
        sql = "INSERT INTO entryproperties VALUES (?, ?, ?)"
        self.db.execute(sql, [entry_id, "ep_access", "public"])

        # TODO: Add permalink
        # permalinks (permalink, entry_id, type, data)
        # permalink = archives/YYYY-MM-DD-%title%.html
        # %title% = sanitised, no Unicode, ü --> ue, etc.
        # WORKAROUND: Edit your blog settings and change the permalink to let S9Y regenerate them
        #             then change back to desired value

        for category in list(set(entry.categories)):
            self.add_category(entry_id, category)

        for tag in list(set(entry.tags)):
            self.add_tag(entry_id, tag)

    def commit(self):
        self.db.commit()

    def add_category(self, entry_id: int, category_name: str):
        # Tables: category, entrycat, access
        # Category: categoryid, category_name, "", "", 0, 0, 0, parentid, NULL, NULL
        # entrycat: entryid, categoryid
        print(f"{entry_id} - {category_name}")
        sql = "SELECT categoryid FROM category WHERE category_name = ?"
        result = self.db.execute(sql, [category_name])
        cat = result.fetchone()
        if cat:
            category_id = cat[0]
        else:
            # Category does not yet exist, add it
            sql = "INSERT INTO category (category_name) VALUES (?)"
            result = self.db.execute(sql, [category_name])
            category_id = result.lastrowid
            # Add access permissions
            # access: 0, category_id, "category", read
            # access: 0, category_id, "category", write
            sql = "INSERT INTO access VALUES (?, ?, ?, ?, ?)"
            self.db.execute(sql, [0, category_id, "category", "read", ""])
            self.db.execute(sql, [0, category_id, "category", "write", ""])
            # Add permalink
            sql = "INSERT INTO permalinks VALUES (?, ?, ?, ?)"
            self.db.execute(sql, [f"categories/{category_name}", category_id, "category", None])

        sql = "INSERT INTO entrycat VALUES (?, ?)"
        self.db.execute(sql, [entry_id, category_id])

    def add_tag(self, entry_id: int, tag: str):
        # Table: entrytags (entryid, tag)
        sql = "INSERT INTO entrytags VALUES (?, ?)"
        self.db.execute(sql, (entry_id, tag))
