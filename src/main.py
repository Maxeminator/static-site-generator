from textnode import TextNode, TextType
import os
import shutil

def copy_static(src, dst, first_call=True):
    if os.path.exists(dst) and first_call:
        shutil.rmtree(dst)
        print(f"Created new folder {dst}")
        os.mkdir(dst)
    elif not os.path.exists(dst):
        print(f"Created new folder {dst}")
        os.mkdir(dst)
    for entry in os.listdir(src):
        src_path=os.path.join(src, entry)
        dst_path=os.path.join(dst, entry)
        if os.path.isfile(src_path):
            print(f"Copied {src_path} → {dst_path}")
            shutil.copy(src_path,dst_path)
        else:
            print(f"Created new folder {dst_path}")
            os.mkdir(dst_path)
            copy_static(src_path, dst_path,first_call=False)
    

def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))  # путь до src/main.py
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))  # подняться в корень проекта

    static_path = os.path.join(root_dir, "static")
    public_path = os.path.join(root_dir, "public")

    node = TextNode("This is some anchorn text", TextType.LINK, "http://www.boot.dev")
    print(node)
    copy_static(static_path, public_path)

if __name__ == "__main__":
    main()