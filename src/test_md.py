import unittest

from markdown import block_to_block_type, markdown_to_blocks

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
