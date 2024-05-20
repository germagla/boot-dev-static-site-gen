import os
import shutil

from page import generate_pages_recursive


def main():
    src = os.path.abspath("./static")
    dst = os.path.abspath("./public")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    copy_contents(src, dst)

    generate_pages_recursive(
        os.path.abspath("./content"),
        os.path.abspath("./template.html"),
        os.path.abspath("./public"),
    )


def copy_contents(src, dst):
    if not os.path.isdir(src):
        raise ValueError(f"{src} is not a directory")
    if not os.path.isdir(dst):
        os.mkdir(dst)
    # print(f"Copying the contents of {src} to {dst}")
    for item in os.listdir(src):
        item_path = os.path.join(src, item)  # Get the full path of the item
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        if os.path.isdir(item_path):
            copy_contents(item_path, os.path.join(dst, item))


if __name__ == "__main__":
    main()
