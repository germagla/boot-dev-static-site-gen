import unittest

from inline_markdown import *
from textnode import TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        nodes = [TextNode("This is a text node", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, "*", "bold"), nodes)

    def test_single_delimiter(self):
        nodes = [TextNode("This is a text node", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, "*", "bold"), nodes)

    def test_odd_delimiters(self):
        nodes = [TextNode("*This is a text node", "text")]
        self.assertRaises(ValueError, split_nodes_delimiter, nodes, "*", "bold")

    def test_even_delimiters(self):
        nodes = [TextNode("*This is a text node*", "text")]
        new_nodes = [TextNode("This is a text node", "bold")]
        self.assertEqual(split_nodes_delimiter(nodes, "*", "bold"), new_nodes)

    def test_multiple_delimiters(self):
        nodes = [TextNode("*This is a text node* and *this is another*", "text")]
        new_nodes = [
            TextNode("This is a text node", "bold"),
            TextNode(" and ", "text"),
            TextNode("this is another", "bold"),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", "bold"), new_nodes)

    def test_does_not_start_with_delimiter(self):
        nodes = [TextNode("This is a text *node* and *this is another*", "text")]
        new_nodes = [
            TextNode("This is a text ", "text"),
            TextNode("node", "bold"),
            TextNode(" and ", "text"),
            TextNode("this is another", "bold"),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", "bold"), new_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_images(self):
        text = "This is a text node"
        self.assertEqual(extract_markdown_images(text), [])

    def test_single_image(self):
        text = "This is a text node ![alt text](https://www.google.com)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "https://www.google.com")])

    def test_multiple_images(self):
        text = "This is a text node ![alt text](https://www.google.com) and ![another](https://www.google.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://www.google.com"), ("another", "https://www.google.com")],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_no_links(self):
        text = "This is a text node"
        self.assertEqual(extract_markdown_links(text), [])

    def test_single_link(self):
        text = "This is a text node [link text](https://www.google.com)"
        self.assertEqual(extract_markdown_links(text), [("link text", "https://www.google.com")])

    def test_multiple_links(self):
        text = "This is a text node [link text](https://www.google.com) and [another](https://www.google.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link text", "https://www.google.com"), ("another", "https://www.google.com")],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_no_images(self):
        nodes = [TextNode("This is a text node", "text")]
        self.assertEqual(split_nodes_image(nodes), nodes)

    def test_single_image(self):
        nodes = [TextNode("This is a text node ![alt text](https://www.google.com)", "text")]
        new_nodes = [
            TextNode("This is a text node ", "text"),
            TextNode("alt text", "image", "https://www.google.com"),
        ]
        self.assertEqual(split_nodes_image(nodes), new_nodes)

    def test_multiple_images(self):
        nodes = [
            TextNode("This is a text node ![alt text](https://www.google.com) and ![another](https://www.google.com)",
                     "text")]
        new_nodes = [
            TextNode("This is a text node ", "text"),
            TextNode("alt text", "image", "https://www.google.com"),
            TextNode(" and ", "text"),
            TextNode("another", "image", "https://www.google.com"),
        ]
        self.assertEqual(split_nodes_image(nodes), new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        nodes = [TextNode("This is a text node", "text")]
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_single_link(self):
        nodes = [TextNode("This is a text node [link text](https://www.google.com)", "text")]
        new_nodes = [
            TextNode("This is a text node ", "text"),
            TextNode("link text", "link", "https://www.google.com"),
        ]
        self.assertEqual(split_nodes_link(nodes), new_nodes)

    def test_multiple_links(self):
        nodes = [
            TextNode("This is a text node [link text](https://www.google.com) and [another](https://www.google.com)",
                     "text")]
        new_nodes = [
            TextNode("This is a text node ", "text"),
            TextNode("link text", "link", "https://www.google.com"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.google.com"),
        ]
        self.assertEqual(split_nodes_link(nodes), new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_boot_dev_test(self):
        text = ("This is **text** with an *italic* word and a `code block` and an ![image]("
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link]("
                "https://boot.dev)")
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TEXT_TYPES["text_type_text"]),
                TextNode("text", TEXT_TYPES["text_type_bold"]),
                TextNode(" with an ", TEXT_TYPES["text_type_text"]),
                TextNode("italic", TEXT_TYPES["text_type_italic"]),
                TextNode(" word and a ", TEXT_TYPES["text_type_text"]),
                TextNode("code block", TEXT_TYPES["text_type_code"]),
                TextNode(" and an ", TEXT_TYPES["text_type_text"]),
                TextNode("image", TEXT_TYPES["text_type_image"],
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", TEXT_TYPES["text_type_text"]),
                TextNode("link", TEXT_TYPES["text_type_link"], "https://boot.dev"),
            ]
        )

    def test_no_markdown(self):
        text = "This is a text node"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is a text node", TEXT_TYPES["text_type_text"])])

    def test_no_closing_delimiter(self):
        text = "This is a text node **bold"
        self.assertRaises(ValueError, text_to_textnodes, text)


if __name__ == "__main__":
    unittest.main()
