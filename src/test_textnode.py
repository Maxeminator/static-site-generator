import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_url_type(self):
        node = TextNode("This is a text node", TextType.BOLD,url="http://www.boot.dev")
        node2 = TextNode("Text", TextType.ITALIC,url="")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node= TextNode("This is bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold node")

    def test_italic(self):
        node= TextNode("This is italic node", TextType.ITALIC)
        html_node= text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value,"This is italic node")

    def test_code(self):
        node= TextNode("This is code node", TextType.CODE)
        html_node= text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value,"This is code node")
    
    def test_link(self):
        node= TextNode("Click me", TextType.LINK, "https://boot.dev")
        html_node= text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props["href"], "https://boot.dev")

    def test_image(self):
        node = TextNode("Alt text",TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"],"https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text")

if __name__ == "__main__":

    unittest.main()