import re

from textnode import TextNode, TEXT_TYPES, text_node_to_html_node


def text_to_htmlnodes(text):
    return [text_node_to_html_node(textnode) for textnode in text_to_textnodes(text)]


def text_to_textnodes(text):
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [
                            TextNode(text, TEXT_TYPES["text_type_text"])
                        ], "`", TEXT_TYPES["text_type_code"]
                    )
                    , "**", TEXT_TYPES["text_type_bold"]
                )
                , "*", TEXT_TYPES["text_type_italic"]
            )
        )
    )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TEXT_TYPES["text_type_text"]:

            if node.text.count(delimiter) % 2 != 0:
                raise ValueError(f"Invalid markdown: no closing delimiter ({delimiter})")

            split_nodes = node.text.split(delimiter)
            for i, part in enumerate(split_nodes):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TEXT_TYPES["text_type_text"]))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TEXT_TYPES["text_type_text"]:
            new_nodes.append(node)
            continue
        text = node.text
        parts = re.split(r"!\[.*?\]\(.*?\)", text)
        image_tuples = extract_markdown_images(text)
        i = 0
        while i < len(parts):
            if parts[i] != "":
                new_nodes.append(TextNode(parts[i], TEXT_TYPES["text_type_text"]))
            if i < len(image_tuples):
                new_nodes.append(TextNode(image_tuples[i][0], TEXT_TYPES["text_type_image"], image_tuples[i][1]))
            i += 1
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TEXT_TYPES["text_type_text"]:
            new_nodes.append(node)
            continue
        text = node.text
        parts = re.split(r"\[.*?\]\(.*?\)", text)
        link_tuples = extract_markdown_links(text)
        i = 0
        while i < len(parts):
            if parts[i] != "":
                new_nodes.append(TextNode(parts[i], TEXT_TYPES["text_type_text"]))
            if i < len(link_tuples):
                new_nodes.append(TextNode(link_tuples[i][0], TEXT_TYPES["text_type_link"], link_tuples[i][1]))
            i += 1
    return new_nodes
