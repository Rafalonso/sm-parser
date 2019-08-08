from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import io


def pdfparser(data):
    if isinstance(data, str):
        fp = open(data, 'rb')
    else:
        fp = io.BytesIO(data)
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    return data


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_html_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def goto_element(xpath, dom):
    root = ET.fromstring(dom)
    try:
        elem = root.find(xpath)
    except SyntaxError:
        elem = root.find(".{}".format(xpath))
    retstr = io.StringIO()
    ET.ElementTree(elem).write(retstr, encoding='unicode')
    retstr.seek(0)
    return retstr.read()
