const WEEKS = 34;                     // до конца мая
const KEY = "vzvesit-v2";
let sel = new Set(["биология", "география"]);
try { const s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (Array.isArray(s) && s.length) sel = new Set(s); } catch (e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify([...sel])); } catch (e) {} };

const esc = s => String(s).replace(/[<>&]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;"}[c]));
const fq = v => v == null ? "—" : String(v).replace(".", ",");
const fk = v => (Number.isInteger(v) ? v + ",0" : String(v).replace(".", ","));
const passBall = p => p.s26 || p.s;
const openPl = p => p.o == null ? p.p : p.o;

const PRESETS = [
  ["Биология + география", ["биология", "география"]],
  ["Биология + химия", ["биология", "химия"]],
  ["Математика + физика", ["математика", "физика"]],
  ["Математика + информатика", ["математика", "информатика"]],
  ["Математика + география", ["математика", "география"]],
  ["Обществознание + история", ["обществознание", "история"]],
];

function fits(p, nab) {
  if (p.o === 0 || !passBall(p)) return false;
  const set = new Set(["русский", ...nab]);
  if (!p.r.every(x => set.has(x))) return false;
  if (p.ch.length && !p.ch.some(x => set.has(x))) return false;
  return true;
}

// три уровня цели: порог, по 50 за предмет, по 60
const LEVELS = [
  {key: "hp",  name: "Взять пороги",        per: 42, sum: 126, note: "минимум, чтобы результат засчитали"},
  {key: "h50", name: "По 50 за предмет",    per: 50, sum: 150, note: "нижняя граница реального"},
  {key: "h60", name: "По 60 за предмет",    per: 60, sum: 180, note: "уровень выше среднего по стране"},
];

function plan(nab) {
  return LEVELS.map(L => {
    const hours = ["русский", ...nab].reduce((s, k) => s + SUBJ_INFO[k][L.key], 0);
    const ok = PROGS.filter(p => fits(p, nab) && passBall(p) <= L.sum);
    return {...L, hours, week: +(hours / WEEKS).toFixed(1),
            n: ok.length, m: ok.reduce((a, p) => a + openPl(p), 0)};
  });
}

// вердикт: на каком уровне бюджет становится реальным и чего это стоит
function verdict(rows) {
  const good = rows.find(r => r.n >= 3 && r.m >= 60);
  if (!good) {
    const any = rows.find(r => r.n > 0);
    return any
      ? {cls: "t2", head: "Шанс есть, но узкий",
         text: `Даже на уровне «${any.name.toLowerCase()}» подходит всего ${any.n} программ. ` +
               `Такой набор стоит брать, только если эти направления действительно нужны.`}
      : {cls: "t2", head: "Бюджета с этим набором нет",
         text: "Ни одна бюджетная программа трёх городов не принимает такое сочетание предметов."};
  }
  const cls = good.week <= 6 ? "t0" : (good.week <= 11 ? "t0" : "t1");
  const how = good.week <= 6 ? "по часу в будний день"
            : (good.week <= 9 ? "полтора часа в будни и три в выходной"
            : (good.week <= 12 ? "два часа в будни и четыре в выходной"
            : "три часа каждый день без выходных"));
  return {cls, head: `На бюджет реально при цели «${good.name.toLowerCase()}»`,
          text: `Это ${good.n} программ и ${good.m} мест. Цена — ${fq(good.week)} часа в неделю ` +
                `до конца мая: ${how}. Всего ${good.hours} часов подготовки с нуля.`};
}

// какие задания нужно закрыть на 60 тестовых
function nabor60(t) {
  if (!t.list) return null;
  let got = 0; const keep = new Set();
  for (const [n, , b, lvl] of t.list) {
    if (n > t.part1 || got >= t.p60) continue;
    if (lvl !== "Б" && got + b <= t.p60 - 2) continue;   // повышенные берём в последнюю очередь
    keep.add(n); got += b;
  }
  for (const [n, , b] of t.list) {                        // добираем, если базовых не хватило
    if (got >= t.p60 || n > t.part1 || keep.has(n)) continue;
    keep.add(n); got += b;
  }
  return {keep, got};
}

function tasksBlock(nab) {
  return ["русский", ...nab].map(k => {
    const t = TASKS[k], i = SUBJ_INFO[k];
    if (!t) return "";
    const nb = nabor60(t);
    const head = `<div class="hd"><h3>${i.n}</h3>
      <span class="tag ${i.K <= 2.5 ? "t0" : (i.K <= 6 ? "t1" : "t2")}">${t.total} заданий</span></div>
      <p class="plus">На 60 баллов нужно ${t.p60} первичных из ${t.pmax}${
        nb ? `, это ${nb.keep.size} заданий из ${t.total}` : ""}. ${
        t.p60 <= t.pb1
          ? `Всё берётся первой частью: она даёт ${t.pb1} баллов, задачи с развёрнутым решением можно не трогать.`
          : `<b>Первой части не хватит:</b> она даёт ${t.pb1} баллов, нужно добрать ещё ${t.p60 - t.pb1} из второй части.`}</p>`;
    const body = t.list
      ? `<div class="tasks">${t.list.map(([n, name, b, lvl, ty, vol]) => {
          const on = nb && nb.keep.has(n);
          return `<div class="tk${on ? " on" : ""}${n > t.part1 ? " second" : ""}">
            <span class="tn">${n}</span>
            <span class="tt">${name}<span class="tw">${ty} · знаний ${vol}</span></span>
            <span class="tl">${lvl === "Б" ? "базовый" : (lvl === "П" ? "повышенный" : "высокий")}</span>
            <span class="tb">${b}</span>${on ? `<span class="tm">нужно</span>` : ""}</div>`;
        }).join("")}</div>`
      : `<div class="tasks">${t.blocks.map(([num, what, ball, ty, vol]) =>
          `<div class="tk blk"><span class="tn">${num.replace("Задания ", "").replace("Задание ", "")}</span>
           <span class="tt">${what}<span class="tw">${ty} · знаний ${vol}</span></span>
           <span class="tb2">${ball}</span></div>`).join("")}</div>`;
    return `<div class="sub-card">${head}${body}
      <div class="meta">Структура: ${t.src}. Баллы за отдельные задания —
      по демоверсии 2026; на 2027 год возможны сдвиги в нумерации.</div></div>`;
  }).join("");
}

function render() {
  const nab = [...sel];
  const ok = PROGS.filter(p => fits(p, nab)).sort((a, b) => passBall(a) - passBall(b));
  const rows = plan(nab);
  const v = nab.length ? verdict(rows) : null;
  const K = +(nab.reduce((s, k) => s + SUBJ_INFO[k].K, 0) + SUBJ_INFO["русский"].K).toFixed(1);

  document.getElementById("presets").innerHTML = PRESETS.map(([name, list]) => {
    const on = list.length === sel.size && list.every(x => sel.has(x));
    return `<button class="qp${on ? " on" : ""}" data-p="${list.join(",")}">${name}</button>`;
  }).join("");

  document.getElementById("picker").innerHTML = Object.keys(SUBJ_INFO)
    .filter(k => k !== "русский")
    .sort((a, b) => SUBJ_INFO[a].K - SUBJ_INFO[b].K)
    .map(k => `<button class="pk${sel.has(k) ? " on" : ""}" data-k="${k}">
        ${SUBJ_INFO[k].n}<span>${fk(SUBJ_INFO[k].K)}</span></button>`).join("");

  document.getElementById("out").innerHTML = !nab.length
    ? `<p style="color:var(--faint);margin-top:20px">Выберите хотя бы один предмет сверх русского.</p>`
    : `
    <section class="set verdict">
      <span class="tag ${v.cls}">${v.head}</span>
      <p style="margin-top:12px;font-size:16px">${v.text}</p>
    </section>

    <section>
      <h2>Три уровня цели</h2>
      <p class="lede" style="font-size:15.5px">Чем выше целитесь, тем больше часов и тем шире выбор.
      Часы — подготовка с нуля к концу мая, вместе с русским.</p>
      <div class="scroll"><table>
        <colgroup><col><col class="w1"><col class="w2"><col class="w1"><col class="w1"></colgroup>
        <tr><th>Цель</th><th class="r">Сумма<br>трёх ЕГЭ</th><th class="r">Часов<br>в неделю</th>
        <th class="r">Программ</th><th class="r">Мест</th></tr>
        ${rows.map(r => `<tr><td class="nm"><b>${r.name}</b><span>${r.note}</span></td>
          <td class="r">${r.sum}</td>
          <td class="r"><b style="color:var(--ink)">${fq(r.week)}</b><span class="cell-sub">${r.hours} ч всего</span></td>
          <td class="r">${r.n}</td><td class="r">${r.m}</td></tr>`).join("")}
      </table></div>
      <p style="font-size:13.5px;color:var(--faint);margin-top:12px">
      Суммарная сложность набора — ${fk(K)} по десятибалльной шкале, включая русский.</p>
    </section>

    <section>
      <h2>Подводные камни</h2>
      ${["русский", ...nab].map(k => {
        const i = SUBJ_INFO[k];
        return `<div class="sub-card">
          <div class="hd"><h3>${i.n}</h3><span class="tag ${i.K <= 2.5 ? "t0" : (i.K <= 6 ? "t1" : "t2")}">
            сложность ${fk(i.K)}</span></div>
          <p class="plus">${i.good}</p>
          <ul>${i.bad.map(b => `<li>${b}</li>`).join("")}</ul>
          <div class="meta">Курс ${i.h} ч · порог ${i.pp} первичных из ${i.pmax} = ${i.pt} баллов ·
            до 50 баллов ≈ ${i.h50} ч работы</div>
        </div>`;
      }).join("")}
    </section>

    <section>
      <h2>Объём: все задания экзамена</h2>
      <p class="lede" style="font-size:15.5px">Что именно спрашивают и сколько заданий нужно закрыть
      на 60 баллов. Отмеченные — минимальный набор: только первая часть, задачи с развёрнутым
      решением в него не входят.</p>
      ${tasksBlock(nab)}
    </section>

    <section>
      <h2>Куда можно поступить — все ${ok.length}</h2>
      <p class="lede" style="font-size:15.5px">Проходной — итог приёма 2026 года, конкурс — заявлений
      на бюджетное место. Нажмите на строку, чтобы прочитать, чем предстоит заниматься,
      какие плюсы и где подводные камни.</p>
      ${ok.length ? ok.map(p => {
          const b = passBall(p);
          const cls = b <= 150 ? "t0" : (b <= 180 ? "t0" : (b <= 200 ? "t1" : "t2"));
          const lab = b <= 150 ? "берётся по 50 за предмет" : (b <= 180 ? "по 60 за предмет"
                    : (b <= 200 ? "по 67 за предмет" : "по 70 и выше"));
          const g = DESC[p.code.slice(0, 2)];
          const note = p.nt && !/сводке|агрегатора|ориентир|данные вуза|проходной 20/.test(p.nt)
                     ? `<div class="note-line">${esc(p.nt)}</div>` : "";
          return `<details class="prog">
            <summary>
              <span class="pb">${b}</span>
              <span class="pn"><b>${esc(p.n)}</b><span>${esc(p.v)} · ${esc(p.c)}</span></span>
              <span class="pm">${openPl(p)} мест${p.k26 ? " · конкурс " + fq(p.k26) : ""}</span>
              <span class="tag ${cls}">${lab}</span>
            </summary>
            <div class="pbody">
              ${note}
              ${g ? `<p class="what"><b>${g.t}.</b> ${g.w}</p>
              <div class="pm2">
                <div><b>Плюсы</b><ul>${g.p.map(x => `<li>${x}</li>`).join("")}</ul></div>
                <div><b>Минусы и подводные камни</b><ul>${g.m.map(x => `<li>${x}</li>`).join("")}</ul></div>
              </div>` : ""}
            </div>
          </details>`;
        }).join("") : `<p style="color:var(--faint)">С этим набором бюджетных программ нет.</p>`}
    </section>`;

  document.querySelectorAll(".pk").forEach(b => b.onclick = () => {
    const k = b.dataset.k;
    sel.has(k) ? sel.delete(k) : sel.add(k);
    save(); render();
  });
  document.querySelectorAll(".qp").forEach(b => b.onclick = () => {
    sel = new Set(b.dataset.p.split(","));
    save(); render();
  });
}
render();
