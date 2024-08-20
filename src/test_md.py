import unittest

from htmlnode import HTMLNode, LeafNode
from markdown import block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestMarkdown(unittest.TestCase):
    def test_props_to_html(self):
        md = \
"""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        result = markdown_to_blocks(md)
        self.assertEqual(expected, result)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

from markdown import BlockTypes

class TestBlockTypes(unittest.TestCase):
    def test_heading(self):
        for i in range(1,7):
            block = i*"#"+" "+"This is a Heading"
            expect = BlockTypes.heading
            result = block_to_block_type(block)
            self.assertEqual(expect,result)
    def test_code(self):
        block = "```print('Hello World')```"
        expect = BlockTypes.code
        result = block_to_block_type(block)
        self.assertEqual(expect,result)
    def test_quote(self):
        block  = \
"""> Writing
> tests
> is
> boring"""
        expect = BlockTypes.quote
        result = block_to_block_type(block)
        self.assertEqual(expect,result)
    def test_unordered_list(self):
        block = \
"""* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expect = BlockTypes.unordered_list
        result = block_to_block_type(block)
        self.assertEqual(expect,result)
        block = \
"""- This is the first list item in a list block
- This is a list item
- This is another list item"""
        expect = BlockTypes.unordered_list
        result = block_to_block_type(block)
        self.assertEqual(expect,result)
    def test_ordered_list(self):
        block = \
"""1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""
        expect = BlockTypes.ordered_list
        result = block_to_block_type(block)
        self.assertEqual(expect,result)

class TestMD_to_HTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = "This is **bolded** paragraph"
        result = markdown_to_html_node(md)
        expected = "[HTMLNode(p,None,[HTMLNode(None,This is ,None,None), HTMLNode(b,bolded,None,None), HTMLNode(None, paragraph,None,None)],None)]"
        expected = f"HTMLNode(div,None,{expected},None)"
        self.assertEqual(repr(result),expected)
    def test_heading(self):
        md = "##### This is a heading\n\n###thisisnot"
        result = markdown_to_html_node(md)
        expected = "[HTMLNode(h5,This is a heading,None,None), HTMLNode(p,None,[HTMLNode(None,###thisisnot,None,None)],None)]"
        expected = f"HTMLNode(div,None,{expected},None)"
        self.assertEqual(repr(result),expected)
    def test_code(self):
        md = "``` This is code ```\n\n```This also```\n\n`Thisnot`"
        result = markdown_to_html_node(md)
        expected = "[HTMLNode(pre,None,[HTMLNode(code, This is code ,None,None)],None), HTMLNode(pre,None,[HTMLNode(code,This also,None,None)],None), HTMLNode(p,None,[HTMLNode(code,Thisnot,None,None)],None)]"
        expected = f"HTMLNode(div,None,{expected},None)"
        self.assertEqual(repr(result),expected)
    def test_quote(self):
        md = ">quote starts here\n>\n>nothing above\n>bye"
        result = markdown_to_html_node(md)
        expected = """[HTMLNode(blockquote,quote starts here

nothing above
bye,None,None)]"""
        expected = f"HTMLNode(div,None,{expected},None)"
        self.assertEqual(repr(result),expected)
    def test_unordered_list(self):
        md = "* This is a list\n* with items"
        result = markdown_to_html_node(md)
        expected = "[HTMLNode(ul,None,[HTMLNode(li,This is a list,None,None), HTMLNode(li,with items,None,None)],None)]"
        expected = f"HTMLNode(div,None,{expected},None)"
        self.assertEqual(repr(result),expected)
    def test_ordered_lsit(self):
        md = "1.This is a list\n2.with ordered items"
        result = markdown_to_html_node(md)
        expected = "[HTMLNode(ol,None,[HTMLNode(li,This is a list,None,None), HTMLNode(li,with ordered items,None,None)],None)]"
        expected = f"HTMLNode(div,None,{expected},None)"
        self.assertEqual(repr(result),expected)
