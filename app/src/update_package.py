#!/usr/bin/env python

import sys
import urllib
import subprocess
import os
import yaml
import markdown
import lxml.html
import re
import html2text
from dulwich import porcelain
import shutil

menu_file = "_data/menu.yml"
landing_file = "IT-systems/index.md"
docs_location = "IT-systems"
menu_base = "/IT-systems/"
menu_base_name = "IT-systems"
placeholder_start = '<div style="display:none" class="generated_start">generated items start</div>'
placeholder_end = '<div style="display:none" class="generated_end">generated items end</div>'

package_folder_name = "docs"
package_git_url = "git@github.com:zotya/zotya.github.io.git"
#package_git_url = "https://github.com/zotya/zotya.github.io.git"

def html2lxml(html):
    return lxml.html.fromstring(html)

def lxml2html(tree):
    return lxml.html.tostring(lxml)

def html2md(html):
    return html2text.html2text(html)

def md2html(md):
    return markdown.markdown(md)

def md2lxml(md):
    return html2lxml(md2html(md))

def lxml2md(tree):
    return html2md(lxml2html(tree))

def loadReadme(repo_url):
    resp = urllib.urlopen(repo_url)
    full_html = resp.read()
    html = lxml.html.fromstring(full_html)
    body = html.find_class("markdown-body")[0]
    body_text = lxml.html.tostring(body, 'utf-8')
    readme_md = html2text.html2text(body_text)
    return readme_md

def addTitleToReadme(md, repo_url):
    tree = md2lxml(md)
    h1 = tree.find("h1").text
    package_name = repo_url.split("/")[-1]
    title = h1 or package_name
    md = "---\ntitle: %s\n---\n%s" %(title, md)
    return md, title

def loadMenu():
    relative_menu_file = "%s/%s" %(package_folder_name, menu_file)
    f = open(relative_menu_file, 'r')
    menu_str = f.read()
    f.close()
    menu = yaml.load(menu_str)
    return menu

def saveMenu(menu, repo):
    relative_menu_file = "%s/%s" %(package_folder_name, menu_file)
    os.remove(relative_menu_file)
    f = open(relative_menu_file, "w")
    f.write(yaml.dump(menu, default_flow_style=False))
    f.close()
    porcelain.add(repo, menu_file)

def build_submenu(parent, tree, repo_name):
    submenu = {}
    submenu['text'] = parent
    submenu['url'] = "%s%s/#%s" %(menu_base, repo_name, re.sub('\s+', '-', parent.lower()))
    if len(tree) > 0:
        submenu['subitems'] = []
        for element in tree:
            submenu['subitems'].append(build_submenu(element.keys()[0], element.values()[0], repo_name))
    return submenu

def updateMenu(md, repo_name, repo):
    available_items = ["h1", "h2", "h3", "h4", "h5", "h6"]
    menu = loadMenu()
    readme_tree = md2lxml(md)
    elements = readme_tree.findall("*")
    menu_item_tree = []
    parent_elements = []
    for element in elements:
        if element.tag.lower() in available_items:
            if element.text[:6] == 'title:':
                continue
            new_parent_elements = []
            for parent in parent_elements:
                if element.tag.lower() > parent.tag.lower():
                    new_parent_elements.append(parent)
            new_parent_elements.append(element)

            pointer = menu_item_tree
            for parent in new_parent_elements[:-1]:
                for menu_element in pointer:
                    if menu_element.has_key(parent.text):
                        pointer = menu_element[parent.text]

            new_element = {}
            new_element[element.text] = []
            pointer.append(new_element)

            parent_elements = new_parent_elements

    new_menu_item = build_submenu(menu_item_tree[0].keys()[0], menu_item_tree[0].values()[0], repo_name)
    new_menu_item['source'] = 'generated'
    new_menu_item['url'] = new_menu_item['url'].split('/#')[0]

    for submenu in menu:
        if submenu['text'] == menu_base_name:
            new_it_systems_submenu_from_menu = []
            new_it_systems_submenu_from_generated = []
            added = False
            for item in submenu['subitems']:
                if item.has_key('source') and item['source'] == 'generated':
                    if item['text'] != new_menu_item['text']:
                        new_it_systems_submenu_from_generated.append(item)
                    else:
                        added = True
                        new_it_systems_submenu_from_generated.append(new_menu_item)
                else:
                    new_it_systems_submenu_from_menu.append(item)
            if not added:
                new_it_systems_submenu_from_generated.append(new_menu_item)
            new_it_systems_submenu_from_generated = sorted(new_it_systems_submenu_from_generated, key=lambda k:k['text'])
            submenu['subitems'] = new_it_systems_submenu_from_menu + new_it_systems_submenu_from_generated

    saveMenu(menu, repo)

def updateReadmePage(readme_md, repo_name, repo):
    relative_doc_dir = "%s/%s/%s" %(package_folder_name, docs_location, repo_name)
    relative_doc_file = "%s/index.md" %relative_doc_dir
    doc_file = "%s/%s/index.md" %(docs_location, repo_name)
    should_add_to_git = False
    try:
        os.stat(relative_doc_dir)
    except:
        os.mkdir(relative_doc_dir)
        should_add_to_git = True

    try:
        os.remove(relative_doc_file)
    except OSError:
        pass
    f = open(relative_doc_file, "w")
    f.write(readme_md)
    f.close()
    if should_add_to_git:
        porcelain.add(repo, doc_file)

def updateLandingPage(readme_title, repo):
    relative_landing_file = "%s/%s" %(package_folder_name, landing_file);
    f = open(relative_landing_file, "r")
    lines = f.read().splitlines()
    f.close()

    before_placeholder = []
    between_placeholder = []
    after_placeholder = []
    current_slot = before_placeholder
    for line in lines:
        if line == placeholder_end:
            current_slot = after_placeholder
        current_slot.append(line)
        if line == placeholder_start:
            current_slot = between_placeholder

    new_line = "* %s" %readme_title
    if new_line not in between_placeholder:
        between_placeholder.append("* %s" %readme_title)
    between_placeholder.sort()
    new_lines = before_placeholder + between_placeholder + after_placeholder
    f = open(relative_landing_file, "w")
    f.write("\n".join(new_lines))
    f.close()
    porcelain.add(repo, landing_file)

def update(repo_url):
    try:
        shutil.rmtree(package_folder_name)
    except:
        pass
    repo = porcelain.clone(package_git_url, package_folder_name)


    repo_url = repo_url.split("\n")[0]
    repo_name = repo_url.split('/')[-1]
    readme_md = loadReadme(repo_url)
    readme_md, readme_title = addTitleToReadme(readme_md, repo_url)
    updateMenu(readme_md, repo_name, repo)
    updateReadmePage(readme_md, repo_name, repo)

    updateLandingPage(readme_title, repo)

    open("docs/testfile", "w").write("data")
    porcelain.add(repo, "testfile")

    porcelain.commit(repo, b"updated docs for %s" %repo_name)
    refs_path = b"refs/heads/master"
    porcelain.push(repo, package_git_url, b"HEAD:" + refs_path)



if __name__ == '__main__':
    for arg in sys.argv[1:]:
        update(arg)
