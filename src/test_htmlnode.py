import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_to_html_parent_empty_children(self):
        parent_node=ParentNode("div",[])
        self.assertEqual(parent_node.to_html(),"<div></div>")
    
    def test_to_html_parent_none_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div",None).to_html()
        self.assertEqual(str(context.exception), "Missing child")
    
    def test_to_html_parent_none_tag(self):
        child_node=LeafNode("b","GigaTest")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child_node]).to_html()
        self.assertEqual(str(context.exception), "Missing tag")

if __name__ == "__main__":

    unittest.main()