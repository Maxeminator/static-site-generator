import unittest

from node_splitter import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestExtractors(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node=TextNode(
            "This is text with an [google](https://google.com) and another [yandex](https://yandex.ru)",
            TextType.TEXT,
        )
        new_nodes=split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("google",TextType.LINK,"https://google.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("yandex", TextType.LINK, "https://yandex.ru"),
            ],
            new_nodes,
        )

        
    def test_split_images_links(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [google](https://google.com)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and [google](https://google.com)", TextType.TEXT),
                ],
                new_nodes,
            )
    
    def test_split_links_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [google](https://google.com)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ", TextType.TEXT),
                    TextNode("google", TextType.LINK,"https://google.com")
                ],
                new_nodes,
            )
    
    def test_split_links_images_combined(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [google](https://google.com)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            new_nodes= split_nodes_image(new_nodes)
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("google", TextType.LINK,"https://google.com")
                ],
                new_nodes,
            )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
    
    def test_split_link_single(self):
        node = TextNode(
            "[google](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("google", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )