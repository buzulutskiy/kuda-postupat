const WEEKS = 34;              // до конца мая
const KEY = "vzvesit-v1";
let sel = new Set(["физика", "математика"]);
try { const s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (Array.isArray(s) && s.length) sel = new Set(s); } catch (e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify([...sel])); } catch (e) {} };

const esc = s => String(s).replace(/[<>&]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;"}[c]));
const fq = v => v == null ? "—" : String(v).replace(".", ",");
const fk = v => (Number.isInteger(v) ? v + ",0" : String(v).replace(".", ","));

const passBall = p => p.s26 || p.s;
const openPl = p => p.o == null ? p.p : p.o;

function fits(p, nab) {
  if (p.o === 0 || !passBall(p)) return false;
  const set = new Set(["русский", ...nab]);
  if (!p.r.every(x => set.has(x))) return false;
  if (p.ch.length && !p.ch.some(x => set.has(x))) return false;
  return true;
}

// суммарная оценка набора
function effort(nab) {
  const hours = nab.reduce((s, k) => s + SUBJ_INFO[k].h, 0) + SUBJ_INFO["русский"].h;
  const K = nab.reduce((s, k) => s + SUBJ_INFO[k].K, 0) + SUBJ_INFO["русский"].K;
  // до целевого уровня уходит ~60% курса
  const need = Math.round(hours * 0.6);
  const perWeek = +(need / WEEKS).toFixed(1);
  let verdict, cls;
  if (perWeek <= 7) { verdict = "спокойно"; cls = "t0"; }
  else if (perWeek <= 10) { verdict = "плотно, но реально"; cls = "t0"; }
  else if (perWeek <= 14) { verdict = "тяжело"; cls = "t1"; }
  else { verdict = "на грани невозможного"; cls = "t2"; }
  return {hours, need, perWeek, K: +K.toFixed(1), verdict, cls};
}

function scenarios(ok) {
  // сумма трёх: порог / минимум / средние / хороший
  return [["Взяли только пороги", 125], ["Слабо: по 45 за предмет", 135],
          ["Минимум: по 50", 150], ["Средние баллы: по 57", 172], ["Хорошо: по 63", 190]]
    .map(([name, s]) => {
      const g = ok.filter(p => passBall(p) <= s);
      return {name, s, n: g.length, m: g.reduce((a, p) => a + openPl(p), 0)};
    });
}

function render() {
  const nab = [...sel];
  const ok = PROGS.filter(p => fits(p, nab)).sort((a, b) => passBall(a) - passBall(b));
  const e = effort(nab);
  const sc = scenarios(ok);

  document.getElementById("picker").innerHTML = Object.keys(SUBJ_INFO)
    .filter(k => k !== "русский")
    .sort((a, b) => SUBJ_INFO[a].K - SUBJ_INFO[b].K)
    .map(k => `<button class="pk${sel.has(k) ? " on" : ""}" data-k="${k}">
        ${SUBJ_INFO[k].n}<span>${fk(SUBJ_INFO[k].K)}</span></button>`).join("");

  document.getElementById("out").innerHTML = !nab.length
    ? `<p style="color:var(--faint);margin-top:20px">Выберите хотя бы один предмет сверх русского.</p>`
    : `
    <section class="set">
      <div class="stats">
        <div><b class="num">${fk(e.K)}</b><span>суммарная<br>сложность</span></div>
        <div><b class="num">${e.need}</b><span>часов до цели<br>из ${e.hours} курса</span></div>
        <div><b class="num">${fq(e.perWeek)}</b><span>часов в неделю<br>до конца мая</span></div>
        <div><b class="num">${ok.length}</b><span>программ<br>подходит</span></div>
      </div>
      <p style="margin-top:16px"><span class="tag ${e.cls}">${e.verdict}</span>
      <span style="margin-left:10px;font-size:14px;color:var(--faint)">
      при восьми месяцах и нулевых знаниях</span></p>
      <p style="font-size:13.5px;color:var(--faint);margin-top:10px">
      Считается так: до нужного уровня уходит около 60 процентов школьного курса,
      это ${e.need} часов, и они делятся на 34 недели до конца мая. Целиться ниже — значит
      и часов меньше, но и список программ короче.</p>
    </section>

    <section class="set">
      <div class="kick">Что получится при разном результате</div>
      <div class="scroll"><table style="margin-top:12px">
        <colgroup><col><col class="w1"><col class="w1"><col class="w1"></colgroup>
        <tr><th>Исход</th><th class="r">Сумма</th><th class="r">Программ</th><th class="r">Мест</th></tr>
        ${sc.map(s => `<tr><td class="nm"><b>${s.name}</b></td><td class="r">${s.s}</td>
          <td class="r">${s.n}</td><td class="r">${s.m}</td></tr>`).join("")}
      </table></div>
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
          <div class="meta">Курс ${i.h} ч · порог ${i.pp} первичных из ${i.pmax} = ${i.pt} баллов</div>
        </div>`;
      }).join("")}
    </section>

    <section>
      <h2>Куда можно поступить — все ${ok.length}</h2>
      <p class="lede" style="font-size:15.5px">Проходной — итог приёма 2026 года, конкурс — заявлений
      на бюджетное место. Зелёным отмечено то, что берётся средними баллами.</p>
      ${ok.length ? `<div class="scroll"><table>
        <colgroup><col><col class="w2"><col class="w1"><col class="w1"><col class="w2"></colgroup>
        <tr><th>Направление</th><th class="r">Проходной</th><th class="r">Конкурс</th>
        <th class="r">Мест</th><th class="r">Оценка</th></tr>
        ${ok.map(p => {
          const b = passBall(p);
          const cls = b <= 172 ? "t0" : (b <= 190 ? "t1" : "t2");
          const lab = b <= 172 ? "средними" : (b <= 190 ? "выше среднего" : "трудно");
          return `<tr><td class="nm"><b>${esc(p.n)}</b><span>${esc(p.v)} · ${esc(p.c)} — ${
            GRP[p.code.slice(0,2)] || ""}</span></td>
            <td class="r">${b}</td><td class="r">${fq(p.k26)}</td>
            <td class="r">${openPl(p)}</td>
            <td class="r"><span class="tag ${cls}">${lab}</span></td></tr>`;
        }).join("")}
      </table></div>` : `<p style="color:var(--faint)">С этим набором бюджетных программ нет.</p>`}
    </section>`;

  document.querySelectorAll(".pk").forEach(b => b.onclick = () => {
    const k = b.dataset.k;
    sel.has(k) ? sel.delete(k) : sel.add(k);
    save(); render();
  });
}
render();
