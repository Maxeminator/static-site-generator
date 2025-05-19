

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        list_html=[]
        for key , value in self.props.items():
            list_html.append(f' {key}="{value}"')
        string_html="".join(list_html)
        return string_html
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None or self.tag=="":
            return f"{self.value}"

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError ("Missing tag")
        if self.children is None:
            raise ValueError ("Missing child")
        childs=[]
        for child in self.children:
            childs.append(child.to_html())
        return f"<{self.tag}>{''.join(childs)}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"