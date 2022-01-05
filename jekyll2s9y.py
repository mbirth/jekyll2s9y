#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from os import makedirs
from os.path import basename
import shutil
import pytz
import yaml
import jekyllreader
import s9ywriter


with open("config.yaml", "rt") as f:
    config = yaml.load(f)

print(repr(config))

# copy original file to working copy
shutil.copyfile(config["general"]["s9y_database"], config["general"]["s9y_database_output"])

DATEFORMAT_IN = "%Y-%m-%d %H:%M:%S %z"
DATEFORMAT_OUT = "%Y-%m-%d %H:%M:%S"

LOCAL_TIMEZONE = pytz.timezone(config["general"]["timezone"])

# MAIN SCRIPT
jk = jekyllreader.JekyllReader(config["general"]["jekyll_dir"])
s9y = s9ywriter.S9YWriter(config["general"]["s9y_database_output"])
for i in range(0, jk.len()):
    print(f"Item: {i}")
    jk_article = jk.get(i)

    new_entry = s9ywriter.S9YEntry()
    for k, v in config["s9y_defaults"].items():
        setattr(new_entry, k, v)

    new_entry.title = jk_article.metadata["title"]
    date_created = datetime.strptime(jk_article.metadata["created"], DATEFORMAT_IN).astimezone(LOCAL_TIMEZONE)
    date_updated = datetime.strptime(jk_article.metadata["updated"], DATEFORMAT_IN).astimezone(LOCAL_TIMEZONE)
    new_entry.timestamp = int(date_created.timestamp())
    new_entry.last_modified = int(date_updated.timestamp())

    # Handle images
    img_target_dir = config["general"]["s9y_media_dir"] + "/" + str(date_created.year) + "/"
    img_files = jk_article.images
    print(repr(img_files))
    jk_article.replace_imagepaths("/" + img_target_dir)
    for img in img_files:
        img_name = basename(img)
        makedirs(img_target_dir, exist_ok=True)
        shutil.copyfile(img, img_target_dir + img_name)

    # Handle body: Split into body+extended if possible
    content = jk_article.body
    content = content.replace("\r", "")
    splits = content.split("\n\n", 1)
    if len(splits) == 1:
        new_entry.body = content
    else:
        splits[1] = splits[1].strip("\n")
        (new_entry.body, new_entry.extended) = splits

    # Handle tags/categories and other metadata
    for t in jk_article.metadata["tags"]:
        if t in config["categories"]:
            new_entry.categories.append(t)
        else:
            new_entry.tags.append(t)

    if "language" in jk_article.metadata and jk_article.metadata["language"] != "en":
        if jk_article.metadata["language"] == "de":
            new_entry.title += " 🇩🇪"
        else:
            new_entry.title += " (" + jk_article.metadata["language"] + ")"

    s9y.add_entry(new_entry)
s9y.commit()
