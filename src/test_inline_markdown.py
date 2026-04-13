import unittest
import inline_markdown
from inline_markdown import (
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
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
    def test_split_link(self):
        node = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    def test_split_image_non_text_node(self):
        node = TextNode("**bold text**", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("**bold text**", TextType.BOLD)],
            new_nodes,
    )
    def test_split_link_non_text_node(self):
        node = TextNode("**bold text**", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("**bold text**", TextType.BOLD)],
            new_nodes,
    )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
])
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



if __name__ == "__main__":
    unittest.main()
    def test_heading(self):
        block = "# Hello World"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    def test_code(self):
        block = "```\nHello World```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    def test_quote(self):
        block = "> Hello World\n> World Hello"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    def test_unordered_list(self):
        block = "- Hello World\n - World Hello"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    def test_ordered_list(self):
        block = "1. Hello World\n2. World Hello"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    def test_paragraph(self):
        block = "Hello World"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_invalid_list(self):
        block = "2. Hello World\n 1. World Hello"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_invalid_quote(self):
        block = "> Hello World\n World Hello"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)