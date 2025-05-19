import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        first_delimiter_pos = node.text.find(delimiter)
        if first_delimiter_pos ==-1:
            new_nodes.append(node)
            continue

        second_delimeter_pos= node.text.find(delimiter, first_delimiter_pos+len(delimiter))

        if second_delimeter_pos == -1:
            raise Exception(f"No closing delimiter '{delimiter}' found")
        
        text_before= node.text[:first_delimiter_pos]
        text_between=node.text[first_delimiter_pos+len(delimiter):second_delimeter_pos]
        text_after=node.text[second_delimeter_pos+len(delimiter):]

        # Add the text before as a TEXT node
        if text_before:
            new_nodes.append(TextNode(text_before, TextType.TEXT))
            
        # Add the text between as the specified text_type
        new_nodes.append(TextNode(text_between, text_type))
        
        # Recursively process the text after
        if text_after:
            # Create a temporary node with the remaining text
            after_node = TextNode(text_after, TextType.TEXT)
            # Process this node and extend our results
            new_nodes.extend(split_nodes_delimiter([after_node], delimiter, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_link(old_nodes):
    new_nodes=[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches=extract_markdown_links(node.text)
        text=node.text
        for anc,url in matches:
            section=text.split(f"[{anc}]({url})", 1)
            if section[0]:
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(f"{anc}",TextType.LINK,f"{url}"))
            text=section[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes=[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches=extract_markdown_images(node.text)
        text=node.text
        for anc,url in matches:
            section=text.split(f"![{anc}]({url})", 1)
            if section[0]:
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(f"{anc}",TextType.IMAGE,f"{url}"))
            text=section[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes=[TextNode(text,TextType.TEXT)]
    nodes=split_nodes_link(split_nodes_image(nodes))
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes