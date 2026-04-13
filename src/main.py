import textnode
from textnode import TextNode,__eq__,__repr__
def main():
    print("hello world")
    new = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(__repr__(new))

main ()