import re

from enum import Enum
from textnode import text_node_to_html_node
from node_splitter import text_to_textnodes
from htmlnode import HTMLNode,ParentNode
from textnode import TextNode,TextType

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

def markdown_to_blocks(markdown):
    markdonw_list=markdown.split("\n\n")
    cleaned_markdown_list=[]
    for block in markdonw_list:
        cleaned_block=block.strip()
        if cleaned_block:
            cleaned_markdown_list.append(cleaned_block)
    return cleaned_markdown_list

def block_to_block_type(block):
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    lines=block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(re.match(r'^\d+\.\s',line) for line in lines):
        numbers=[int(re.match(r'^(\d+)',line).group(1)) for line in lines]
        expected_numbers=list(range(1, len(lines)+1))
        if numbers == expected_numbers:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks=markdown_to_blocks(markdown)
    children=[]
    for block in blocks:
        block_type=block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                normalized_text = ' '.join(block.split())
                paragraph_children = text_to_children(normalized_text)
                paragraph_node = ParentNode("p", paragraph_children)
                children.append(paragraph_node)
            case BlockType.HEADING:
                heading_children=text_to_children(block)
                level=0
                for char in block:
                    if char == '#':
                        level+=1
                    else:
                        break

                heading_text=block[level:].strip()
                heading_children=text_to_children(heading_text)
                heading_tag=f"h{level}"
                heading_node=ParentNode(heading_tag, heading_children)

                children.append(heading_node)

            case BlockType.CODE:
                # Remove the triple backticks and extract clean code content
                lines = block.strip().split("\n")
                
                # Remove triple backtick lines
                if len(lines) >= 2 and "```" in lines[0] and "```" in lines[-1]:
                    code_lines = lines[1:-1]
                else:
                    code_lines = [line for line in lines if not line.strip() == "```"]
                
                # Remove leading whitespace from each line
                cleaned_lines = []
                for line in code_lines:
                    if line.strip():  # Only process non-empty lines
                        cleaned_lines.append(line.lstrip())
                    else:
                        cleaned_lines.append(line)  # Keep empty lines as is
                
                # Add a newline at the end to match expected output
                code_text = "\n".join(cleaned_lines) + "\n"
                
                # Create the code node with the cleaned text
                code_text_node = TextNode(code_text, TextType.TEXT)
                code_html_node = text_node_to_html_node(code_text_node)
                code_node = ParentNode("code", [code_html_node])
                pre_node = ParentNode("pre", [code_node])
                children.append(pre_node)

            case BlockType.QUOTE:
                quote_text=block.lstrip(">").strip()
                quote_children=text_to_children(quote_text)
                quote_node=ParentNode("blockquote", quote_children)
                children.append(quote_node)

            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                list_items = []

                for item in items:
                    item_text = item.lstrip("*-").strip()
                    if item_text:
                        item_children = text_to_children(item_text)
                        li_node = ParentNode("li", item_children)
                        list_items.append(li_node)
                ul_node = ParentNode("ul", list_items)
                children.append(ul_node)

            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                list_items = []

                for item in items:
                    dot_index = item.find('.')
                    if dot_index != -1:
                        item_text = item[dot_index+1:].strip()
                        if item_text:
                            item_children = text_to_children(item_text)
                            li_node = ParentNode("li", item_children)
                            list_items.append(li_node)
                ol_node = ParentNode("ol", list_items)
                children.append(ol_node)

    parent_node = ParentNode("div", children)
    return parent_node