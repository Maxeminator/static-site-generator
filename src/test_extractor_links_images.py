import unittest

from node_splitter import extract_markdown_images, extract_markdown_links

class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [to google](https://www.google.com)"
        )
        self.assertListEqual([("to google","https://www.google.com")],matches)
    
    def test_extract_multi_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![darkest secret](https://i.imgur.com/aKaOqIh.gif)" 
        )
        self.assertListEqual([("image","https://i.imgur.com/zjjcJKZ.png"),("darkest secret","https://i.imgur.com/aKaOqIh.gif")],matches)

if __name__ == "__main__":

    unittest.main()