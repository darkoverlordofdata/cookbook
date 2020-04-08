#! python3
'''Cleans all the recipes in the folder, does not do anything to already
clean recipes. Ignores any file that starts with an underscore'''

import os
import re

bad = r"1/2 1/3 1/4 1/8 2/3 3/4 3/8 5/8 7/8 tsp tbsp Tbsp tbs(?!p) Tbs(?!p) cup Oz Lb".split(" ")
good = "½ ⅓ ¼ ⅛ ⅔ ¾ ⅜ ⅝ ⅞ tsp Tbsp Tbsp Tbsp Tbsp Cup oz lb".split(" ")
repls = list(zip(bad, good))

def fix_title(title):
    new_title = re.sub(r"\.|'|,", "", title)
    new_title = re.sub("&", "and", new_title)
    return new_title.strip()

def clean(text):
    """fix measures, fractions, and some other things"""
    #clean structure
    text = re.sub(r"(?<!\|)Amount ?\| ?Ingredient(?!\|)", "|Amount|Ingredient|", text)
    text = re.sub(r"----\|----\n\n", r"----|----\n", text)
    text = re.sub(r"(?<!\|)----\|----(?!\|)", "|----|----|", text)
    text = re.sub("## Directions", "## Cooking Instructions", text)

    #fractions        
    for pat, rep in repls:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)

    #links
    def fix_link(match):
        return "](../"+re.sub(" ", "-", fix_title(match.group(1)))+")"
    text = re.sub(r"\]\((.*?)\)", fix_link, text)
    
    #add spaces to the end of lines
    lines = text.split("\n")
    new_text = []
    for line in lines:
        match = re.search(r"  $", line)
        if match:
            new_text.append(line)
        else:
            new_text.append(line+"  ")

    text = "\n".join(new_text)

    return text
    
source_folder = "../new"
dest_folder = "../clean"

def all_local_files(func):
    for file_name in os.listdir(source_folder):
        if file_name[0] == "_": continue
        print(file_name)

        with open(os.path.join(source_folder, file_name), encoding="utf8") as file:
            text = file.read()

        match = re.search(r"# (.*)", text)
        if not match:
            print('file "{}" has no title, not fixing')
            continue
        new_file_name = fix_title(match.group(1))+".markdown"
        print(new_file_name)
        
        new_text = func(text)
        with open(os.path.join(dest_folder, new_file_name), "w", encoding="utf8") as file:
            file.write(new_text)

if not os.access(dest_folder, os.F_OK):
    os.mkdir(dest_folder)

all_local_files(clean)

print("done")
