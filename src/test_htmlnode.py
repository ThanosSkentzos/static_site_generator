import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a","google","",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        expected = ' href="https://www.google.com" target="_blank"'
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

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_props(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("a", "Click me!", {"href": "https://www.google.com"})
                ],
            )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<a href="https://www.google.com">Click me!</a></p>'
        self.assertEqual(node.to_html(), expected)

    def test_no_children(self):
        node = ParentNode("p",None)
        try:
            node.to_html()
        except ValueError as v:
            self.assertEqual(1,1)
        except Exception:
            self.assertEqual(1,0)

    def test_0_children(self):
        node = ParentNode("p",[])
        try:
            node.to_html()
        except ValueError as v:
            self.assertEqual(1,1)
        except Exception:
            self.assertEqual(1,0)


if __name__ == "__main__":
    unittest.main()
