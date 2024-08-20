from enum import Enum
from functools import reduce

class BlockTypes(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

add = lambda x,y:x+y
def generate(func):
    def wrapper(list_input):
        return reduce(func,list_input)
    return wrapper

radd = generate(add)

def block_to_block_type(block):
    lines = block.split('\n')
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

def main():
    for i in range(6):
        block = (i+1)*"#"+" "+"This is a Heading"
        expect = BlockTypes.heading
        result = block_to_block_type(block)
if __name__=="__main__":
    main()
