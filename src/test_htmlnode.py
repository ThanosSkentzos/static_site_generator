import unittest

from htmlnode import HTMLNode,LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a","google","",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        expected = '<p>This is a paragraph of text.</p>'
        self.assertEqual(leaf.to_html(), expected)
    def test_to_html_props(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf.to_html(),expected)
if __name__ == "__main__":
    unittest.main()
