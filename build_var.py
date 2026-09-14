# -*- coding: utf-8 -*-
"""Страница «Варианты» — простое правило выбора для Марка."""
import json, html
TRI = json.load(open('/tmp/tri.json'))
PR = json.load(open('/tmp/pairs.json'))
BASE = open('/tmp/base.css').read()
def esc(s): return html.escape(s, quote=False)

CHOICE = [
 {"k":"физика","t":"Как работают машины и электричество",
  "q":"Интересно разобрать зарядку, понять, почему светит лампочка, что там внутри у двигателя.",
  "subj":"физика","n":41,"m":1070,
  "life":"Четыре года это будет выглядеть так: схемы, расчёты, лабораторные, много математики. "
         "Радиотехника, электроника, связь, энергетика. Работа — инженер на заводе, в связи, в энергетике.",
  "warn":"Если физика сейчас идёт через силу — учти, что в вузе её станет втрое больше, "
         "и «дотерпеть до диплома» на этом направлении почти никому не удаётся."},
 {"k":"биология","t":"Как устроено живое",
  "q":"Интересно, как работает организм, что происходит с едой, как устроены животные и растения.",
  "subj":"биология","n":32,"m":485,
  "life":"Четыре года: анатомия, микробиология, технология продуктов, практика на производстве "
         "и в хозяйствах. Ветеринарная экспертиза, пищевые технологии, аквакультура. "
         "Работа — на пищевом производстве, в лаборатории, в ветнадзоре.",
  "warn":"Учить придётся много и подряд: биология — это объём, а не сообразительность. "
         "Зато без формул."},
 {"k":"география","t":"Земля, растения, хозяйство",
  "q":"Интересно, где что растёт, как устроены леса и сады, почему хозяйство расположено именно так.",
  "subj":"география","n":11,"m":181,
  "life":"Четыре года: почвоведение, лесоводство, садоводство, много полевой практики. "
         "Лесное дело, садоводство, ландшафтная архитектура, аквакультура. "
         "Работа — в лесхозе, питомнике, хозяйстве, на природоохране.",
  "warn":"Выбор специальностей здесь самый узкий, и почти всё связано с землёй и селом. "
         "Если это не близко — лучше не брать."},
]

def rows(key):
    return "".join(
        f"<tr><td class='nm'><b>{esc(t['n'][:52])}</b><span>{esc(t['v'])}</span></td>"
        f"<td class='r'>{t['s']}</td><td class='r'>{t['p']}</td>"
        f"<td class='r'>{t['k'] if t['k'] else '—'}</td></tr>" for t in TRI[key])

cards = "".join(f"""
<section class="pick" id="p{i}">
  <div class="ptop">
    <div>
      <div class="kick">Если ближе это</div>
      <h2>{esc(c['t'])}</h2>
      <p class="qq">{esc(c['q'])}</p>
    </div>
    <div class="pnum"><b>{esc(c['subj'])}</b><span>{c['n']} программ · {c['m']} мест</span></div>
  </div>
  <p class="life"><b>Чем это будет на самом деле.</b> {esc(c['life'])}</p>
  <p class="warn">{esc(c['warn'])}</p>
  <div class="scroll"><table>
    <colgroup><col><col class="w1"><col class="w2"><col class="w3"></colgroup>
    <thead><tr><th>Куда проходит по 2026 году</th><th class="r">Проходной</th>
      <th class="r">Мест</th><th class="r">Конкурс</th></tr></thead>
    <tbody>{rows(c['k'])}</tbody></table></div>
</section>""" for i, c in enumerate(CHOICE, 1))

PAGE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Простое правило выбора предметов ЕГЭ для поступления на бюджет: что учить, чем страховаться и чем это обернётся на четыре года.">
<meta name="color-scheme" content="light dark">
<title>Что сдавать и куда это ведёт</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,500;0,700;1,500&family=PT+Sans:wght@400;700&display=swap">
<style>{BASE}
.tog{{display:inline-flex;gap:0;border:1px solid var(--line);border-radius:7px;overflow:hidden;flex-wrap:wrap}}
.tog .tb-l{{display:inline-block;padding:7px 13px;font-size:13.5px;color:var(--faint);
  text-decoration:none;border-left:1px solid var(--line)}}
.tog .tb-l:first-child{{border-left:none}}
.tog .tb-l:hover{{background:var(--sand);color:var(--ink)}}
.tog .tb-l.on{{background:var(--acc-soft);color:var(--ink);font-weight:700}}
.navbar{{margin:0 0 20px}}
.rule{{background:var(--acc-soft);border-radius:12px;padding:26px 28px;margin:22px 0 26px}}
.rule .kick{{color:var(--acc)}}
.rule h2{{font-size:26px;margin-top:9px;line-height:1.15}}
.formula{{margin-top:18px;display:grid;gap:10px}}
.formula div{{display:flex;gap:14px;align-items:baseline;font-size:16px}}
.formula em{{font-style:normal;flex:none;width:112px;font-size:11.5px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--faint);font-weight:700;padding-top:3px}}
.formula b{{color:var(--ink)}}
.rule p{{margin-top:16px;font-size:15px;max-width:62ch}}
.pick{{border-top:1px solid var(--line);padding-top:24px;margin-top:28px}}
.ptop{{display:flex;justify-content:space-between;gap:22px;flex-wrap:wrap;align-items:flex-start}}
.ptop h2{{font-size:25px;margin-top:6px}}
.qq{{margin-top:8px;font-size:15.5px;max-width:46ch}}
.pnum{{flex:none;text-align:right;padding-top:8px}}
.pnum b{{display:block;font-family:Vollkorn,serif;font-size:23px;color:var(--acc)}}
.pnum span{{display:block;font-size:12.5px;color:var(--faint);margin-top:4px;
  font-variant-numeric:tabular-nums}}
.life{{margin-top:16px;font-size:15px;max-width:66ch}}
.warn{{margin-top:11px;font-size:14.5px;color:var(--body);background:var(--sand);
  border-radius:8px;padding:12px 15px;max-width:66ch}}
.big{{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:22px 24px;
  margin:24px 0;box-shadow:var(--sh)}}
.big h2{{font-size:22px}}
.big h3{{font-size:16px;margin-top:18px}}
.big p{{margin-top:11px;font-size:15px;max-width:64ch}}
.steps{{counter-reset:s;display:grid;gap:13px;margin-top:16px;padding:0}}
.steps li{{list-style:none;position:relative;padding-left:38px;font-size:15px}}
.steps li::before{{counter-increment:s;content:counter(s);position:absolute;left:0;top:-1px;
  width:26px;height:26px;border-radius:50%;background:var(--acc-soft);color:var(--acc);
  font-weight:700;font-size:13px;display:grid;place-items:center}}
.steps b{{color:var(--ink)}}
details{{margin-top:14px;border-top:1px solid var(--line2);padding-top:14px}}
summary{{cursor:pointer;font-size:14.5px;color:var(--acc);font-weight:700}}
details table{{margin-top:12px}}
</style>
</head>
<body>
<div class="wrap">
<div class="tog navbar">
  <a class="tb-l" href="./">Тест</a>
  <a class="tb-l" href="vzvesit.html">Предметы ЕГЭ</a>
  <a class="tb-l" href="./?tab=att">Аттестат</a>
  <a class="tb-l" href="znakomstvo.html">Знакомство с ЕГЭ</a>
  <a class="tb-l on" href="varianty.html">Варианты</a>
</div>
<header style="border-bottom:1px solid var(--line);padding-bottom:20px">
  <div class="kick">Без длинных рассуждений</div>
  <h1 style="margin-top:10px">Что сдавать и куда это ведёт</h1>
  <p class="lede">Выбирать надо один раз и осенью. Ниже — правило, один вопрос к себе
  и честное описание того, чем каждый путь обернётся на четыре года вперёд.</p>
</header>

<div class="rule">
  <div class="kick">Правило</div>
  <h2>Русский и математика — всегда. Третий предмет — по интересу. Биология — для подстраховки.</h2>
  <div class="formula">
    <div><em>Обязательно</em><span><b>Русский язык</b> — его сдают все, выбора нет.</span></div>
    <div><em>Обязательно</em><span><b>Профильная математика</b> — открывает больше половины
      бюджетных программ. Без неё выбор сжимается в четыре раза.</span></div>
    <div><em>По интересу</em><span><b>Один предмет из трёх</b> — физика, биология или география.
      Тот, в котором не противно разбираться.</span></div>
    <div><em>Страховка</em><span><b>Биология до минимального порога</b> — 34 часа, час в неделю.
      Если интерес и так биология — страховка не нужна.</span></div>
  </div>
  <p>Всё. Больше решать нечего. Остальное на этой странице — объяснение, почему именно так.</p>
</div>

<div class="big">
  <h2>Один вопрос, который решает всё</h2>
  <p>Не «что легче» — легче не будет нигде. И не «где больше мест» — места есть везде.
  Вопрос один: <b>в чём не противно разбираться четыре года?</b></p>
  <p>Потому что предмет ЕГЭ — это не экзамен на три часа. Это специальность, а потом работа.
  Сдать физику и поступить на радиотехнику — значит четыре года решать задачи и считать схемы.
  Если физика сейчас идёт через силу, в вузе её станет втрое больше, и бросить на втором курсе
  будет дороже, чем выбрать другое сейчас.</p>
  <p>Ниже три ответа на этот вопрос. Прежде чем читать — зайди в
  <a href="znakomstvo.html">«Знакомство с ЕГЭ»</a> и полистай настоящие задания физики,
  биологии и географии. Полчаса. Это честнее любых рассуждений.</p>
</div>

{cards}

<div class="big">
  <h2>Зачем биология «для подстраховки»</h2>
  <p>Набор из трёх экзаменов хрупкий: русский, математика и физика открывают 41 программу,
  но если провалить <b>любой</b> из двух профильных — остаётся ровно ноль. Все 41 требуют оба.</p>
  <p>Биология до минимального порога стоит <b>34 часа</b> — час в неделю с сентября по май.
  Это не второй профильный предмет, это подушка. И вот что она меняет:</p>
  <div class="scroll"><table>
    <colgroup><col><col class="w2"><col class="w3"></colgroup>
    <thead><tr><th>Как сложится</th><th class="r">Программ</th><th class="r">Мест</th></tr></thead>
    <tbody>
      <tr><td class="nm"><b>Всё сдал</b></td><td class="r">65</td><td class="r">1424</td></tr>
      <tr><td class="nm"><b>Провалил биологию</b><span>ничего не потерял</span></td>
        <td class="r">41</td><td class="r">1070</td></tr>
      <tr><td class="nm"><b>Провалил физику</b><span>биология вытягивает</span></td>
        <td class="r">32</td><td class="r">485</td></tr>
      <tr><td class="nm"><b>Провалил математику</b><span>остаётся хоть что-то</span></td>
        <td class="r">13</td><td class="r">179</td></tr>
    </tbody></table></div>
  <p><b>И даже совсем слабый расклад проходит.</b> Русский 50, математика 39, биология 39 —
  это сумма 128, и она берёт ветеринарно-санитарную экспертизу АГТУ (проходной 125,
  конкурс 4,0) и пищевые технологии ВолГАУ (126). Пороги — уже бюджет.</p>
  <details>
    <summary>Почему именно биология, а не другой предмет</summary>
    <div class="scroll"><table>
      <colgroup><col><col class="w2"><col class="w3"></colgroup>
      <thead><tr><th>Добавить к математике и физике</th><th class="r">Программ</th>
        <th class="r">Цена, часов</th></tr></thead>
      <tbody>
        <tr><td class="nm"><b>Биология</b></td><td class="r">+24</td><td class="r">34</td></tr>
        <tr><td class="nm">Химия</td><td class="r">+6</td><td class="r">84</td></tr>
        <tr><td class="nm">География</td><td class="r">+2</td><td class="r">38</td></tr>
        <tr><td class="nm">Обществознание</td><td class="r">+2</td><td class="r">69</td></tr>
        <tr><td class="nm">Информатика</td><td class="r">0</td><td class="r">49</td></tr>
      </tbody></table></div>
    <p style="font-size:14px">Информатика даёт ноль: везде, где её принимают, уже принимают
    физику. География и обществознание — почти ноль. Химия вдвое дороже биологии
    и вчетверо бесполезнее.</p>
  </details>
</div>

<div class="big">
  <h2>А если поступлю и пойму, что не моё</h2>
  <p>Это бывает чаще, чем кажется, и об этом честнее знать заранее.</p>
  <p><b>Как снизить риск сейчас.</b> Посмотреть не только задания ЕГЭ, но и то, чем занимаются
  на самом направлении: найти учебный план на сайте вуза и прочитать список предметов
  первых двух курсов. Если половина названий вызывает тоску — это ответ.</p>
  <p><b>Что можно сделать потом.</b> Перевестись внутри вуза на другое направление — обычно
  после первого курса и при наличии мест, с досдачей разницы. Перевестись в другой вуз —
  сложнее, но возможно. Уйти и поступить заново — потеря года, но не катастрофа.
  Самое плохое — тянуть четыре года через силу и получить диплом, по которому не пойдёшь работать.</p>
  <p><b>И трезвая мысль.</b> Первое образование редко оказывается единственным. Бюджетное место
  в региональном вузе — это не приговор на всю жизнь, а способ спокойно прожить четыре года,
  получить корочку и понять, чего хочется. Выбирать надо так, чтобы эти четыре года
  не были мучением, а не так, чтобы угадать профессию мечты.</p>
</div>

<div class="big">
  <h2>Что делать дальше</h2>
  <ul class="steps">
    <li><b>Полистать настоящие задания.</b> <a href="znakomstvo.html">Знакомство с ЕГЭ</a>,
    три предмета, полчаса.</li>
    <li><b>Выбрать один профильный</b> — тот, где хочется понять, как устроено.</li>
    <li><b>Начать с русского и математики</b> прямо сейчас: они нужны в любом варианте,
    и они самые долгие.</li>
    <li><b>С октября добавить биологию</b> по часу в неделю, если профильный не она.</li>
    <li><b>Не менять решение после Нового года.</b> Из восьми месяцев три уже уйдут.</li>
  </ul>
</div>

<footer class="foot">Проходные баллы, конкурс и число мест — из приказов о зачислении 2026 года
по вузам Волгограда, Волжского и Астрахани. Часы — из разбора демоверсий ФИПИ 2027
по той же методике, что на странице «Предметы ЕГЭ». Цифры 2027 года изменятся: контрольные
цифры приёма распределяют осенью 2026, но набор направлений и порядок величин обычно
сохраняются. Информатика, химия и обществознание из рассмотрения исключены.</footer>
</div>
</body>
</html>"""
open('varianty.html','w').write(PAGE)
print('varianty.html', len(PAGE)//1024, 'КБ')
