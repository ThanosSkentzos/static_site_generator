from enum import Enum

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

delim_to_text_type = {
    '*':text_type_italic,
    '**':text_type_bold,
    '`':text_type_code}

from htmlnode import LeafNode
class TextNode():
    def __init__(self,text,text_type,url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other) -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
    def __repr__(self) -> str:
        return(f"TextNode({self.text}, {self.text_type}, {self.url})")


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

def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)

    node = TextNode("This is text with a *code block* word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "*", text_type_code)
    print(new_nodes)
if __name__=="__main__":
    main()
