from html import escape
from html.parser import HTMLParser
from urllib.parse import urlparse


ALLOWED_TAGS = {
    "p", "br", "strong", "em", "u", "s",
    "h2", "h3", "h4",
    "ul", "ol", "li",
    "blockquote", "a",
}

# El navegador usa etiquetas distintas según el comando de contenteditable.
# Se normalizan aquí para que el formato aplicado en el editor no se pierda
# al guardar el artículo.
TAG_ALIASES = {
    "b": "strong",
    "i": "em",
    "strike": "s",
    "del": "s",
    "div": "p",
}


class BlogHTMLSanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        tag = TAG_ALIASES.get(tag, tag)
        if tag not in ALLOWED_TAGS:
            return

        if tag == "br":
            self.parts.append("<br>")
            return

        allowed_attrs = []
        if tag == "a":
            for name, value in attrs:
                name = name.lower()
                if name == "href" and value:
                    parsed = urlparse(value.strip())
                    if parsed.scheme in ("http", "https", "mailto") or value.startswith("/"):
                        allowed_attrs.append(f'href="{escape(value, quote=True)}"')
                elif name == "title" and value:
                    allowed_attrs.append(f'title="{escape(value, quote=True)}"')

            self.parts.append("<a" + (" " + " ".join(allowed_attrs) if allowed_attrs else "") + ">")
        else:
            self.parts.append(f"<{tag}>")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        tag = tag.lower()
        tag = TAG_ALIASES.get(tag, tag)
        if tag in ALLOWED_TAGS and tag != "br":
            self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(escape(data))

    def get_html(self):
        return "".join(self.parts)


def sanitize_blog_html(value):
    parser = BlogHTMLSanitizer()
    parser.feed(value or "")
    parser.close()
    return parser.get_html()
