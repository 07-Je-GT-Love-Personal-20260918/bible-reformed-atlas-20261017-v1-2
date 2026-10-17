"""Validate static links, fragment targets and complete source data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json

root=Path(__file__).resolve().parent.parent
public=root/'dist'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.duplicates=[];self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key=='id':
                if value in self.ids:self.duplicates.append(value)
                self.ids.add(value)
            if key in ('href','src') and value:self.links.append(value)

paths=[public/'index.html',public/'study.html',public/'creeds.html',*sorted((public/'books').glob('*.html'))]
cache={p.resolve():Page(p.read_text(encoding='utf-8')) for p in public.rglob('*.html')}
errors=[]
for path in paths:
    page=cache[path.resolve()]
    errors.extend(f'{path.name}: duplicate id {id}' for id in page.duplicates)
    for link in page.links:
        url=urlsplit(link)
        if url.scheme or url.netloc:continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path.resolve()
        if not target.exists():errors.append(f'{path.name}: missing {link}');continue
        if url.fragment and target.suffix=='.html':
            if unquote(url.fragment) not in cache[target].ids and url.fragment!='animated-atlas':
                errors.append(f'{path.name}: missing fragment {link}')
books=json.loads((root/'assets/books.json').read_text(encoding='utf-8'))['books']
assert len(books)==66
for book in books:
    for field in ['name','core','whole','context','why','what','local','christ','application']:
        assert book[field] and '???' not in book[field], (book['english'],field)
assert not (public/'CNAME').exists(), 'Stale Surge CNAME must not enter other deployments'
assert len(list((public/'books').glob('*.html')))==66
print('Static validation:',len(paths),'pages;',len(books),'complete book records;',len(errors),'link/fragment/id errors.')
for error in errors:print(error)
assert not errors
