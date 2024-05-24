import re


def markdown_escape(message: str):
    return re.sub(r'[_*[\]()~>#\+\-=|{}.!]', lambda x: '\\' + x.group(), message)
