import unittest,textnode,htmlnode

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_something(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    def test_none(self):
        node = HTMLNode("a", "click me", None, None)
        self.assertEqual(node.props_to_html(), '')
    def test_empty_props(self):
        node = HTMLNode("p", "hello", None, {})
        self.assertEqual(node.props_to_html(), "")
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "click me", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">click me</a>')
    def test_leaf_to_html_p3(self):
        node = LeafNode("a", None, {"href": "https://example.com"})
        with self.assertRaises(ValueError):
            node.to_html()
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
    def test_if_no_children(self):
        node = ParentNode("b",None,"props")
        with self.assertRaises(ValueError):
            node.to_html()
if __name__ == "__main__":
    unittest.main()