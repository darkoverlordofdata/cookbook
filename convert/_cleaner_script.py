#! python3
'''Cleans all the recipes in the folder, does not do anything to already
clean recipes. Ignores any file that starts with an underscore'''

import os
import re

bad = r"1/2 1/3 1/4 1/8 2/3 3/4 3/8 5/8 7/8 tsp tbsp Tbsp tbs(?!p) Tbs(?!p) cup Oz Lb".split(" ")
good = "½ ⅓ ¼ ⅛ ⅔ ¾ ⅜ ⅝ ⅞ tsp Tbsp Tbsp Tbsp Tbsp Cup oz lb".split(" ")
repls = list(zip(bad, good))

def clean(text):
    """fix measures, fractions, and some other things"""



    text = re.sub(r"----\|----\n\n", r"|----|----|\n", text)
    text = re.sub("## Directions", "## Cooking Instructions", text)
            
    for pat, rep in repls:
                text = re.sub(pat, rep, text, flags=re.IGNORECASE)

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
    

def all_local_files(func):
    for file_name in os.listdir("."):
        if file_name[0] == "_": continue
        print(file_name)

        with open(file_name, encoding="utf8") as file:
            text = file.read()
        
        new_text = func(text)
        
        with open(file_name, "w", encoding="utf8") as file:
            file.write(new_text)

all_local_files(clean)

print("done")
