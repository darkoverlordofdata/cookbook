#! python3
'''Cleans all the recipes in the folder, does not do anything to already
clean recipes. Ignores any file that starts with an underscore'''

import sys
import os
import re
from os.path import join as join_path


bad = r"1/2 1/3 1/4 1/8 2/3 3/4 3/8 5/8 7/8 tsp tbsp Tbsp tbs(?!p) Tbs(?!p) cup Oz Lb".split(" ")
good = "½ ⅓ ¼ ⅛ ⅔ ¾ ⅜ ⅝ ⅞ tsp Tbsp Tbsp Tbsp Tbsp Cup oz lb".split(" ")
repls = list(zip(bad, good))

def fix_title(title):
    new_title = re.sub(r"\.|'|,", "", title)
    new_title = re.sub("&", "and", new_title)
    new_title = re.sub(" ", "-", new_title)
    new_title = re.sub("---", "--", new_title)
    new_title = re.sub(r"\(|\)", "_", new_title)
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
        #return "](../"+re.sub(" ", "-", fix_title(match.group(1)))+")"
        return "]("+fix_title(match.group(1))+".markdown)"
    text = re.sub(r"\]\((.*?)\)", fix_link, text)
    
    lines = text.split("\n")
    new_text = []
    #remove spaces from the end of lines
    for line in lines:
        match = re.search(r" +$", line)
        if match:
            new_text.append(line[:-len(match.group(0))])
        else:
            new_text.append(line)

    text = "\n".join(new_text)

    return text
    
source_folder = "./new"
savory_folder = "./savory"
sweet_folder = "./sweet"

def all_local_files(source_folder, dest_folder):
    found = False
    for file_name in os.listdir(source_folder):
        found = True
        if file_name[0] == "_": continue

        with open(join_path(source_folder, file_name), encoding="utf8") as file:
            text = file.read()

        match = re.search(r"# (.*)", text)
        if not match:
            print('file "{}" has no title, not fixing')
            continue
        old_title = match.group(1)
        new_text = clean(text)
        
        match = re.search(r"# (.*)", new_text)
        new_file_name = fix_title(match.group(1))+".markdown"
        print("{old} is now {new}".format(old=file_name, new=new_file_name))
        
        with open(join_path(dest_folder, new_file_name), "w", encoding="utf8") as file:
            file.write(new_text)
    return found

# if not os.access(dest_folder, os.F_OK):
#     os.mkdir(dest_folder)

#all_local_files(clean)

def generate_list(folder, template):
    items = []
    for file_name in os.listdir(folder):
        if (file_name.startswith("_")
        or file_name.startswith("index")):
            continue

        with open(join_path(folder, file_name), encoding="utf8") as file:
            text = file.read()

        match = re.search(r"# (.*)", text)
        if not match:
            continue

        link = template.format(file=fix_title(match.group(1))+".markdown",
                               title=match.group(1))
        items.append(link)

    items.sort()
    return items


savory_template = '''# Savory Recipes
Savory recipes are those that use salt to enhance flavor and to minimize biterness.
On this page you'll find entrées, sides, and sauces. Also waffles.

Entries
'''

sweet_template = '''# Sweet Recipes
Sweet recipes are those that use sugar to enhance flavor and to minimize bitterness.
On this page you'll find baked goods, candies, and desserts.

Entries
'''

list_entry_template = " - [{title}]({file})\n"

def main():
    chap = input("Update savory or sweet? -> ").casefold()
    
    if chap == "savory".casefold():
        dest_folder = savory_folder
        page_template = savory_template
    
    elif chap == "sweet".casefold():
        dest_folder = sweet_folder
        page_template = sweet_template
    
    else:
        input("I don't know what {} means ".format(chap))
        sys.exit(1)
    
    found = all_local_files(source_folder, dest_folder)
    if not found:
        print("No new files found? Updating index anyway.")
    else:
        print("Updating index.")
    
    items = generate_list(dest_folder, list_entry_template)
    index_text = page_template+''.join(items)

    with open(join_path(dest_folder, "index.markdown"), "w", encoding="utf8") as file:
        file.write(index_text)
    print("New index generated.")

    input("press enter to end. ")

main()