class TextNode():
    def __init__(self,text,text_type,url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other) -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
    def __repr__(self) -> str:
        return(f"TextNode({self.text},{self.text_type},{self.url})")

def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)

if __name__=="__main__":
    main()
