import unittest

from textnode import TextNode, split_nodes_delimiter,text_node_to_html_node

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitDelimiter(unittest.TestCase):
    def test_code_case(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(repr(new_nodes),"[TextNode(This is text with a , text, None), TextNode(code block, code, None), TextNode( word, text, None)]")
        new_nodes = split_nodes_delimiter([node],'**',text_type_text)

    def test_bold_case(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(repr(new_nodes),"[TextNode(This is text with a , text, None), TextNode(bold block, bold, None), TextNode( word, text, None)]")
    def test_italic_case(self):
        node = TextNode("This is text with a *italic block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(repr(new_nodes),"[TextNode(This is text with a , text, None), TextNode(italic block, italic, None), TextNode( word, text, None)]")


if __name__ == "__main__":
    unittest.main()
