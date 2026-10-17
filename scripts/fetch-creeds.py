"""Extract the historical creeds verbatim from the user-selected source.

Only HTML markup and paragraph-edge layout whitespace are removed. The wording,
punctuation, numbering and internal whitespace of each paragraph are preserved.
"""
from html.parser import HTMLParser
from pathlib import Path
import hashlib, json, urllib.request

ROOT=Path(__file__).resolve().parent.parent
SOURCES=[('apostles','使徒信经','apostles-creed','我信神'),
         ('nicene','尼西亚信经','nicene-creed','我们信独一的神'),
         ('athanasian','亚他那修信经','athanasian-creed','1)')]

class Article(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.article=False;self.paragraph=False;self.parts=[];self.paragraphs=[]
    def handle_starttag(self,tag,attrs):
        if tag=='article': self.article=True
        if self.article and tag=='p':self.paragraph=True;self.parts=[]
        if self.paragraph and tag=='br':self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag=='p' and self.paragraph:
            self.paragraphs.append(''.join(self.parts).strip());self.paragraph=False
        if tag=='article':self.article=False
    def handle_data(self,data):
        if self.paragraph:self.parts.append(data)

output=[]
for slug,title,path,start in SOURCES:
    url='https://ccifellowship.org/books/book-of-praise/creeds/'+path
    with urllib.request.urlopen(url,timeout=40) as response: source=response.read().decode('utf-8')
    parsed=Article();parsed.feed(source)
    index=next(i for i,p in enumerate(parsed.paragraphs) if p.startswith(start))
    paragraphs=[p for p in parsed.paragraphs[index:] if p]
    assert paragraphs[-1].endswith(('阿们！','阿们!')), (slug,paragraphs[-1])
    text='\n\n'.join(paragraphs)
    output.append({'id':slug,'title':title,'source':url,'retrieved':'2026-10-17',
        'paragraphs':paragraphs,'sha256':hashlib.sha256(text.encode()).hexdigest()})
    print(slug,'paragraphs:',len(paragraphs),'characters:',len(text),'sha256:',output[-1]['sha256'])
(ROOT/'assets/creeds.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
