from textnode import TextNode, TextType
from copystatic import copy_static
from markdown_blocks import markdown_to_html_node

import os
import re
import shutil

def generate_page(gen_from_path, gen_template_path, gen_dest_path):
    print(f"Generating page from {gen_from_path} to {gen_template_path} using {gen_dest_path}")
    with open(gen_from_path, "r", encoding="utf-8") as f:
        markdown_string=f.read()
    with open(gen_template_path, "r", encoding="utf-8") as f:
        template=f.read()
    html_after=markdown_to_html_node(markdown_string).to_html()
    title=extract_title(markdown_string)
    
    html = template.replace("{{ Title }}", f" {title} ")
    html = html.replace("{{ Content }}", f" {html_after} ")
    
    os.makedirs(os.path.dirname(gen_dest_path), exist_ok=True)
    with open(gen_dest_path, "w", encoding="utf-8") as f:
        f.write(html)

def rec_generate_page(content_dir, gen_template_path, public_path):
    for entry in os.listdir(content_dir):
        src_path=os.path.join(content_dir, entry)
        dst_path=os.path.join(public_path, entry.replace(".md", ".html"))
        if os.path.isfile(src_path):
            print(f"Generating page from {src_path} to {gen_template_path} using {dst_path}")
            with open(src_path, "r", encoding="utf-8") as f:
                markdown_string=f.read()
            with open(gen_template_path, "r", encoding="utf-8") as f:
                template=f.read()
            html_after=markdown_to_html_node(markdown_string).to_html()
            title=extract_title(markdown_string)
            
            html = template.replace("{{ Title }}", f" {title} ")
            html = html.replace("{{ Content }}", f" {html_after} ")
            
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            print(f"Created new folder {dst_path}")
            os.mkdir(dst_path)
            rec_generate_page(src_path,gen_template_path, dst_path)

def extract_title(markdown):
    lines=markdown.split('\n')
    for line in lines:
        match= re.match(r"^# (.+)", line)
        if match:
            return match.group(1).strip()
        
    raise Exception("Heading title not found")

def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))  # путь до src/main.py
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))  # подняться в корень проекта
    content_dir=os.path.join(root_dir, "content")
    blog_dir=os.path.join(content_dir, "blog")

    static_path = os.path.join(root_dir, "static")
    public_path = os.path.join(root_dir, "public")
    gen_template_path = os.path.join(root_dir,"template.html")

    copy_static(static_path,public_path)
    rec_generate_page(content_dir, gen_template_path, public_path)

if __name__ == "__main__":
    main()