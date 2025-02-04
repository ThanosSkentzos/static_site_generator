import re
from unittest.runner import TextTestRunner

from textnode import (
    TextNode,LeafNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

delim_to_text_type = {
    '**':text_type_bold,
    '*':text_type_italic,
    '`':text_type_code,
    '```':text_type_code,
}


def text_node_to_html_node(text_node):
    type =  text_node.text_type
    if type == text_type_text:
        return LeafNode(None,text_node.text)
    elif type == text_type_bold:
        return LeafNode("b",text_node.text)
    elif type == text_type_italic:
        return LeafNode("i",text_node.text)
    elif type == text_type_code:
        return LeafNode("code",text_node.text)
    elif type == text_type_link:
        return LeafNode("a",text_node.text,{"href":text_node.url})
    elif type == text_type_image:
        return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
    else:
        raise ValueError(f"invalid text_type {text_node.text_type}")

def generate_splitter(delimiter):
    def split_on_delimiter(nodes):
        return split_nodes_delimiter(nodes,delimiter,delim_to_text_type[delimiter])
    return split_on_delimiter

split_bold = generate_splitter("**")
split_ital = generate_splitter("*")
split_code = generate_splitter("`")
split_code_block = generate_splitter("```")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]
    if delimiter not in delim_to_text_type:
        raise ValueError(f"Invalid delimiter value: {delimiter}")
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            #find new nodes from textnode
            text = node.text
            num_delimiter_found = text.count(delimiter)
            if num_delimiter_found%2!=0:
                raise Exception("Invalid Markdown Syntax")
            else:
                node_split = split_delimiters(text,delimiter)
                new_nodes += node_split
    return new_nodes

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            nodes.append(node)
            continue
        text = node.text
        img_tuples = extract_markdown_images(text)
        if len(img_tuples)==0:
            nodes += [TextNode(text,text_type_text)]
            continue
        remaining_text = text
        for t in img_tuples:
            alt = t[0]
            url = t[1]
            img_text = f"![{alt}]({url})"
            before,after = remaining_text.split(img_text,1)
            if len(before)!=0:
                nodes += [TextNode(before,text_type_text)]
            nodes += [TextNode(alt,text_type_image,url)]
            remaining_text = after
        if len(remaining_text)>0:
            nodes += [TextNode(remaining_text,text_type_text)]
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodes+= [node]
            continue
        text = node.text
        link_tuples = extract_markdown_links(text)
        if len(link_tuples)==0:
            nodes += [TextNode(text,text_type_text)]
            continue
        remaining_text = text
        c = 0
        for t in link_tuples:
            c+=1
            alt = t[0]
            url = t[1]
            link_text = f"[{alt}]({url})"
            before,after = remaining_text.split(link_text,1)
            if len(before)!=0:
                nodes += [TextNode(before,text_type_text)]
            nodes += [TextNode(alt,text_type_link,url)]
            remaining_text = after
        if len(remaining_text)>0:
            nodes += [TextNode(remaining_text,text_type_text)]
    return nodes

def split_delimiters(text,delim) -> list[TextNode]:
    if len(text)==0:
        return []
    if delim not in text:
        return [TextNode(text,text_type_text)]
    type = delim_to_text_type[delim]
    before,inside,after =  text.split(delim,2)
    lst = [TextNode(before,text_type_text),TextNode(inside,type)]
    if len(after)>3:
        lst += split_delimiters(after,delim)
    elif len(after)>0:
        lst += [TextNode(after,text_type_text)]
    return lst

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)

def text_to_textnodes(text):
    nodes = [TextNode(text,text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_bold(nodes)
    nodes = split_ital(nodes)
    nodes = split_code_block(nodes)
    nodes = split_code(nodes)
    return nodes

def md_text_to_textnodes(text):
    nodes = [TextNode(text,text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_bold(nodes)
    nodes = split_ital(nodes)
    nodes = split_code(nodes)
    nodes = split_code_block(nodes)
    return nodes

def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    print(new_nodes)
if __name__=="__main__":
    main()
