import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):

    def test_tag(self):
        node = HTMLNode(None, "test")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value,"test")

    def test_children(self):
        child=HTMLNode("b","bold")
        node = HTMLNode("p", None, [child], None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [child])

    def test_value(self):
        node=HTMLNode("p", "just text")
        self.assertEqual(node.value,"just text")
        self.assertIsNone(node.children)

    def test_props(self):
        prop={"href": "https://a.b"}
        node=HTMLNode(None, None, None, prop)
        self.assertEqual(node.props_to_html(), ' href="https://a.b"')

        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node2.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_prop(self):
        prop={"href": "https://a.b"}
        node = LeafNode("a", "Hello, world!",prop)
        self.assertEqual(node.to_html(), '<a href="https://a.b">Hello, world!</a>')  

    def test_leaf_to_html_a_child(self):
        with self.assertRaises(ValueError):
            LeafNode("a",None,None).to_html()

    def test_leaf_to_html_a_tag(self):
        node=LeafNode(None,"Test")
        self.assertEqual(node.to_html(),"Test")
        

if __name__ == "__main__":

    unittest.main()