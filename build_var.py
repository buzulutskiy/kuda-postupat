# -*- coding: utf-8 -*-
"""Страница «Варианты» — три реальные дороги Марка на бюджет."""
import json, html
R = json.load(open('/tmp/r3.json'))
T = json.load(open('/tmp/r3_text.json'))
BASE = open('/tmp/base.css').read()
ORDER = ["математика + физика", "математика + биология", "биология + география"]
def esc(s): return html.escape(s, quote=False)

def rows(d):
    out = []
    for t in d['top']:
        out.append(f"<tr><td class='nm'><b>{esc(t['n'][:52])}</b><span>{esc(t['v'])}</span></td>"
                   f"<td class='r'>{t['s']}</td><td class='r'>{t['p']}</td>"
                   f"<td class='r'>{t['k'] if t['k'] else '—'}</td></tr>")
    return "".join(out)

cards = []
for i, k in enumerate(ORDER, 1):
    d, t = R[k], T[k]
    cards.append(f"""
<section class="route" id="r{i}">
  <div class="rhead">
    <div>
      <div class="kick">Вариант {i}</div>
      <h2>{esc(t['name'])}</h2>
      <p class="verdict">{esc(t['verdict'])}</p>
      <p class="who">{esc(t['who'])}</p>
    </div>
    <div class="rnum">
      <div><b>{d['n']}</b><span>программ</span></div>
      <div><b>{d['places']}</b><span>мест</span></div>
    </div>
  </div>
  <div class="cols">
    <div class="pro"><h3>Что хорошего</h3><ul>{''.join(f'<li>{esc(x)}</li>' for x in t['plus'])}</ul></div>
    <div class="con"><h3>Чем платишь</h3><ul>{''.join(f'<li>{esc(x)}</li>' for x in t['minus'])}</ul></div>
  </div>
  <div class="hrs">Часов до порога по трём предметам вместе — <b>{sum(d['hp'].values())}</b>.
    Если целиться на 50 баллов по каждому — {sum(d['h50'].values())}.
    Дешёвых программ (проходной до 145): <b>{d['ncheap']}</b> на {d['pcheap']} мест.</div>
  <div class="scroll"><table>
    <colgroup><col><col class="w1"><col class="w2"><col class="w3"></colgroup>
    <thead><tr><th>Куда проходит по 2026 году</th><th class="r">Проходной</th>
      <th class="r">Мест</th><th class="r">Конкурс</th></tr></thead>
    <tbody>{rows(d)}</tbody></table></div>
  <p class="try">Проверить на себе: <a href="znakomstvo.html">открой настоящие задания</a>
    и посмотри {esc(t['check'])} — не «кажется ли проще», а хочется ли разбираться.</p>
</section>""")

PAGE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Три реальных набора предметов ЕГЭ для поступления на бюджет: что каждый открывает и чем за него платишь.">
<meta name="color-scheme" content="light dark">
<title>Три дороги на бюджет</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,500;0,700;1,500&family=PT+Sans:wght@400;700&display=swap">
<style>{BASE}
.tog{{display:inline-flex;gap:0;border:1px solid var(--line);border-radius:7px;overflow:hidden;flex-wrap:wrap}}
.tog .tb-l{{display:inline-block;padding:7px 13px;font-size:13.5px;color:var(--faint);
  text-decoration:none;border-left:1px solid var(--line)}}
.tog .tb-l:first-child{{border-left:none}}
.tog .tb-l:hover{{background:var(--sand);color:var(--ink)}}
.tog .tb-l.on{{background:var(--acc-soft);color:var(--ink);font-weight:700}}
.navbar{{margin:0 0 20px}}
.short{{display:grid;gap:0;margin:20px 0 8px;border:1px solid var(--line);border-radius:11px;
  overflow:hidden;background:var(--card)}}
.short a{{display:grid;grid-template-columns:1fr auto;gap:14px;align-items:baseline;
  padding:16px 20px;border-top:1px solid var(--line2);text-decoration:none;color:inherit}}
.short a:first-child{{border-top:none}}
.short a:hover{{background:var(--sand)}}
.short b{{font-family:Vollkorn,Georgia,serif;font-size:20px;color:var(--ink);display:block}}
.short span{{font-size:14px;color:var(--body);display:block;margin-top:3px}}
.short i{{font-style:normal;font-size:13px;color:var(--faint);white-space:nowrap;
  font-variant-numeric:tabular-nums}}
.route{{border-top:1px solid var(--line);padding-top:26px;margin-top:32px}}
.rhead{{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:flex-start}}
.rhead h2{{font-size:27px;margin-top:6px}}
.verdict{{margin-top:8px;font-size:16px;color:var(--acc);font-weight:700}}
.who{{margin-top:7px;font-size:15px;max-width:46ch}}
.rnum{{display:flex;gap:22px;flex:none;padding-top:6px}}
.rnum div{{text-align:right}}
.rnum b{{display:block;font-family:Vollkorn,serif;font-size:27px;color:var(--ink);line-height:1;
  font-variant-numeric:tabular-nums}}
.rnum span{{display:block;font-size:11px;color:var(--faint);margin-top:4px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:20px}}
@media (max-width:640px){{.cols{{grid-template-columns:1fr;gap:16px}}.rnum{{gap:16px}}}}
.cols h3{{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);
  font-family:"PT Sans",sans-serif}}
.cols ul{{margin:9px 0 0;padding-left:19px;display:grid;gap:6px;font-size:14.5px}}
.pro li::marker{{color:var(--ok)}}
.con li::marker{{color:var(--bad)}}
.hrs{{margin-top:18px;background:var(--sand);border-radius:8px;padding:12px 15px;font-size:14px}}
.try{{margin-top:14px;font-size:14px;color:var(--faint)}}
.try a{{color:var(--acc)}}
.big{{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:22px 24px;
  margin:22px 0;box-shadow:var(--sh)}}
.big h2{{font-size:22px}}
.big h3{{font-size:16px;margin-top:20px}}
.big p{{margin-top:11px;font-size:15px;max-width:64ch}}
.fact{{display:flex;gap:16px;align-items:baseline;margin-top:14px;padding-top:13px;
  border-top:1px solid var(--line2)}}
.fact b{{font-family:Vollkorn,serif;font-size:30px;color:var(--ink);flex:none;line-height:1;
  font-variant-numeric:tabular-nums;min-width:92px}}
.fact span{{font-size:14.5px}}
.fact span i{{font-style:normal;display:block;font-size:12.5px;color:var(--faint);margin-top:4px}}
.fact span i a{{color:var(--faint)}}
.steps{{counter-reset:s;display:grid;gap:13px;margin-top:16px;padding:0}}
.steps li{{list-style:none;position:relative;padding-left:38px;font-size:15px}}
.steps li::before{{counter-increment:s;content:counter(s);position:absolute;left:0;top:-1px;
  width:26px;height:26px;border-radius:50%;background:var(--acc-soft);color:var(--acc);
  font-weight:700;font-size:13px;display:grid;place-items:center}}
.steps b{{color:var(--ink)}}
tr.dim{{opacity:.55}}
td .yes{{color:var(--ok);font-weight:700}}
td .no{{color:var(--bad)}}
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
<header style="border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:6px">
  <div class="kick">Решать тебе</div>
  <h1 style="margin-top:10px">Три дороги на бюджет</h1>
  <p class="lede">Задача: поступить на бюджет, всё равно куда. Времени — до июня 2027,
  база почти с нуля. Русский обязателен у всех, дальше два предмета на выбор.
  Реальных вариантов три.</p>
</header>

<div class="short">
  <a href="#r1"><span><b>Математика и физика</b>
    <span>Больше всего мест, но самый высокий риск не дотянуть</span></span>
    <i>41 программа · 1070 мест</i></a>
  <a href="#r2"><span><b>Математика и биология</b>
    <span>Почти та же широта, но без физики</span></span>
    <i>32 программы · 485 мест</i></a>
  <a href="#r3"><span><b>Биология и география</b>
    <span>Самый спокойный по учёбе и самый узкий по выбору</span></span>
    <i>11 программ · 181 место</i></a>
</div>
<p class="src" style="font-size:13px;color:var(--faint);margin-bottom:26px">Информатика, химия
и обществознание из рассмотрения убраны. Остальные предметы — русский, математика, физика,
биология, география.</p>

<div class="big">
  <h2>Главное, что надо понять про цель</h2>
  <p><b>Шестьдесят баллов не нужны.</b> Проходные на этих направлениях — 124–142. Сумма
  минимальных порогов по трём предметам — около 120. То есть задача не «сдать хорошо»,
  а <b>уверенно перейти пороги по двум предметам и вытянуть русский чуть выше среднего</b>.
  Это принципиально другая по сложности задача, и она реальна.</p>
  <p><b>Развилка — профильная математика.</b> Из 75 бюджетных программ с проходным до 170
  она нужна на 40. Первые два варианта её требуют, третий — нет. Всё остальное второстепенно.</p>
</div>

<div class="big">
  <h2>Что говорит опыт тех, кто уже прошёл через это</h2>
  <p>Я собрал отзывы выпускников, слова учителей и официальную статистику. Если свести всё
  вместе, картина получается такая.</p>

  <div class="fact"><b>2–16%</b><span>не берут даже минимальный порог: по физике 2,1%,
    по биологии 16%. То есть <b>провалить экзамен целиком — редкий исход</b>. Ошибаются
    почти никогда не в этом.
    <i><a href="https://ege.lancmanschool.ru/poleznyie-stati/itogi-ege-po-biologii-2024-goda/">Итоги ЕГЭ по биологии</a>,
    <a href="https://irorb.ru/wp-content/uploads/2026/04/metodicheskie-rekomendaczii-po-podgotovke-k-gia-po-fizike-v-2025-%E2%80%93-2026-uchebnom-godu-na-osnove-analiza-ege-2026.pdf">анализ ЕГЭ по физике, 2025</a></i></span></div>

  <div class="fact"><b>36,4%</b><span>тех, кто <b>сам выбрал</b> физику, не дотянули до 60 баллов.
    Каждый третий из мотивированных. Вот здесь и ошибаются: не в том, сдадут ли,
    а в том, на сколько.
    <i><a href="https://irorb.ru/wp-content/uploads/2026/04/metodicheskie-rekomendaczii-po-podgotovke-k-gia-po-fizike-v-2025-%E2%80%93-2026-uchebnom-godu-na-osnove-analiza-ege-2026.pdf">Методический анализ ЕГЭ по физике, 2025</a></i></span></div>

  <div class="fact"><b>54,5</b><span>средний балл по биологии — <b>ниже, чем у физики</b> (61,7)
    и ниже географии (54,8). «Лёгкость» предмета не превращается в баллы: там, где меньше
    формул, больше объёма и строже проверка развёрнутых ответов.
    <i><a href="https://4ege.ru/novosti-ege/75487-srednie-bally-ege-2025.html">Средние баллы ЕГЭ-2025</a></i></span></div>

  <div class="fact"><b>0</b><span>найденных историй «сам, с нуля, за год, на 60+».
    Ни одной. У всех успехов есть либо скрытая база (74 балла за три месяца),
    либо репетитор или курс (86 баллов через онлайн-школу). Это самый честный вывод
    из всей подборки.
    <i><a href="https://otvet.mail.ru/question/231140003">Ответы Mail.ru</a>,
    <a href="https://www.woman.ru/kids/nursery/thread/5914189/">Woman.ru</a></i></span></div>

  <h3>Как выглядят провалы</h3>
  <p>У них общий рисунок, и он не про способности. <b>Юлия</b> взяла «понятные» предметы,
  готовилась сама — не набрала минимум по обоим, ушла в колледж на платное.
  <b>Маша</b> занималась два года с репетиторами, потратила больше 200 тысяч — биология 43,
  не хватило девяти баллов. <b>Парень за три недели до экзамена</b>: пробник по математике 27,
  по физике 39 — один и тот же пробел вылез дважды. Общее у всех трёх: поздний старт
  или отсутствие внешнего контроля, а у первой ещё и выбор предмета «по лёгкости».</p>

  <h3>И поправка на кривое зеркало</h3>
  <p>Истории успеха публикуют репетиторы и онлайн-курсы — им это выгодно. Истории провалов
  живут в закрытых пабликах и в поиск не попадают. Поэтому видимое соотношение
  «получилось / не получилось» завышено в пользу успеха, и опираться надо на официальную
  статистику, а не на рассказы. А статистика говорит прямо: <b>треть мотивированных
  не добирает до 60</b>.</p>

  <h3>Что из этого следует</h3>
  <p>Порог Марк возьмёт почти наверняка. Шестьдесят по физике с нуля самостоятельно —
  не базовый сценарий. Но поскольку цель — перейти пороги, а не набрать 60, <b>расчёт сходится
  даже по пессимистичному сценарию</b>. Главное — начать осенью и не менять предмет в январе.</p>
</div>

{''.join(cards)}

<div class="big">
  <h2>Все сочетания, которые вообще возможны</h2>
  <p>Из четырёх предметов — математика, физика, биология, география — получается шесть пар.
  Вот они все, чтобы не казалось, что я что-то спрятал.</p>
  <div class='scroll'><table><colgroup><col><col class='w1'><col class='w2'><col class='w3'><col class='w4'></colgroup><thead><tr><th>Набор (плюс русский)</th><th class='r'>Программ</th><th class='r'>Мест</th><th class='r'>Дешёвых<span class='cell-sub'>до 145 баллов</span></th><th class='r'>Часов<span class='cell-sub'>до порогов</span></th></tr></thead><tbody><tr><td class='nm'><b>Математика + физика</b><span><span class="yes">рабочий</span></span></td><td class='r'>41</td><td class='r'>1070</td><td class='r'>10</td><td class='r'>185</td></tr><tr><td class='nm'><b>Математика + биология</b><span><span class="yes">рабочий</span></span></td><td class='r'>32</td><td class='r'>485</td><td class='r'>13</td><td class='r'>171</td></tr><tr><td class='nm'><b>Физика + биология</b><span><span class="yes">рабочий</span></span></td><td class='r'>13</td><td class='r'>179</td><td class='r'>7</td><td class='r'>170</td></tr><tr><td class='nm'><b>Биология + география</b><span><span class="yes">рабочий</span></span></td><td class='r'>11</td><td class='r'>181</td><td class='r'>5</td><td class='r'>160</td></tr><tr class=dim><td class='nm'><b>Математика + география</b><span><span class="no">не рассматриваем</span></span></td><td class='r'>7</td><td class='r'>140</td><td class='r'>—</td><td class='r'>175</td></tr><tr class=dim><td class='nm'><b>Физика + география</b><span><span class="no">не рассматриваем</span></span></td><td class='r'>2</td><td class='r'>47</td><td class='r'>—</td><td class='r'>174</td></tr></tbody></table></div>
  <p><b>Два сочетания отпадают сразу.</b> «Математика и география» и «физика и география» —
  в них нет ни одной программы с проходным до 145 баллов, а у последней вообще две программы
  на оба города. Учить столько же, а выбора нет.</p>
  <p><b>«Физика и биология» — рабочий, но странный вариант.</b> 13 программ, и профильная
  математика не нужна вообще: пищевые технологии ВолгГТУ (131), Садоводство ВолГАУ (137),
  Лесное дело (140). Проблема в другом: физика стоит на математике, и учить физику,
  не занимаясь математикой, — самый верный способ не сдать ни то, ни другое.</p>
</div>

<div class="big" style="background:var(--acc-soft);border-color:var(--acc)">
  <h2>Четвёртый экзамен — самый выгодный ход</h2>
  <p>Биология до минимального порога стоит <b>34 часа</b> — дешевле любого другого предмета.
  Если сдавать не два предмета по выбору, а три, набор
  <b>русский + математика + физика + биология</b> открывает <b>65 программ и 1424 места</b>
  вместо 41 и 1070.</p>
  <p>Двадцать четыре дополнительные программы за примерно тридцать часов работы — при том,
  что весь основной набор стоит 185 часов. Прибавка меньше пятой части времени за
  полуторакратный рост выбора. Дешёвых программ (до 145 баллов) становится 21 вместо 10.</p>
  <p><b>И это же страховка.</b> Если к весне станет ясно, что физика не идёт, биология
  в запасе не даст остаться ни с чем: ветеринарно-санитарная экспертиза АГТУ — 125 баллов,
  пищевые технологии ВолГАУ — 126.</p>
  <p>Цена: четыре экзамена вместо трёх — это четыре дня в июне и риск, что на последнем
  кончатся силы. Решать ближе к зиме, когда будет видно, как идёт подготовка.</p>
</div>


<div class="big" style="margin-top:34px">
  <h2>Что решает, кроме баллов</h2>
  <p>На проходных 124–142 это значит не меньше, чем сам экзамен.</p>
  <ul class="steps">
    <li><b>Целевое обучение.</b> Отдельный конкурс, где людей обычно меньше, чем мест.
    Предложения — на портале «Работа России», заявка через Госуслуги вместе с основной.
    Цена: 3–5 лет отработки, при отказе — вернуть всю стоимость обучения.</li>
    <li><b>Индивидуальные достижения.</b> Волонтёрство, ГТО, аттестат с отличием — до 10 баллов.
    На таких проходных это решает исход.</li>
    <li><b>Правильная подача.</b> Пять вузов и пять специальностей — занять все. Первым
    приоритетом желаемое, последними — заведомо проходные направления с недобором.
    Не подать согласие — не попасть в приказ, даже проходя по баллам.</li>
    <li><b>Допнабор в августе.</b> Если основной этап не вышел, с 12 по 21 августа вузы
    добирают на оставшиеся места — чаще всего как раз на инженерных и аграрных направлениях.</li>
  </ul>
</div>

<div class="big">
  <h2>Как выбрать за неделю</h2>
  <ul class="steps">
    <li><b>Открой «Знакомство с ЕГЭ»</b> и пролистай три предмета: физику, биологию, географию.
    Там настоящие страницы экзамена 2027 года.</li>
    <li><b>Засеки, где не хочется закрыть вкладку.</b> Не «что кажется проще» — проще
    не будет нигде.</li>
    <li><b>Разбери по одному заданию из каждого</b> по разбору под страницей. Полчаса на предмет.</li>
    <li><b>Реши до ноября.</b> Смена предмета в январе означает, что три месяца из восьми ушли впустую.</li>
    <li><b>Дальше только работа:</b> три часа в неделю на предмет, без пропусков.</li>
  </ul>
</div>

<footer class="foot">Проходные баллы, конкурс и число зачисленных — из приказов о зачислении
2026 года. Часы — из разбора демоверсий ФИПИ 2027 по той же методике, что на странице
«Предметы ЕГЭ». Статистика и цитаты — по ссылкам. Цифры 2027 года изменятся: контрольные
цифры приёма распределяют осенью 2026, но набор направлений и порядок величин обычно
сохраняются.</footer>
</div>
</body>
</html>"""
open('varianty.html','w').write(PAGE)
print('varianty.html', len(PAGE)//1024, 'КБ')
