import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestExtractors(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_block_to_block_type(self):

        self.assertEqual(
        block_to_block_type("This is **bolded** paragraph"),
        BlockType.PARAGRAPH
    )
    
        self.assertEqual(
        block_to_block_type("This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"),
        BlockType.PARAGRAPH
    )
    
        self.assertEqual(
        block_to_block_type("- This is a list\n- with items"),
        BlockType.UNORDERED_LIST
    )
    
        self.assertEqual(
        block_to_block_type("# Heading 1"),
        BlockType.HEADING
    )
    
        self.assertEqual(
        block_to_block_type("```\nsome code\n```"),
        BlockType.CODE
    )
    
        self.assertEqual(
        block_to_block_type(">This is a quote\n>Another line"),
        BlockType.QUOTE
    )
    
        self.assertEqual(
        block_to_block_type("1. First item\n2. Second item"),
        BlockType.ORDERED_LIST
    )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    

if __name__ == "__main__":

    unittest.main()