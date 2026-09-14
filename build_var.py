# -*- coding: utf-8 -*-
"""Страница «Варианты» — маршруты Марка на бюджет."""
import json, html

R = json.load(open('/tmp/page_routes.json'))
BASE = open('/tmp/base.css').read()

def esc(s): return html.escape(s, quote=False)

def hours_line(d):
    parts = [f"{k} {v} ч" for k, v in d['h50'].items()]
    return " · ".join(parts) + f" = <b>{sum(d['h50'].values())} ч</b>"

def prog_rows(d):
    rows = []
    for t in d['top']:
        k = f"конкурс {t['k']}" if t['k'] else "—"
        m = f"{t['m']}" if t['m'] else "—"
        rows.append(f"<tr><td class='nm'><b>{esc(t['n'][:52])}</b><span>{esc(t['v'])}</span></td>"
                    f"<td class='r'>{t['s']}</td><td class='r'>{t['p']}</td>"
                    f"<td class='r'>{k}</td><td class='r'>{m}</td></tr>")
    return "".join(rows)

cards = []
for i, d in enumerate(R, 1):
    wide = d['n'] >= 20
    cards.append(f"""
<section class="route{' dead' if d['n'] <= 3 else ''}" id="r{i}">
  <div class="rhead">
    <div>
      <div class="kick">Вариант {i}</div>
      <h2>{esc(d['name'])}</h2>
      <p class="who">{esc(d['who'])}</p>
    </div>
    <div class="rnum">
      <div><b>{d['n']}</b><span>программ</span></div>
      <div><b>{d['places']}</b><span>мест</span></div>
      <div><b>{sum(d['h50'].values())}</b><span>часов</span></div>
    </div>
  </div>
  <div class="cols">
    <div class="pro"><h3>Что хорошего</h3><ul>{''.join(f'<li>{esc(x)}</li>' for x in d['plus'])}</ul></div>
    <div class="con"><h3>Чем платишь</h3><ul>{''.join(f'<li>{esc(x)}</li>' for x in d['minus'])}</ul></div>
  </div>
  <div class="hrs">Часы до 50 баллов по каждому предмету: {hours_line(d)}.
    До минимального порога — {sum(d['hp'].values())} ч.</div>
  {'<div class="scroll"><table><colgroup><col><col class="w1"><col class="w2"><col class="w3"><col class="w4"></colgroup>'
   '<thead><tr><th>Куда проходит</th><th class="r">Проходной</th><th class="r">Мест</th>'
   '<th class="r">Конкурс</th><th class="r">Зачислено</th></tr></thead><tbody>'
   + prog_rows(d) + '</tbody></table></div>' if d['top'] else ''}
  <p class="try">Проверить на себе: <a href="znakomstvo.html">открой настоящие задания</a>
    и посмотри {esc(d['check'])} — не «кажется ли проще», а хочется ли в этом разбираться.</p>
</section>""")

PAGE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Шесть вариантов набора предметов ЕГЭ: что каждый открывает, сколько стоит в часах и чем за него платишь.">
<meta name="color-scheme" content="light dark">
<title>Шесть дорог на бюджет</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vollkorn:ital,wght@0,500;0,700;1,500&family=PT+Sans:wght@400;700&display=swap">
<style>{BASE}
.tog{{display:inline-flex;gap:0;border:1px solid var(--line);border-radius:7px;overflow:hidden;flex-wrap:wrap}}
.tog .tb-l{{display:inline-block;padding:7px 13px;font-size:13.5px;color:var(--faint);
  text-decoration:none;border-left:1px solid var(--line)}}
.tog .tb-l:first-child{{border-left:none}}
.tog .tb-l:hover{{background:var(--sand);color:var(--ink)}}
.tog .tb-l.on{{background:var(--acc-soft);color:var(--ink);font-weight:700}}
.navbar{{margin:0 0 20px}}
.route{{border-top:1px solid var(--line);padding-top:26px;margin-top:30px}}
.route.dead{{opacity:.72}}
.rhead{{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:flex-start}}
.rhead h2{{font-size:27px;margin-top:6px}}
.who{{margin-top:9px;font-size:15.5px;max-width:46ch}}
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
.big p{{margin-top:11px;font-size:15px;max-width:64ch}}
.q{{border-left:3px solid var(--line);padding:2px 0 2px 16px;margin:14px 0;font-size:14.5px}}
.q b{{color:var(--ink)}}
.q cite{{display:block;font-style:normal;font-size:12.5px;color:var(--faint);margin-top:5px}}
.q cite a{{color:var(--faint)}}
.steps{{counter-reset:s;display:grid;gap:14px;margin-top:16px}}
.steps li{{list-style:none;position:relative;padding-left:38px;font-size:15px}}
.steps li::before{{counter-increment:s;content:counter(s);position:absolute;left:0;top:-1px;
  width:26px;height:26px;border-radius:50%;background:var(--acc-soft);color:var(--acc);
  font-weight:700;font-size:13px;display:grid;place-items:center}}
.steps b{{color:var(--ink)}}
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
<header style="border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:10px">
  <div class="kick">Решать тебе</div>
  <h1 style="margin-top:10px">Шесть дорог на бюджет</h1>
  <p class="lede">Задача простая: поступить на бюджет, всё равно куда. Времени — до июня 2027,
  база — почти с нуля. Ниже шесть наборов предметов: что каждый открывает, сколько стоит в часах
  и чем за него придётся заплатить. Цифры — из приказов о зачислении 2026 года и разбора
  демоверсий ФИПИ 2027. Выбирать никто за тебя не будет.</p>
</header>

<div class="big">
  <h2>Три вещи, которые надо понять до выбора</h2>
  <p><b>1. Настоящая развилка — не физика, а профильная математика.</b> Из 75 бюджетных программ
  с проходным до 170 баллов она нужна на 40. Всё остальное — вопрос вкуса, а это — вопрос
  доступа к половине мест.</p>
  <p><b>2. Физику и информатику почти везде принимают на выбор.</b> Строго физика нужна ровно
  на одной программе из 75, а 56 программ берут любой из этих двух предметов. Если физика
  не идёт — её можно не брать, не теряя почти ничего.</p>
  <p><b>3. «Лёгкий предмет» — миф, который дорого стоит.</b> Обществознание выбирают 255 тысяч
  человек в год, и средний балл по нему 53,6 — минимум за шесть лет; порог не берёт примерно
  каждый пятый. У биологии средний балл 54,5 и 16% не прошедших порог — это худшие цифры
  среди всех ЕГЭ. Лёгких предметов не бывает, бывают разные виды труда.</p>
</div>

{''.join(cards)}

<div class="big" style="margin-top:34px">
  <h2>Что говорят те, кто уже пробовал</h2>
  <p>Это не мои выводы, а то, что пишут учителя, репетиторы и выпускники. Ссылки на источники —
  под каждой цитатой.</p>

  <h3 style="margin-top:20px;font-size:17px">Про физику с нуля</h3>
  <div class="q"><b>Учитель физики Константин Барковец:</b> если учишься в обычном классе,
  где физика два раза в неделю, «в лучшем случае перейдёшь порог, школьной базовой программы
  не хватит». Готовиться — значит решать не две задачи в день, а двадцать.
  <cite><a href="https://www.pravmir.ru/mnogie-deti-umnee-menya-uchitel-fiziki-konstantin-barkovecz/">Правмир, 2024</a></cite></div>
  <div class="q"><b>Репетитор И. В. Яковлев:</b> «От самостоятельной подготовки к ЕГЭ по физике
  предостерегаю сразу и категорически». Оптимальный срок — два года, с начала 10 класса.
  Отдельно: «плохая математическая подготовка мешает школьникам решать физические задачи».
  <cite><a href="https://mathus.ru/art/egephys2.php">mathus.ru</a></cite></div>
  <div class="q"><b>Официальная статистика по региону (Башкортостан, 2025):</b> среди тех,
  кто выбрал физику — а это уже мотивированные ребята — <b>36,4% не дотянули до 60 баллов</b>,
  средний балл упал с 68,8 до 65,4.
  <cite><a href="https://irorb.ru/wp-content/uploads/2026/04/metodicheskie-rekomendaczii-po-podgotovke-k-gia-po-fizike-v-2025-%E2%80%93-2026-uchebnom-godu-na-osnove-analiza-ege-2026.pdf">Методический анализ ЕГЭ по физике, 2025</a></cite></div>
  <div class="q">Истории с хорошим концом тоже есть, но у всех одна особенность: либо была
  скрытая база (74 балла за три месяца), либо репетитор или курс (86 баллов через онлайн-школу).
  Чисто самостоятельной истории «с нуля за год на 60+» не нашлось ни одной.
  <cite><a href="https://otvet.mail.ru/question/231140003">Ответы Mail.ru</a>,
  <a href="https://www.woman.ru/kids/nursery/thread/5914189/">Woman.ru</a></cite></div>

  <h3 style="margin-top:22px;font-size:17px">Про биологию</h3>
  <div class="q"><b>Маша, 2025:</b> готовилась два года с репетиторами, потратила больше
  200 тысяч рублей. Химия 56, <b>биология 43</b>, русский 52. До цели не хватило девяти баллов,
  ушла на платное.
  <cite><a href="https://t-j.ru/vinyu-sebya-za-lyuboj-otdyh/">Т—Ж, 2025</a></cite></div>
  <div class="q"><b>Выпускники о ЕГЭ-2025:</b> «Ощущение, что готовилась зря». Тяжелее всего —
  генетическая задача и трофические уровни; «задания немного отличались от демоверсий».
  <cite><a href="https://mel.fm/novosti/7461839-popalas-v-lovushku-v-odnom-zadanii-uzhas-vypuskniki-s-dalnego-vostoka--o-yege-po-biologii">Мел, 2025</a></cite></div>
  <div class="q">Порог по биологии не берут 16–19% сдающих, средний балл 54,5 — один из самых
  низких среди всех предметов. Основные баллы теряют во второй части: любая биологическая
  ошибка обнуляет весь развёрнутый ответ.
  <cite><a href="https://ege.lancmanschool.ru/poleznyie-stati/itogi-ege-po-biologii-2024-goda/">Итоги ЕГЭ по биологии</a>,
  <a href="https://www.rbc.ru/society/07/07/2025/6869aaa49a7947837dab9d83">РБК, 2025</a></cite></div>

  <h3 style="margin-top:22px;font-size:17px">Про географию</h3>
  <div class="q"><b>Учитель географии Дмитрий Коменденко:</b> «География далеко не простой
  экзамен» — там картография и вычисления. Школа даёт минимум, глубокие знания — нет.
  <cite><a href="https://pedsovet.org/article/geografia-hit-sezona-kak-novye-pravila-priema-v-vuzy-izmenat-otnosenie-k-etomu-predmetu">Педсовет</a></cite></div>
  <div class="q">Средний балл по географии — <b>54,8</b>, то есть не выше, чем у обществознания
  и биологии. Миф «выучил учебник — и пятёрка» статистикой не подтверждается.
  <cite><a href="https://4ege.ru/novosti-ege/75487-srednie-bally-ege-2025.html">Средние баллы ЕГЭ-2025</a></cite></div>
  <div class="q"><b>Зато конкурс ниже.</b> Географию сдают всего около 21 тысячи человек в год —
  это 2,7% выпускников, самый непопулярный предмет. Обратная сторона та же: и программ,
  где она принимается, мало.
  <cite><a href="https://media.foxford.ru/articles/ege-geography">Фоксфорд</a></cite></div>

  <h3 style="margin-top:22px;font-size:17px">Про обществознание</h3>
  <div class="q"><b>Юлия:</b> взяла обществознание и биологию как «понятные» предметы,
  готовилась без репетиторов — <b>не набрала минимум по обоим</b>. Ушла в колледж на платное.
  <cite><a href="https://pedsovet.org/article/est-li-zizn-posle-provalennogo-ege-istorii-vypusknikov-raznyh-let">Педсовет</a></cite></div>
  <div class="q">Причина не в сложности мыслей, а в объёме: кодификатор — 75 тем из пяти разных
  наук, единого учебника нет, вторая часть каждый год ужесточается.
  <cite><a href="https://ege-obschestvo.ru/tpost/8pte04va71-statistika-ege-po-obschestvoznaniyu">Разбор статистики</a></cite></div>
</div>

<div class="big">
  <h2>Что решает, кроме баллов</h2>
  <p>Четыре вещи, которые на этих проходных значат не меньше, чем сам экзамен.</p>
  <ul class="steps">
    <li><b>Целевое обучение.</b> Отдельный конкурс, где людей обычно меньше, чем мест.
    Предложения работодателей — на портале «Работа России», заявка подаётся вместе с основной
    через Госуслуги. Цена: 3–5 лет отработки у заказчика, а при отказе — вернуть всю стоимость
    обучения. С 2026 одна заявка — один вуз.</li>
    <li><b>Индивидуальные достижения.</b> Волонтёрство, ГТО, аттестат с отличием — до 10 баллов.
    На проходных 124–140 это решает исход. В одной из историй парень прямо написал:
    «если бы не пять баллов за волонтёрство, я бы не поступил».</li>
    <li><b>Правильная подача.</b> Пять вузов и пять специальностей — надо занять все.
    Первым приоритетом ставить желаемое, последними — заведомо проходные направления,
    где недобор. Заочная форма и филиалы почти всегда идут ниже очной. Не подать согласие —
    значит не попасть в приказ, даже если проходишь по баллам.</li>
    <li><b>Допнабор в августе.</b> Если основной этап не вышел, с 12 по 21 августа вузы
    добирают на оставшиеся места: в 2026 это была сотня вузов и больше двух тысяч мест.
    Чаще всего недобор — как раз на инженерных и аграрных направлениях.</li>
  </ul>
</div>

<div class="big">
  <h2>Как выбрать за неделю, а не за полгода</h2>
  <ul class="steps">
    <li><b>Открой «Знакомство с ЕГЭ»</b> и пролистай четыре предмета подряд: физику,
    информатику, биологию, географию. Там настоящие страницы экзамена 2027 года.</li>
    <li><b>Засеки, где не хочется закрыть вкладку.</b> Не «что кажется проще» — проще не будет
    нигде. Важно, где хочется понять, как это устроено.</li>
    <li><b>Возьми по одному заданию из каждого</b> и попробуй разобраться по разбору под
    страницей. Полчаса на предмет. Это даёт больше, чем месяц размышлений.</li>
    <li><b>Реши до ноября.</b> После Нового года смена предмета означает, что три месяца
    работы ушли впустую — а их всего восемь.</li>
    <li><b>Скажи вслух, что выбрал, и запиши дату.</b> Дальше — только работа: 3 часа в неделю
    на предмет, без пропусков. Это и есть вся стратегия.</li>
  </ul>
</div>

<div class="big" style="background:var(--sand);border:none">
  <h2>Если коротко</h2>
  <p><b>Самый широкий путь</b> — профильная математика плюс физика или информатика: 41 и 39
  программ, больше тысячи мест, проходные от 124. Но физика стоит на математике, и если
  математика идёт тяжело, восемь месяцев уйдут на добор алгебры, а не на физику.</p>
  <p><b>Самый спокойный путь</b> — биология с географией: ни одного задания уровня «тяжело»,
  дешевле всех до порога. Но это 11 программ и 181 место, почти всё — аграрное
  и рыбохозяйственное. Не «плохо», а узко: надо заранее быть согласным на такую специальность.</p>
  <p><b>Чего точно не стоит делать</b> — брать обществознание в расчёте на лёгкость. Три
  программы, 48 мест и худшая статистика сдачи по стране.</p>
  <p>И последнее. Любой из этих путей работает только при одном условии — что занимаешься
  регулярно с осени. Восемь месяцев по три часа в неделю — это 100 часов на предмет,
  ровно столько, сколько нужно на 50 баллов по большинству из них. Опоздание на два месяца
  этот запас съедает целиком.</p>
</div>

<footer class="foot">Проходные баллы, конкурс и число зачисленных — из приказов о зачислении
2026 года (Поступашкин). Часы и сложность заданий — из разбора демоверсий ФИПИ 2027 по единой
методике, той же, что на странице «Предметы ЕГЭ». Цитаты и статистика — по ссылкам под ними.
Числа по 2027 году изменятся: контрольные цифры приёма распределяют осенью 2026,
но набор направлений и порядок величин обычно сохраняются.</footer>
</div>
</body>
</html>"""
open('varianty.html','w').write(PAGE)
print('varianty.html', len(PAGE)//1024, 'КБ')
