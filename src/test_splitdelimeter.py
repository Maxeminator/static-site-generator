import unittest
from textnode import TextNode, TextType
from node_splitter import split_nodes_delimiter 

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_no_delimiter(self):
        # Test with text that has no delimiters
        node = TextNode("This is plain text with no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is plain text with no delimiters")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_bold_delimiter(self):
        # Test with text that has bold delimiters
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("**Bold** and `code`", TextType.TEXT)
        bold_result = split_nodes_delimiter([node], "**", TextType.BOLD)
        code_result = split_nodes_delimiter(bold_result, "`", TextType.CODE)
        self.assertEqual(len(code_result), 3)
        
if __name__ == "__main__": 
    unittest.main()