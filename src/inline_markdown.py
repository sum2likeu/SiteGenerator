from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode,HTMLNode
import re
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        elif delimiter not in n.text:
            new_nodes.append(n)
        else:
            sections = n.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            index = 0
            for i,section in enumerate(sections):
                if i % 2 == 0:
                    new_nodes.append(TextNode(section,TextType.TEXT))
                else:
                    new_nodes.append(TextNode(section,text_type))
    return new_nodes
def extract_markdown_images(text):
    matches = re.findall((r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"),text)
    return matches
def extract_markdown_links(text):
    matches = re.findall((r"\[([^\[\]]*)\]\(([^\(\)]*)\)"), text)
    return matches
def split_nodes_image(old_nodes):
    output = []
    for node in old_nodes:
        links = extract_markdown_images(node.text)
        remaining = node.text
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        if len(links) == 0:
            output.append(node)
            continue
        for link_text, url in links:
            markdown = f"![{link_text}]({url})"
            sections = remaining.split(f"![{link_text}]({url})", 1)
            if sections[0] != "":
                output.append(TextNode(sections[0], TextType.TEXT))
            output.append(TextNode(link_text, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining != "":
            output.append(TextNode(remaining, TextType.TEXT))
    return output
def split_nodes_link(old_nodes):
    output = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        remaining = node.text
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        if len(links) == 0:
            output.append(node)
            continue
        for link_text, url in links:
            markdown = f"[{link_text}]({url})"
            sections = remaining.split(f"[{link_text}]({url})", 1)
            if sections[0] != "":
                output.append(TextNode(sections[0], TextType.TEXT))
            output.append(TextNode(link_text, TextType.LINK, url))
            remaining = sections[1]
        if remaining != "":
            output.append(TextNode(remaining, TextType.TEXT))
    return output
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD) 
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)  
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
def markdown_to_blocks(markdown):
    strings = markdown.split("\n\n")
    finalstring = []
    for s in strings:
        if s.strip() != "":
            finalstring.append(s.strip())
    return finalstring
def block_to_block_type(text):
    if text.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    codelines = text.split("\n")
    if codelines[0].startswith("```") and codelines[-1].endswith("```") and len(codelines) > 1:
        return BlockType.CODE
    if text.startswith(">"):
        for l in codelines:
            if not l.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if text.startswith("- "):
        for l in codelines:
            if not l.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    n = 1
    if text.startswith(f"{n}. "):
        for l in codelines:
            if not l.startswith(f"{n}. "):
                return BlockType.PARAGRAPH
            n+=1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for b in blocks:
        if block_to_block_type(b) == BlockType.HEADING:
            node = head_to_html(b)
        elif block_to_block_type(b) == BlockType.PARAGRAPH:
            text = b.replace("\n", " ")
            il_children = text_to_children(text)
            node = ParentNode("p", il_children)
        elif block_to_block_type(b) == BlockType.CODE:
            if not b.startswith("```") or not b.endswith("```"):
                raise ValueError("invalid code block")
            text = b[4:-3]
            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code = ParentNode("code", [child])
            node = ParentNode("pre", [code])
        elif block_to_block_type(b) == BlockType.ORDERED_LIST:
            items = b.split("\n")
            html_items = []
            for item in items:
                parts = item.split(". ", 1)
                text = parts[1]
                il_children = text_to_children(text)
                html_items.append(ParentNode("li", il_children))
            node = ParentNode("ol", html_items)
        elif block_to_block_type(b) == BlockType.UNORDERED_LIST:
            items = b.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                il_children = text_to_children(text)
                html_items.append(ParentNode("li", il_children))
            node = ParentNode("ul", html_items)
        elif block_to_block_type(b) == BlockType.QUOTE:
            lines = b.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            il_children = text_to_children(content)
            node = ParentNode("blockquote", il_children)
        children.append(node)

    parent = ParentNode("div",children)
    return parent
def text_to_children(text):
    nlist = text_to_textnodes(text)
    html_list = []
    for l in nlist:
      html_list.append(text_node_to_html_node(l))
    return html_list
def head_to_html(b):
    if b.startswith("# "):
        children = text_to_children(b[2:])
        return ParentNode("h1",children)
    elif b.startswith("## "):
        children = text_to_children(b[3:])
        return ParentNode("h2",children)
    elif b.startswith("### "):
        children = text_to_children(b[4:])
        return ParentNode("h3",children)
    elif b.startswith("#### "):
        children = text_to_children(b[5:])
        return ParentNode("h4",children)
    elif b.startswith("##### "):
        children = text_to_children(b[6:])
        return ParentNode("h5",children)
    elif b.startswith("###### "):
        children = text_to_children(b[7:])
        return ParentNode("h6",children)


