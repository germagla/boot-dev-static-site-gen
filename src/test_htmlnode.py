import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


class TestParentNode(unittest.TestCase):
    def test_no_tag_raises_value_error(self):
        node = ParentNode(None, children=[LeafNode(None, "Normal text")])
        self.assertRaises(ValueError, node.to_html)

    def test_no_children_raises_value_error(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)

    def test_base_case(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nesting(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ]),
            ParentNode("p", [
                LeafNode("i", "italic text")
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text</p><p><i>italic text</i></p></div>"
        )


class TestLeafNode(unittest.TestCase):
    def test_tag(self):
        node = LeafNode(tag="a", value="Google", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_no_tag(self):
        node = LeafNode(None, value="No tag")
        self.assertEqual(node.to_html(), 'No tag')


if __name__ == "__main__":
    unittest.main()
