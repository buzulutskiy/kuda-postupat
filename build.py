"""Вшивает src/*.js прямо в страницы: блокировщики рекламы режут внешние .js."""
import re, os
PAGES={'znakomstvo.html':['zadaniya.js'],
       'vzvesit.html':['subjdata.js','grpdesc.js','tasks.js','app.js']}
for page,js in PAGES.items():
    html=open(page).read()
    inline='\n'.join(f'<script>\n/* {n} */\n'+open(os.path.join('src',n)).read().rstrip()+'\n</script>' for n in js)
    marker='<!--JS-->'
    if marker in html:
        html=re.sub(r'<!--JS-->.*?<!--/JS-->', marker+'\n'+inline+'\n<!--/JS-->', html, flags=re.S)
    else:
        first=re.search(r'<script src="[^"]+"></script>', html)
        html=re.sub(r'(<script src="[^"]+"></script>\s*)+', marker+'\n'+inline+'\n<!--/JS-->\n', html, count=1)
    open(page,'w').write(html)
    print(page, len(html)//1024, 'КБ')
