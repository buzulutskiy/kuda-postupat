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
const openPl = p => p.p26 != null ? p.p26 : (p.o == null ? p.p : p.o);



function fits(p, nab) {
  if (openPl(p) === 0 || !passBall(p)) return false;
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

// сложность отдельного задания: масштаб предмета × формат × объём × уровень × тип работы
const KWORD = k =>
  k < 1.5 ? "совсем просто" :
  k < 2.5 ? "просто" :
  k < 4   ? "надо выучить" :
  k < 6   ? "средне" :
  k < 8   ? "тяжело" : "очень тяжело";

function taskK(subjKey, b, lvl, ty, vol, fmt) {
  // предмет задаёт масштаб, но решает само задание: формат, объём, уровень, тип работы
  const sub = 1 + (SUBJ_INFO[subjKey].K - 1) * 0.30;
  const f = /выбрать/.test(fmt) ? 0.8
          : (/написать|сочинение|программу|развёрнут|аргумент|сопоставл|план|объяснение|решение с/.test(fmt) ? 2.0 : 1.3);
  const v = vol === "мало" ? 0.85 : (vol === "много" ? 1.2 : 1.0);
  const l = lvl === "Б" ? 1.0 : (lvl === "П" ? 1.2 : 1.5);
  const t = /теория|заучивание|правила/.test(ty) ? 0.95
          : (/программирование|сочинение/.test(ty) ? 1.35 : 1.1);
  return +Math.min(10, Math.max(0.5, sub * f * v * l * t)).toFixed(1);
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
    const need = nb ? t.list.filter(r => nb.keep.has(r[0])) : [];
    const avg = need.length
      ? +(need.reduce((s, r) => s + taskK(k, r[2], r[3], r[4], r[5], r[6]), 0) / need.length).toFixed(1)
      : null;
    const head = `<div class="hd"><h3>${i.n}</h3>
      <span class="tag ${i.K <= 2.5 ? "t0" : (i.K <= 6 ? "t1" : "t2")}">${t.total} заданий</span></div>
      <p class="plus">На 60 баллов нужно ${t.p60} первичных из ${t.pmax}${
        nb ? `, это ${nb.keep.size} заданий из ${t.total}${avg ? `, в среднем «${KWORD(avg)}»` : ""}` : ""}. ${
        t.p60 <= t.pb1
          ? `Всё берётся первой частью: она даёт ${t.pb1} баллов, развёрнутые задачи можно не трогать.`
          : `<b>Первой части не хватит:</b> она даёт ${t.pb1} баллов, нужно добрать ещё ${t.p60 - t.pb1} из второй части.`}</p>`;
    const body = t.list
      ? `<div class="tasks">${t.list.map(([n, name, b, lvl, ty, vol, fmt]) => {
          const on = nb && nb.keep.has(n);
          const self = /написать|сочинение|программу|решение|развёрнут|объяснить|аргумент|сопоставл|разобрать|план/.test(fmt)
            ? "hard" : (/выбрать/.test(fmt) ? "easy" : "mid");
          const tk = taskK(k, b, lvl, ty, vol, fmt);
          const w = Math.round(tk / 10 * 100);
          return `<div class="tk${on ? " on" : ""}${n > t.part1 ? " second" : ""}">
            <span class="tn">${n}</span>
            <span class="tt">${name}<span class="tw">${fmt}</span></span>
            <span class="tks"><i style="width:${w}%" class="${self}"></i><b>${KWORD(tk)}</b></span>
            <span class="tb">${b}</span></div>`;
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
  const v = nab.length ? verdict(plan(nab)) : null;
  const K = +(nab.reduce((s, k) => s + SUBJ_INFO[k].K, 0) + SUBJ_INFO["русский"].K).toFixed(1);

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
      <p class="lede" style="font-size:15.5px">Что именно спрашивают, что надо сделать руками
      и сколько заданий нужно закрыть на 60 баллов. Отмеченные — минимальный набор.</p>
      <div class="legend">
        <span><i class="sq easy"></i>выбрать из вариантов</span>
        <span><i class="sq mid"></i>решить и вписать ответ</span>
        <span><i class="sq hard"></i>написать самому</span>
        <span>Справа — насколько тяжело даётся само задание</span>
      </div>
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
              <span class="pm">${openPl(p)} мест${p.sog26 ? " · согласий " + p.sog26 : ""}${p.k26 ? " · заявлений " + (p.zay26 || "") : ""}</span>
              <span class="tag ${cls}">${lab}</span>
            </summary>
            <div class="pbody">
              ${note}
              ${VUZSLUG[p.v] ? `<p class="src-line"><a href="${PKV}${VUZSLUG[p.v]}/priem-2026"
                target="_blank" rel="noopener">Проверить на Поступашкине: приём 2026 в ${esc(p.v)} →</a></p>` : ""}
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
}
render();
