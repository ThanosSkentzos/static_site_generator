from enum import Enum
from functools import reduce
from functions import text_node_to_html_node, md_text_to_textnodes
from htmlnode import LeafNode, ParentNode

class BlockTypes(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def generate(func):
    def wrapper(list_input):
        return reduce(func,list_input)
    return wrapper
add = lambda x,y:x+y
radd = generate(add)

def block_to_block_type(block):
    lines = block.split('\n\n')
    num_lines = len(lines)
    first_chars = list(map(lambda x:x[0],lines))
    first_2_chars = list(map(lambda x:x[0:2],lines))
    num_hash = 0
    if block[0]=="#":
        for c in block:
            if c=="#":
                num_hash+=1
            else:
                if c!=" ":
                    return BlockTypes.paragraph
                if num_hash<=6:
                    return BlockTypes.heading
    elif block[:3]=="```" and block[-3:]==block[:3]:
        return BlockTypes.code
    elif radd(first_chars)==num_lines*">":
        return BlockTypes.quote
    elif radd(first_2_chars) in [num_lines*"* ",num_lines*"- "]:
        return BlockTypes.unordered_list
    elif radd(first_2_chars) == radd([f"{i+1}." for i in range(num_lines)]):
        return BlockTypes.ordered_list
    else:
        return BlockTypes.paragraph

def markdown_to_blocks(markdown):
    blocks = []
    if len(markdown)==0:
        return blocks
    for line in markdown.split('\n\n'):
        if len(line)==0:
            continue
        line = line.strip()
        blocks.append(line)
    return blocks

def markdown_to_html_node(markdown):
    nodes = []
    for block in markdown_to_blocks(markdown):
        type = block_to_block_type(block)
        block_lines = block.split('\n\n')
        lines = block.split('\n')
        match type:
            case BlockTypes.paragraph:
                # print("| paragraph |",block)
                text_nodes = md_text_to_textnodes(block)
                html_nodes = list(map(text_node_to_html_node,text_nodes))
                paragraph_node = ParentNode("p",html_nodes)
                nodes.append(paragraph_node)
            case BlockTypes.heading:
                num = block.count("#")
                text = block.strip("#").strip(" ")
                nodes.append(LeafNode(f"h{num}",text))
            case BlockTypes.code:
                # print("| code block |",block)
                text = block.strip('```')
                nodes.append(ParentNode("pre",[LeafNode("code",text)]))
            case BlockTypes.quote:
                quote = "\n".join([line.strip('>') for line in lines])
                nodes.append(LeafNode("blockquote",quote))
            case BlockTypes.unordered_list:
                nodes.append(ParentNode("ul",[LeafNode("li",line[2:]) for line in lines]))
            case BlockTypes.ordered_list:
                nodes.append(ParentNode("ol",[LeafNode("li",line[2:]) for line in lines]))
    return ParentNode("div",nodes)



def main():
    md = """
This is **bolded** paragraph

# this is a heading


This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

>quote starts here
>
>nothing above
>bye

* This is a list
* with items
"""
    # md = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # md = text = "This is **bold** text with an *italic* word and a `inline code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = markdown_to_html_node(md)
    print(nodes[0].to_html())
if __name__=="__main__":
    main()
