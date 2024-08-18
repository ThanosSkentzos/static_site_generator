class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props:dict=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props = ""
        for k,v in self.props.items():
            props += f' {k}="{v}"'
        return props

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props: dict = None) -> None:
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props: dict = None) -> None:
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have children.")
        children_html ="".join([child.to_html() for child in self.children])
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

def main():
    node = HTMLNode("a","google",[],
        {
            "href": "https://www.google.com",
            "target": "_blank",
        })
    print(node)
    print(node.props_to_html())

    leaf = LeafNode("p", "This is a paragraph of text.")
    print(leaf)
    print(leaf.to_html())

    leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leaf2)
    print(leaf2.to_html())

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())

if __name__=="__main__":
    main()
