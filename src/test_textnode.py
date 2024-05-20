import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_vs_no_url(self):
        node = TextNode("This is a text node", "italic", "url")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_diff_test_type(self):
        node = TextNode("This is a text node", "code")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)


class TestNodeToHTMLNode(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("This is a text node", "text")
        self.assertEqual(text_node_to_html_node(node).to_html(), "This is a text node")

    def test_text_type_bold(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>This is a text node</b>")

    def test_text_type_italic(self):
        node = TextNode("This is a text node", "italic")
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>This is a text node</i>")

    def test_text_type_code(self):
        node = TextNode("This is a text node", "code")
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>This is a text node</code>")

    def test_text_type_link(self):
        node = TextNode("This is a text node", "link", "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<a href="https://www.google.com">This is a text node</a>',
        )

    def test_text_type_image(self):
        node = TextNode("This is a text node", "image", "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<img src="https://www.google.com" alt="This is a text node"></img>',
        )

    def test_invalid_text_type(self):
        node = TextNode("This is a text node", "invalid")
        self.assertRaises(ValueError, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()
