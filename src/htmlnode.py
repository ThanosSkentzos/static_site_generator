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
        return " ".join(f'{k}="{v}"' for k,v in self.props.items())

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props: dict = None) -> None:
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        else:
            return self.create_tag()
    def create_tag(self):
        return f'<{self.tag}{" " if self.props is not None else ""}{self.props_to_html()}>{self.value}</{self.tag}>'


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

if __name__=="__main__":
    main()
