import re

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_htmlnodes

BLOCK_TYPES = {
    "block_type_paragraph": "paragraph",
    "block_type_heading": "heading",
    "block_type_code": "code",
    "block_type_quote": "quote",
    "block_type_unordered_list": "unordered_list",
    "block_type_ordered_list": "ordered_list",
}


def markdown_to_blocks(text):
    return [block.strip() for block in text.split("\n\n") if block != ""]


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BLOCK_TYPES["block_type_heading"]
    if len(block.splitlines()) > 1 and block.startswith("```") and block.endswith("```"):
        return BLOCK_TYPES["block_type_code"]
    if block.startswith(">"):
        for line in block.splitlines():
            if not line.startswith(">"):
                # raise ValueError("Invalid markdown: All lines in a quote block must start with '>'")
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_quote"]
    if block.startswith("* ") or block.startswith("- "):
        for line in block.splitlines():
            if not line.startswith("* ") and not line.startswith("- "):
                # raise ValueError("Invalid markdown: All lines in a list block must start with '* ' or '- '")
                return BLOCK_TYPES["block_type_paragraph"]
        return BLOCK_TYPES["block_type_unordered_list"]
    if block.startswith("1. "):
        n = 1
        for line in block.splitlines():
            if not line.startswith(f"{n}. "):
                # raise ValueError("Invalid markdown: Invalid ordered list numbering")
                return BLOCK_TYPES["block_type_paragraph"]
            n += 1
        return BLOCK_TYPES["block_type_ordered_list"]
    return BLOCK_TYPES["block_type_paragraph"]


def paragraph_block_to_html_node(block):
    # return f"<p>{block}</p>"
    return ParentNode("p", text_to_htmlnodes(block))


def heading_block_to_html_node(block):
    groups = re.match(r"^(#{1,6}) (.*)", block).groups()
    level = len(groups[0])
    # return f"<h{level}>{groups[1]}</h{level}>"
    return ParentNode(f"h{level}", text_to_htmlnodes(groups[1]))


def code_block_to_html_node(block):
    # return f"<pre><code>{block.strip("```").strip()}</code></pre>"
    return ParentNode("pre", [LeafNode("code", block.strip("```").strip())])


def quote_block_to_html_node(block):
    # return f"<blockquote>{"\n".join([line[2:] for line in block.splitlines()])}</blockquote>"
    return LeafNode("blockquote", "\n".join([line[2:] for line in block.splitlines()]))


def ul_block_to_html_node(block):
    items = [f"<li>{line[2:]}</li>" for line in block.splitlines()]
    # return f"<ul>{''.join(items)}</ul>"
    return ParentNode("ul", [ParentNode("li", text_to_htmlnodes(line[2:])) for line in block.splitlines()])


def ol_block_to_html_node(block):
    items = [f"<li>{line[3:]}</li>" for line in block.splitlines()]
    # return f"<ol>{''.join(items)}</ol>"
    return ParentNode("ol", [ParentNode("li", text_to_htmlnodes(line[3:])) for line in block.splitlines()])


CONVERTERS = {
    BLOCK_TYPES["block_type_paragraph"]: paragraph_block_to_html_node,
    BLOCK_TYPES["block_type_heading"]: heading_block_to_html_node,
    BLOCK_TYPES["block_type_code"]: code_block_to_html_node,
    BLOCK_TYPES["block_type_quote"]: quote_block_to_html_node,
    BLOCK_TYPES["block_type_unordered_list"]: ul_block_to_html_node,
    BLOCK_TYPES["block_type_ordered_list"]: ol_block_to_html_node,
}


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        nodes.append(CONVERTERS[block_type](block))
    return ParentNode("div", nodes)
