class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("error")
    def props_to_html(self):
        if self.props == None:
            return ""
        line = ""
        for key,value in self.props.items():
             line += f' {key}="{value}"'
        return line
    def __repr__(self):
        print(self.tag)
        print(self.value)
        print(self.children)
        print(self.props)
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
    def to_html(self):
        if self.value == None:
            raise ValueError("error")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,value=None,children=children,props=props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("error")
        if self.children == None:
            raise ValueError("no value")
        else:
            result = ""
            for n in self.children:
                result += n.to_html()
            return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
    