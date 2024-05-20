import unittest

from block_markdown import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_boot_dev_test(self):
        markdown = (
            "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis "
            "is the same paragraph on a new line\n\n* This is a list\n* with items")
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class BlockToBlockTypeTest(unittest.TestCase):
    def test_identifies_heading(self):
        self.assertEqual(block_to_block_type("# Heading"),
                         BLOCK_TYPES["block_type_heading"])
        self.assertEqual(block_to_block_type("## Heading"),
                         BLOCK_TYPES["block_type_heading"])
        self.assertEqual(block_to_block_type("###### Heading"),
                         BLOCK_TYPES["block_type_heading"])

    def test_identifies_code(self):
        self.assertEqual(block_to_block_type("```\ncode```"),
                         BLOCK_TYPES["block_type_code"])
        self.assertEqual(block_to_block_type("```code\n```"),
                         BLOCK_TYPES["block_type_code"])

    def test_identifies_quote(self):
        self.assertEqual(block_to_block_type("> quote"), BLOCK_TYPES["block_type_quote"])
        self.assertEqual(block_to_block_type("> quote\n> quote"),
                         BLOCK_TYPES["block_type_quote"])

    def test_identifies_unordered_list(self):
        self.assertEqual(block_to_block_type("* item\n* item"),
                         BLOCK_TYPES["block_type_unordered_list"])
        self.assertEqual(block_to_block_type("- item\n- item"),
                         BLOCK_TYPES["block_type_unordered_list"])

    def test_identifies_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item\n2. item"),
                         BLOCK_TYPES["block_type_ordered_list"])

    def test_identifies_paragraph(self):
        self.assertEqual(block_to_block_type("paragraph"),
                         BLOCK_TYPES["block_type_paragraph"])

    def test_identifies_paragraph_with_seven_hashes(self):
        self.assertEqual(block_to_block_type("####### Heading"),
                         BLOCK_TYPES["block_type_paragraph"])

    def test_identifies_paragraph_without_end_triple_backtick(self):
        self.assertEqual(block_to_block_type("```code"),
                         BLOCK_TYPES["block_type_paragraph"])

    def test_identifies_paragraph_without_greater_than_symbol(self):
        self.assertEqual(block_to_block_type("quote"),
                         BLOCK_TYPES["block_type_paragraph"])

    def test_identifies_paragraph_without_bullet_point(self):
        self.assertEqual(block_to_block_type("item"), BLOCK_TYPES["block_type_paragraph"])

    def test_identifies_paragraph_with_incorrect_numbering(self):
        self.assertEqual(block_to_block_type("2. item"),
                         BLOCK_TYPES["block_type_paragraph"])


class BlockTypeToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(paragraph_block_to_html_node("paragraph").to_html(), "<p>paragraph</p>")

    def test_heading(self):
        self.assertEqual(heading_block_to_html_node("# Heading").to_html(), "<h1>Heading</h1>")
        self.assertEqual(heading_block_to_html_node("## Heading").to_html(), "<h2>Heading</h2>")
        self.assertEqual(heading_block_to_html_node("###### Heading").to_html(), "<h6>Heading</h6>")

    def test_code(self):
        self.assertEqual(code_block_to_html_node("```\ncode```").to_html(), "<pre><code>code</code></pre>")
        self.assertEqual(code_block_to_html_node("```code\n```").to_html(), "<pre><code>code</code></pre>")

    def test_quote(self):
        self.assertEqual(quote_block_to_html_node("> quote\n> quote").to_html(),
                         "<blockquote>quote\nquote</blockquote>")

    def test_ul(self):
        self.assertEqual(ul_block_to_html_node("* item\n* item").to_html(), "<ul><li>item</li><li>item</li></ul>")
        self.assertEqual(ul_block_to_html_node("- item\n- item").to_html(), "<ul><li>item</li><li>item</li></ul>")

    def test_ol(self):
        self.assertEqual(ol_block_to_html_node("1. item\n2. item").to_html(), "<ol><li>item</li><li>item</li></ol>")


class TestMarkdownToHTML(unittest.TestCase):
    def test_boot_dev_test(self):
        markdown = (
            "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis "
            "is the same paragraph on a new line\n\n* This is a list\n* with items")
        html = markdown_to_html(markdown).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here\nThis is the same paragraph on a new line</p><ul><li>This is a list</li><li>with "
            "items</li></ul></div>",
        )


if __name__ == '__main__':
    unittest.main()
