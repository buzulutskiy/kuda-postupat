"""Вшивает src/*.js прямо в страницы: блокировщики рекламы режут внешние .js."""
import re, os
PAGES={'znakomstvo.html':['zadaniya.js'],
       'vzvesit.html':['subjdata.js','grpdesc.js','tasks.js','na60.js','app.js']}
PROGS_PAGES=['index.html','vzvesit.html']
PROGS=open(os.path.join('src','progs.js')).read().strip()

for page in PROGS_PAGES:
    html=open(page).read()
    html=re.sub(r'/\*PROGS\*/.*?/\*/PROGS\*/', lambda m: '/*PROGS*/'+PROGS+'/*/PROGS*/', html, flags=re.S)
    open(page,'w').write(html)

for page,js in PAGES.items():
    html=open(page).read()
    inline='\n'.join(f'<script>\n/* {n} */\n'+open(os.path.join('src',n)).read().rstrip()+'\n</script>' for n in js)
    marker='<!--JS-->'
    if marker in html:
        html=re.sub(r'<!--JS-->.*?<!--/JS-->', marker+'\n'+inline+'\n<!--/JS-->', html, flags=re.S)
    else:
        html=re.sub(r'(<script src="[^"]+"></script>\s*)+', marker+'\n'+inline+'\n<!--/JS-->\n', html, count=1)
    open(page,'w').write(html)
    print(page, len(html)//1024, 'КБ')
