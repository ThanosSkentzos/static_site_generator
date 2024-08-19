import re

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
    '*':text_type_italic,
    '**':text_type_bold,
    '`':text_type_code}


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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]
    if delimiter not in delim_to_text_type:
        raise ValueError("Invalid delimiter value")
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            #find new nodes from textnode
            text=node.text
            num_delimiter_found = text.count(delimiter)
            if num_delimiter_found%2!=0:
                print(text.count(delimiter))
                raise Exception("Invalid Markdown Syntax")
            else:
                return split_delimiters(text,delimiter)

def split_delimiters(text,delim) -> list[TextNode]:
    if delim not in text:
        return [TextNode(text,text_type_text)]
    type = delim_to_text_type[delim]
    before,inside,after =  text.split(delim,2)
    lst = [TextNode(before,text_type_text),TextNode(inside,type)]
    if len(after)>3:
        lst += split_delimiters(after,delim)
    else:
        lst += [TextNode(after,text_type_text)]
    return lst

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)
def main():
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) but not ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
if __name__=="__main__":
    main()
