// отрисовка заданий в виде, приближенном к бланку ЕГЭ
const FIG = {
 coords: `<svg viewBox="0 0 260 130" role="img" aria-label="Фрагмент карты с координатной сеткой">
   <rect x="1" y="1" width="258" height="128" fill="none" stroke="currentColor" stroke-width="1" opacity=".35"/>
   ${[40,90,140,190].map(x=>`<line x1="${x}" y1="1" x2="${x}" y2="129" stroke="currentColor" opacity=".18"/>`).join("")}
   ${[35,70,105].map(y=>`<line x1="1" y1="${y}" x2="259" y2="${y}" stroke="currentColor" opacity=".18"/>`).join("")}
   <text x="92" y="32" font-size="9" fill="currentColor" opacity=".6">30° в.д.</text>
   <text x="6" y="68" font-size="9" fill="currentColor" opacity=".6">60° с.ш.</text>
   <circle cx="90" cy="70" r="4" fill="currentColor"/>
   <text x="100" y="74" font-size="10" fill="currentColor">?</text></svg>`,
 graph: `<svg viewBox="0 0 260 150" role="img" aria-label="График координаты от времени">
   <line x1="30" y1="120" x2="240" y2="120" stroke="currentColor"/>
   <line x1="30" y1="120" x2="30" y2="15" stroke="currentColor"/>
   <polyline points="30,120 90,90 150,60 210,30" fill="none" stroke="currentColor" stroke-width="2.5"/>
   ${[0,1,2,3].map(i=>`<line x1="${30+i*60}" y1="120" x2="${30+i*60}" y2="124" stroke="currentColor"/>
     <text x="${26+i*60}" y="137" font-size="9" fill="currentColor">${i*2}</text>`).join("")}
   ${[0,1,2,3].map(i=>`<line x1="26" y1="${120-i*30}" x2="30" y2="${120-i*30}" stroke="currentColor"/>
     <text x="10" y="${124-i*30}" font-size="9" fill="currentColor">${i*4}</text>`).join("")}
   <text x="243" y="124" font-size="9" fill="currentColor">t, с</text>
   <text x="16" y="12" font-size="9" fill="currentColor">x, м</text></svg>`,
 triangle: `<svg viewBox="0 0 220 140" role="img" aria-label="Прямоугольный треугольник с катетами 6 и 8">
   <polygon points="40,120 40,30 160,120" fill="none" stroke="currentColor" stroke-width="2"/>
   <rect x="40" y="108" width="12" height="12" fill="none" stroke="currentColor" opacity=".6"/>
   <text x="18" y="78" font-size="12" fill="currentColor">6</text>
   <text x="95" y="136" font-size="12" fill="currentColor">8</text></svg>`,
 periodic: `<svg viewBox="0 0 220 90" role="img" aria-label="Фрагмент таблицы Менделеева">
   ${[0,1,2,3,4,5].map(i=>`<rect x="${10+i*34}" y="20" width="32" height="46" fill="none"
     stroke="currentColor" opacity=".35"/><text x="${16+i*34}" y="16" font-size="9"
     fill="currentColor" opacity=".6">${i+1}</text>`).join("")}
   <rect x="180" y="20" width="32" height="46" fill="none" stroke="currentColor" stroke-width="2"/>
   <text x="188" y="42" font-size="13" fill="currentColor" font-weight="700">O</text>
   <text x="184" y="58" font-size="8" fill="currentColor" opacity=".7">кислород</text></svg>`,
 demand: `<svg viewBox="0 0 240 150" role="img" aria-label="График спроса со смещением вправо">
   <line x1="30" y1="120" x2="220" y2="120" stroke="currentColor"/>
   <line x1="30" y1="120" x2="30" y2="15" stroke="currentColor"/>
   <line x1="45" y1="25" x2="140" y2="115" stroke="currentColor" stroke-width="2" opacity=".45"/>
   <line x1="95" y1="25" x2="195" y2="115" stroke="currentColor" stroke-width="2.5"/>
   <text x="140" y="22" font-size="9" fill="currentColor">D₁</text>
   <text x="196" y="30" font-size="9" fill="currentColor">D₂</text>
   <text x="222" y="124" font-size="9" fill="currentColor">Q</text>
   <text x="16" y="12" font-size="9" fill="currentColor">P</text></svg>`,
 map: `<svg viewBox="0 0 260 140" role="img" aria-label="Схема боевых действий">
   <rect x="1" y="1" width="258" height="138" fill="none" stroke="currentColor" opacity=".3"/>
   <path d="M20 110 Q 80 60 140 90 T 240 60" fill="none" stroke="currentColor" opacity=".5"/>
   <path d="M60 20 L 60 130" stroke="currentColor" opacity=".25" stroke-dasharray="5 4"/>
   <circle cx="140" cy="90" r="5" fill="currentColor"/>
   <text x="150" y="94" font-size="11" fill="currentColor" font-weight="700">1</text>
   <text x="24" y="130" font-size="9" fill="currentColor" opacity=".6">р. Волга</text></svg>`,
 photo: `<svg viewBox="0 0 220 140" role="img" aria-label="Фотография для описания">
   <rect x="10" y="10" width="200" height="120" fill="none" stroke="currentColor" opacity=".4"/>
   <circle cx="70" cy="55" r="16" fill="currentColor" opacity=".25"/>
   <path d="M25 120 L 80 70 L 120 110 L 160 75 L 200 120 Z" fill="currentColor" opacity=".18"/>
   <text x="66" y="134" font-size="9" fill="currentColor" opacity=".6">фотография</text></svg>`,
};

function renderTask(v) {
  if (v.type === "table") {
    return `<div class="ege-tbl"><table><tr>${v.head.map(h => `<th>${h}</th>`).join("")}</tr>
      ${v.rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join("")}</tr>`).join("")}</table></div>`;
  }
  if (v.type === "match") {
    return `<div class="ege-match">
      <div>${v.left.map(([l, t]) => `<div class="mr"><b>${l}</b> ${t}</div>`).join("")}</div>
      <div>${v.right.map(([n, t]) => `<div class="mr"><b>${n}</b> ${t}</div>`).join("")}</div>
    </div>
    <div class="ege-ans"><span>Ответ:</span>${v.left.map(([l]) =>
      `<i><em>${l}</em></i>`).join("")}</div>`;
  }
  if (v.type === "choices") {
    const num = v.numbered === false;
    return `<ol class="ege-ch${num ? " lettered" : ""}">${v.items.map(x => `<li>${x}</li>`).join("")}</ol>
      <div class="ege-ans"><span>Ответ:</span><i></i><i></i><i></i></div>`;
  }
  if (v.type === "formula") {
    return `<div class="ege-f">${v.items.map(x => `<div>${x}</div>`).join("")}</div>
      <div class="ege-ans"><span>Ответ:</span><i></i><i></i><i></i><i></i></div>`;
  }
  if (v.type === "quote") {
    return `<blockquote class="ege-q">${v.text}</blockquote>`;
  }
  if (v.type === "figure") {
    return `<div class="ege-fig">${FIG[v.kind] || ""}</div>` +
      (v.kind === "photo" || v.kind === "map" ? "" :
       `<div class="ege-ans"><span>Ответ:</span><i></i><i></i><i></i><i></i></div>`);
  }
  if (v.type === "text") {
    return `<div class="ege-lines${v.code ? " code" : ""}">${
      Array.from({length: v.lines}, () => `<span></span>`).join("")}</div>`;
  }
  return "";
}
