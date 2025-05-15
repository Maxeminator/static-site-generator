import unittest
from textnode import TextNode, TextType
from node_splitter import text_to_textnodes  

class TestTextToTextNodes(unittest.TestCase):
    def test_basic_formatting(self):
        
        text = "This is **bold** and this is _italic_ and this is `code`."
        
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(len(result), len(expected), 
                         f"Expected {len(expected)} nodes, got {len(result)}")
        
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text, 
                           f"Node {i} text mismatch")
            self.assertEqual(result[i].text_type, expected[i].text_type, 
                           f"Node {i} type mismatch")

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
        
if __name__ == "__main__":
    unittest.main()