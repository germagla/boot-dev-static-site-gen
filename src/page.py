import os.path

from block_markdown import markdown_to_html


def extract_title(markdown):
    title = None
    for line in markdown.splitlines():
        if line.startswith("# "):
            if not title:
                title = line[2:]
            else:
                raise ValueError("Multiple titles found")
    if title:
        return title
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    title = extract_title(markdown)
    html = markdown_to_html(markdown).to_html()
    with open(template_path, "r") as f:
        template = f.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path, template_path, des_dir_path):
    for item in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, item)):
            if item.endswith(".md"):
                generate_page(
                    os.path.join(dir_path, item),
                    template_path,
                    os.path.join(des_dir_path, item.replace(".md", ".html")),
                )
        if os.path.isdir(os.path.join(dir_path, item)):
            generate_pages_recursive(
                os.path.join(dir_path, item),
                template_path,
                os.path.join(des_dir_path, item),
            )
