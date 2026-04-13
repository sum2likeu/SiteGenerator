import unittest,htmlnode

from textnode import TextNode, TextType,text_node_to_html_node
from inline_markdown import split_nodes_delimiter,extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_link
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node again", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD,"https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node") 
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node") 
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE,"https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "This is a text node")
    def test_link(self):
        node = TextNode("This <a< node", TextType.TEXT)
        html_node = split_nodes_delimiter([node],"<",TextType.TEXT)
        self.assertEqual(html_node, [
            TextNode("This ", TextType.TEXT),
            TextNode("a", TextType.TEXT),  # between the delimiters
            TextNode(" node", TextType.TEXT),
        ])
    def test_bold(self):
        node = TextNode("This **a** node", TextType.TEXT)
        html_node = split_nodes_delimiter([node],"**",TextType.BOLD)
        self.assertEqual(html_node, [
            TextNode("This ", TextType.TEXT),
            TextNode("a", TextType.BOLD),  # between the delimiters
            TextNode(" node", TextType.TEXT),
            ])
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    


if __name__ == "__main__":
    unittest.main()