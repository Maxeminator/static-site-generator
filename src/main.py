from textnode import TextNode, TextType

def main():
    node = TextNode("This is some anchorn text", TextType.LINKS, "http://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()