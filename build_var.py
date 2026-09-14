# -*- coding: utf-8 -*-
"""Страница «Варианты»: правило, три пути с рисками, страховки и тест."""
import json, html
TRI = json.load(open('/tmp/tri.json'))
INS = json.load(open('/tmp/insurance.json'))
QUIZ = open('/tmp/quiz.js').read()
BASE = open('/tmp/base.css').read()
def esc(s): return html.escape(s, quote=False)

CHOICE = [
 {"k":"физика","t":"Как работают машины и электричество","label":"Математика + физика",
  "q":"Интересно разобрать зарядку, понять, почему светит лампочка и что внутри у двигателя.",
  "n":41,"m":1070,"h":185,
  "life":"Четыре года это будет так: матанализ, линейная алгебра, общая физика, теоретическая "
         "механика, лабораторные и расчёты. Радиотехника, электроника, связь, энергетика. "
         "Работа — инженер на заводе, в связи, в энергетике.",
  "risks":[
    ["Риск не доучиться — главный","На первом курсе идёт высшая математика и физика того уровня, "
     "на который школьная тройка не натягивается. Человек, еле перешедший порог по профильной "
     "математике, на матанализе отстаёт с первых недель. Поступить сюда проще, чем доучиться."],
    ["Низкий проходной — это сигнал","124 балла на Радиоэлектронных системах и 82 зачисленных "
     "на 70 мест означают не щедрость, а то, что вуз добирает первый курс с запасом, "
     "зная про отсев."],
    ["Физика стоит на математике","Если математика идёт тяжело, месяцы уйдут не на физику, "
     "а на добор алгебры. Это называют главной причиной провала все репетиторы."],
    ["Треть не дотягивает до 60","Среди тех, кто сам выбрал физику, 36,4% остались "
     "ниже 60 баллов. Для порога этого хватает, для запаса — нет."]]},
 {"k":"биология","t":"Как устроено живое","label":"Математика + биология",
  "q":"Интересно, как работает организм, что происходит с едой, как устроены животные и растения.",
  "n":32,"m":485,"h":171,
  "life":"Четыре года: анатомия, микробиология, химия на прикладном уровне, технология продуктов, "
         "практика на производстве и в хозяйствах. Ветеринарная экспертиза, пищевые технологии, "
         "аквакультура. Работа — на пищевом производстве, в лаборатории, в ветнадзоре.",
  "risks":[
    ["Профильная математика всё равно нужна","От неё здесь не уйти — она в списке обязательных "
     "на всех этих программах. Разница в том, что в вузе математики будет один семестр, "
     "а не два года."],
    ["Биология — это объём","Не сообразительность, а количество: учить придётся много и подряд. "
     "У неё худшая статистика по стране — средний балл 54,5 и 16% не берут порог."],
    ["Мест вдвое меньше","485 против 1070, и наборы по 10–30 человек на программу, "
     "а не по 45–70. Ошибка в приоритетах стоит дороже."],
    ["Направления прикладные","Это работа на производстве и в хозяйствах, часто в районах. "
     "Если хочется в город и в офис — стоит посмотреть, кем реально работают выпускники."]]},
 {"k":"география","t":"Земля, растения, хозяйство","label":"Биология + география",
  "q":"Интересно, где что растёт, как устроены леса и сады, почему хозяйство расположено именно так.",
  "n":11,"m":181,"h":160,
  "life":"Четыре года: почвоведение, ботаника, лесоводство, садоводство, много полевой практики. "
         "Лесное дело, садоводство, ландшафтная архитектура, аквакультура. "
         "Работа — в лесхозе, питомнике, хозяйстве, на природоохране.",
  "risks":[
    ["Выбор самый узкий","11 программ и 181 место, и почти всё связано с землёй и селом. "
     "Это не запасной вариант «на всякий случай» — это сознательное решение работать с растениями "
     "и природой."],
    ["На 60 баллов нужно почти всё","По географии порог для 60 — 30 первичных из 38, "
     "то есть 25 заданий из 29. Учить придётся весь курс, хоть и лёгкими кусками."],
    ["Конкурс не маленький","У Садоводства 12,4 человека на место при 14 местах. "
     "Малое число мест делает конкурс чувствительным: пара сильных абитуриентов меняет картину."],
    ["Без профильной математики путь назад закрыт","Если в мае окажется, что хочется "
     "на техническое — вернуться уже нельзя. Математику надо решать осенью."]]},
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
      <div class="kick">Путь {i}</div>
      <h2>{esc(c['t'])}</h2>
      <p class="qq">{esc(c['q'])}</p>
    </div>
    <div class="pnum"><b>{esc(c['label'])}</b>
      <span>{c['n']} программ · {c['m']} мест</span>
      <span>{c['h']} часов до порогов</span></div>
  </div>
  <p class="life"><b>Чем это будет на самом деле.</b> {esc(c['life'])}</p>
  <div class="risks"><h3>Риски именно этого пути</h3>
    {''.join(f'<div class="risk"><b>{esc(t)}</b><span>{esc(d)}</span></div>' for t, d in c['risks'])}
  </div>
  <div class="scroll"><table>
    <colgroup><col><col class="w1"><col class="w2"><col class="w3"></colgroup>
    <thead><tr><th>Куда проходит по 2026 году</th><th class="r">Проходной</th>
      <th class="r">Мест</th><th class="r">Конкурс</th></tr></thead>
    <tbody>{rows(c['k'])}</tbody></table></div>
</section>""" for i, c in enumerate(CHOICE, 1))

ins = "".join(f"""<div class="ins">
  <b>{esc(x['t'])}</b>
  <p>{esc(x['d'])}</p>
  <p class="but"><span>Подвох:</span> {esc(x['w'])}
  {f' <a href="{x["u"]}">источник</a>' if x['u'] else ''}</p>
</div>""" for x in INS)

PAGE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Три пути на бюджет: что учить, чем рискуешь, чем подстраховаться. С тестом в конце.">
<meta name="color-scheme" content="light dark">
<title>Что сдавать и чем рискуешь</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,500;0,700;1,500&family=PT+Sans:wght@400;700&display=swap">
<style>{BASE}
.tog{{display:inline-flex;gap:0;border:1px solid var(--line);border-radius:7px;overflow:hidden;flex-wrap:wrap}}
.tog .tb-l{{display:inline-block;padding:7px 13px;font-size:13.5px;color:var(--faint);
  text-decoration:none;border-left:1px solid var(--line)}}
.tog .tb-l:first-child{{border-left:none}}
.tog .tb-l:hover{{background:var(--sand);color:var(--ink)}}
.tog .tb-l.on{{background:var(--acc-soft);color:var(--ink);font-weight:700}}
.navbar{{margin:0 0 20px}}
.rule{{background:var(--acc-soft);border-radius:12px;padding:24px 26px;margin:20px 0 24px}}
.rule .kick{{color:var(--acc)}}
.rule h2{{font-size:24px;margin-top:8px;line-height:1.18}}
.formula{{margin-top:16px;display:grid;gap:9px}}
.formula div{{display:flex;gap:14px;align-items:baseline;font-size:15.5px}}
.formula em{{font-style:normal;flex:none;width:104px;font-size:11px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--faint);font-weight:700;padding-top:3px}}
.formula b{{color:var(--ink)}}
.pick{{border-top:1px solid var(--line);padding-top:24px;margin-top:30px}}
.ptop{{display:flex;justify-content:space-between;gap:22px;flex-wrap:wrap;align-items:flex-start}}
.ptop h2{{font-size:25px;margin-top:6px}}
.qq{{margin-top:8px;font-size:15.5px;max-width:44ch}}
.pnum{{flex:none;text-align:right;padding-top:8px}}
.pnum b{{display:block;font-family:Vollkorn,serif;font-size:19px;color:var(--acc)}}
.pnum span{{display:block;font-size:12.5px;color:var(--faint);margin-top:4px;
  font-variant-numeric:tabular-nums}}
.life{{margin-top:16px;font-size:15px;max-width:66ch}}
.risks{{margin-top:18px;background:var(--sand);border-radius:10px;padding:18px 20px}}
.risks h3{{font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--bad);
  font-family:"PT Sans",sans-serif}}
.risk{{margin-top:12px}}
.risk b{{display:block;color:var(--ink);font-size:15px}}
.risk span{{display:block;font-size:14px;margin-top:3px;max-width:64ch}}
.big{{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:22px 24px;
  margin:26px 0;box-shadow:var(--sh)}}
.big h2{{font-size:22px}}
.big p{{margin-top:11px;font-size:15px;max-width:64ch}}
.insw{{display:grid;gap:14px;margin-top:18px}}
.ins{{border-top:1px solid var(--line2);padding-top:14px}}
.ins b{{color:var(--ink);font-size:16px;font-family:Vollkorn,Georgia,serif}}
.ins p{{margin-top:6px;font-size:14.5px;max-width:66ch}}
.ins .but{{color:var(--faint);font-size:13.5px}}
.ins .but span{{color:var(--bad);font-weight:700}}
.ins .but a{{color:var(--faint)}}
.steps{{counter-reset:s;display:grid;gap:13px;margin-top:16px;padding:0}}
.steps li{{list-style:none;position:relative;padding-left:38px;font-size:15px}}
.steps li::before{{counter-increment:s;content:counter(s);position:absolute;left:0;top:-1px;
  width:26px;height:26px;border-radius:50%;background:var(--acc-soft);color:var(--acc);
  font-weight:700;font-size:13px;display:grid;place-items:center}}
.steps b{{color:var(--ink)}}
/* тест */
#quiz{{background:var(--card);border:2px solid var(--acc);border-radius:12px;padding:24px 26px;
  margin:26px 0}}
.qstep{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);
  font-weight:700}}
.qtitle{{font-family:Vollkorn,Georgia,serif;font-size:23px;color:var(--ink);margin-top:8px;
  line-height:1.2}}
.qopts{{display:grid;gap:9px;margin-top:18px}}
.qopt{{text-align:left;background:transparent;border:1px solid var(--line);border-radius:8px;
  padding:13px 16px;font-size:15px;color:var(--ink);transition:.12s}}
.qopt:hover{{border-color:var(--acc);background:var(--acc-soft)}}
.qres h3{{font-family:Vollkorn,Georgia,serif;font-size:26px;color:var(--ink);margin-top:8px}}
.qset{{margin-top:8px;font-size:16px;color:var(--acc);font-weight:700}}
.qn{{margin-top:4px;font-size:13.5px;color:var(--faint);font-variant-numeric:tabular-nums}}
.qres p{{margin-top:10px;font-size:15px}}
.qrisk{{background:var(--sand);border-radius:8px;padding:12px 15px;font-size:14.5px}}
.qalt{{margin-top:16px;padding-top:14px;border-top:1px solid var(--line2);font-size:14.5px}}
.qfoot{{margin-top:16px;font-size:14px;color:var(--faint)}}
.qfoot a{{color:var(--acc)}}
.qagain{{margin-top:16px;background:transparent;border:1px solid var(--line);border-radius:7px;
  padding:9px 16px;font-size:14px;color:var(--faint)}}
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
  <div class="kick">Всё, что нужно для решения</div>
  <h1 style="margin-top:10px">Что сдавать и чем рискуешь</h1>
  <p class="lede">Три пути на бюджет. У каждого написано, что учить, сколько это часов,
  куда реально проходят, чем это обернётся на четыре года и что может пойти не так.
  В конце — тест, который поможет свести всё это к одному ответу.</p>
</header>

<div class="rule">
  <div class="kick">Правило</div>
  <h2>Русский и математика — всегда. Третий предмет — по интересу. Биология — для подстраховки.</h2>
  <div class="formula">
    <div><em>Обязательно</em><span><b>Русский язык</b> — сдают все.</span></div>
    <div><em>Обязательно</em><span><b>Профильная математика</b> — открывает больше половины
      бюджетных программ. Без неё выбор сжимается вчетверо.</span></div>
    <div><em>По интересу</em><span><b>Один предмет из трёх</b> — физика, биология или география.</span></div>
    <div><em>Страховка</em><span><b>Биология до порога</b> — 34 часа, час в неделю.
      Если основной предмет и так биология, страховка не нужна.</span></div>
  </div>
</div>

<div class="big">
  <h2>Один вопрос, который решает всё</h2>
  <p>Не «что легче» — легче не будет нигде. И не «где больше мест» — места есть везде.
  Вопрос один: <b>в чём не противно разбираться четыре года?</b></p>
  <p>Предмет ЕГЭ — это не экзамен на три часа, а специальность и потом работа. Сдать физику
  и поступить на радиотехнику — значит четыре года решать задачи и считать схемы. Если физика
  сейчас идёт через силу, в вузе её станет втрое больше. Вылететь на втором курсе дороже,
  чем выбрать другое сейчас.</p>
  <p>Прежде чем читать дальше — зайди в <a href="znakomstvo.html">«Знакомство с ЕГЭ»</a>
  и полистай настоящие задания физики, биологии и географии. Полчаса.</p>
</div>

{cards}

<div class="big">
  <h2>Зачем биология «для подстраховки»</h2>
  <p>Набор из трёх экзаменов хрупкий: русский, математика и физика открывают 41 программу,
  но если провалить <b>любой</b> из двух профильных — остаётся ровно ноль. Все 41 требуют оба.</p>
  <p>Биология до порога стоит <b>34 часа</b> — час в неделю с сентября по май. Это не второй
  профильный предмет, это подушка.</p>
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
  <p><b>Даже совсем слабый расклад проходит.</b> Русский 50, математика 39, биология 39 —
  сумма 128, и она берёт ветеринарно-санитарную экспертизу АГТУ (проходной 125, конкурс 4,0)
  и пищевые технологии ВолГАУ (126). Пороги — уже бюджет.</p>
  <p><b>Почему именно биология.</b> Из всех добавок к математике с физикой она даёт больше всего:
  +24 программы за 34 часа. Химия — +6 за 84 часа. География и обществознание — по +2.
  Информатика — ровно ноль, потому что везде, где её принимают, уже принимают физику.</p>
</div>

<div class="big">
  <h2>Девять страховок</h2>
  <p>Способы, которые повышают шанс на бюджет помимо самих баллов. У каждого есть подвох —
  он написан рядом.</p>
  <div class="insw">{ins}</div>
</div>

<div class="big">
  <h2>А если поступлю и пойму, что не моё</h2>
  <p><b>Как снизить риск сейчас.</b> Посмотреть не только задания ЕГЭ, но и учебный план
  направления на сайте вуза — список предметов первых двух курсов. Если половина названий
  вызывает тоску, это ответ.</p>
  <p><b>Что можно сделать потом.</b> Перевестись внутри вуза на другое направление — обычно
  после первого курса и при наличии мест, с досдачей разницы. Перевестись в другой вуз —
  сложнее, но возможно. Уйти и поступить заново — потеря года, но не катастрофа. Самое плохое —
  тянуть четыре года через силу и получить диплом, по которому не пойдёшь работать.</p>
  <p><b>И трезвая мысль.</b> Первое образование редко оказывается единственным. Бюджетное место
  в региональном вузе — способ спокойно прожить четыре года, получить корочку и понять,
  чего хочется. Выбирать надо так, чтобы эти четыре года не были мучением, а не так,
  чтобы угадать профессию мечты.</p>
</div>

<h2 style="margin-top:34px;font-size:24px">Свести всё к одному ответу</h2>
<p style="margin-top:10px;font-size:15px;max-width:62ch">Семь вопросов. Тест учитывает интерес,
базу по математике, готовность к нагрузке и к тому, где придётся учиться.</p>
<div id="quiz"></div>

<div class="big">
  <h2>Что делать дальше</h2>
  <ul class="steps">
    <li><b>Полистать настоящие задания.</b> <a href="znakomstvo.html">Знакомство с ЕГЭ</a>,
    три предмета, полчаса.</li>
    <li><b>Выбрать один профильный</b> — тот, где хочется понять, как устроено.</li>
    <li><b>Начать с русского и математики</b> прямо сейчас: они нужны в любом варианте
    и они самые долгие.</li>
    <li><b>С октября добавить биологию</b> по часу в неделю, если профильный не она.</li>
    <li><b>Не менять решение после Нового года.</b> Из восьми месяцев три уже уйдут.</li>
  </ul>
</div>

<footer class="foot">Проходные баллы, конкурс и число мест — из приказов о зачислении 2026 года
по вузам Волгограда, Волжского и Астрахани. Часы — из разбора демоверсий ФИПИ 2027 по той же
методике, что на странице «Предметы ЕГЭ». Правила приёма и пересдачи — по приказам Рособрнадзора
и Минобрнауки, ссылки в блоке страховок. Цифры 2027 года изменятся: контрольные цифры приёма
распределяют осенью 2026, но набор направлений и порядок величин обычно сохраняются.
Информатика, химия и обществознание из рассмотрения исключены.</footer>
</div>
<script>
{QUIZ}
</script>
</body>
</html>"""
open('varianty.html','w').write(PAGE)
print('varianty.html', len(PAGE)//1024, 'КБ')
