/* Slide engine for the HTML deck: navigation, scaling, presenter view, the
 * hands-on timer and the live poll results. No dependencies.
 *
 * Keys: → / Space / PageDown next · ← / PageUp previous · Home / End ·
 *       a number then Enter to jump · F full screen · S presenter view ·
 *       T start or pause the timer · ? help
 */
(function () {
  const W = 1920, H = 1080;
  const params = new URLSearchParams(location.search);
  const SPEAKER = params.has("speaker");
  const stage = document.querySelector(".stage");
  const slides = [...stage.querySelectorAll(":scope > .slide")];
  const N = slides.length;
  const chan = "BroadcastChannel" in window ? new BroadcastChannel("deck-sync") : null;
  let cur = 0;

  // ---------- footer, page numbers and part labels ----------
  const PARTS = { 0: "From data to decision", 1: "Part 1 · Dashboard explainer", 2: "Part 2 · Hands-on exercise", 3: "Part 3 · Uses of AI" };
  slides.forEach((s, i) => {
    if (s.dataset.nofoot === undefined) {
      const f = document.createElement("div"); f.className = "foot";
      const l = document.createElement("span"), dot = document.createElement("i"); dot.className = "part-dot";
      l.append(dot, s.classList.contains("appendix") ? "Appendix" : PARTS[s.dataset.part || 0]);
      const r = document.createElement("span"); r.textContent = (i + 1) + " / " + N;
      f.append(l, r); s.append(f);
    }
    const p = document.createElement("div"); p.className = "progress"; p.style.width = (100 * (i + 1) / N) + "%"; s.append(p);
  });

  // ---------- scaling ----------
  function fit(box, st) {
    const r = box.getBoundingClientRect(), s = Math.min(r.width / W, r.height / H);
    st.style.transform = `translate(-50%, -50%) scale(${s})`;
  }

  // ---------- navigation ----------
  function show(n, from) {
    n = Math.max(0, Math.min(N - 1, n));
    slides.forEach((s, i) => s.classList.toggle("active", i === n));
    cur = n;
    if (location.hash !== "#" + (n + 1)) history.replaceState(null, "", location.pathname + location.search + "#" + (n + 1));
    if (chan && from !== "remote") chan.postMessage({ type: "goto", n });
    if (SPEAKER) speakerRender();
  }
  const fromHash = () => { const m = location.hash.match(/^#(\d+)/); return m ? +m[1] - 1 : 0; };

  let digits = "";
  document.addEventListener("keydown", e => {
    if (e.target.closest("input, textarea, select")) return;
    const k = e.key;
    if (["ArrowRight", "PageDown", " ", "ArrowDown"].includes(k)) { e.preventDefault(); show(cur + 1); }
    else if (["ArrowLeft", "PageUp", "ArrowUp", "Backspace"].includes(k)) { e.preventDefault(); show(cur - 1); }
    else if (k === "Home") show(0);
    else if (k === "End") show(N - 1);
    else if (/^\d$/.test(k)) { digits += k; }
    else if (k === "Enter" && digits) { show(+digits - 1); digits = ""; }
    else if (k === "f" || k === "F") { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen().catch(() => {}); }
    else if (k === "s" || k === "S") { window.open(location.pathname + "?speaker" + (params.get("topic") ? "&topic=" + params.get("topic") : "") + "#" + (cur + 1), "deck-speaker", "width=1300,height=800"); }
    else if (k === "t" || k === "T") Timer.toggle();
    else if (k === "?") document.querySelector(".help").classList.toggle("on");
    else if (k === "Escape") document.querySelector(".help").classList.remove("on");
    if (!/^\d$/.test(k) && k !== "Enter") digits = "";
  });
  let tx = null;
  document.addEventListener("touchstart", e => { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", e => { if (tx == null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); tx = null; });
  // buttons that jump to a named slide (the appendix and back)
  document.addEventListener("click", e => {
    const g = e.target.closest("[data-goto]"); if (!g) return;
    const i = slides.findIndex(s => s.dataset.id === g.dataset.goto); if (i >= 0) show(i);
  });
  document.querySelector(".nav .prev").addEventListener("click", () => show(cur - 1));
  document.querySelector(".nav .next").addEventListener("click", () => show(cur + 1));
  document.querySelector(".nav .help-btn").addEventListener("click", () => document.querySelector(".help").classList.toggle("on"));
  document.querySelector(".help").addEventListener("click", () => document.querySelector(".help").classList.remove("on"));
  if (chan) chan.onmessage = ev => {
    const m = ev.data;
    if (m.type === "goto" && m.n !== cur) show(m.n, "remote");
    if (m.type === "timer") Timer.apply(m.state, true);
  };

  // ---------- hands-on timer (shared by every open view) ----------
  const Timer = (function () {
    const TOTAL = 15 * 60;
    let st = { running: false, endsAt: 0, left: TOTAL };
    const els = () => document.querySelectorAll("[data-timer]");
    const left = () => st.running ? Math.max(0, Math.round((st.endsAt - Date.now()) / 1000)) : st.left;
    function draw() {
      const s = left(), mm = String(Math.floor(s / 60)).padStart(2, "0"), ss = String(s % 60).padStart(2, "0");
      els().forEach(box => {
        const t = box.querySelector(".t"); t.textContent = mm + ":" + ss; t.classList.toggle("low", s <= 60);
        box.querySelector("[data-act=toggle]").textContent = st.running ? "Pause" : (s === TOTAL ? "Start 15:00" : "Resume");
        // highlight the current step from the elapsed time
        const elapsed = TOTAL - s; let acc = 0;
        box.closest(".slide").querySelectorAll(".tstep").forEach(step => {
          const d = +step.dataset.min * 60, a = acc; acc += d;
          step.classList.toggle("now", (st.running || s < TOTAL) && elapsed >= a && elapsed < acc);
          step.classList.toggle("done", elapsed >= acc);
        });
      });
    }
    function apply(s, remote) { st = s; draw(); if (!remote && chan) chan.postMessage({ type: "timer", state: st }); }
    function toggle() { const s = left(); apply(st.running ? { running: false, endsAt: 0, left: s } : { running: true, endsAt: Date.now() + s * 1000, left: s }); }
    function reset() { apply({ running: false, endsAt: 0, left: TOTAL }); }
    document.addEventListener("click", e => {
      const b = e.target.closest("[data-timer] button"); if (!b) return;
      b.dataset.act === "reset" ? reset() : toggle();
    });
    setInterval(() => { if (st.running) draw(); }, 250);
    draw();
    return { toggle, apply };
  })();

  // ---------- live polls ----------
  (function () {
    if (!window.Poll) return;
    const store = (k, v) => { try { if (v === undefined) return JSON.parse(localStorage.getItem(k) || "null"); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } };
    const key = k => "deck-" + Poll.TOPIC + "-" + k;
    let state = { start: [], end: [] };
    const hidden = new Set(store(key("hidden")) || []);
    function draw() {
      const since = { start: store(key("reset-start")) || 0, end: store(key("reset-end")) || 0 };
      document.querySelectorAll("[data-poll-results=start]").forEach(b => {
        const n = Poll.renderStart(b, state, since.start);
        b.closest(".slide").querySelectorAll(".poll-n b").forEach(x => x.textContent = n);
      });
      document.querySelectorAll("[data-poll-results=end]").forEach(b => {
        const n = Poll.renderEnd(b, state, since.end, hidden, id => { hidden.add(id); store(key("hidden"), [...hidden]); draw(); }, 14);
        b.closest(".slide").querySelectorAll(".poll-n b").forEach(x => x.textContent = n);
      });
    }
    document.querySelectorAll("[data-poll-url]").forEach(a => { a.textContent = Poll.url(a.dataset.pollUrl).replace("https://", ""); a.href = Poll.url(a.dataset.pollUrl); });
    document.addEventListener("click", e => {
      const b = e.target.closest(".poll-tools button"); if (!b) return;
      const p = b.dataset.poll;
      if (b.dataset.act === "reset" && confirm("Hide the answers received so far on this screen? (They stay on the relay; download them first if you need them.)")) { store(key("reset-" + p), Math.floor(Date.now() / 1000)); draw(); }
      if (b.dataset.act === "csv") {
        const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([Poll.toCSV(state)], { type: "text/csv" }));
        a.download = "poll-answers-" + new Date().toISOString().slice(0, 16).replace(/[:T]/g, "-") + ".csv"; a.click();
      }
    });
    Poll.subscribe(s => { state = s; draw(); },
      status => document.querySelectorAll(".poll-status").forEach(x => x.textContent = status === "live" ? "● live" : "reconnecting…"));
  })();

  // ---------- presenter view ----------
  let spNext, spNextStage, spNotes, spSlideNo, spClock, t0 = null;
  function speakerRender() {
    const notes = slides[cur].querySelector("aside.notes");
    spNotes.textContent = notes ? notes.textContent.trim().replace(/\n\s+/g, "\n") : "(no notes)";
    spSlideNo.textContent = (cur + 1) + " / " + N;
    spNextStage.querySelectorAll(":scope > .slide").forEach((s, i) => s.classList.toggle("active", i === cur + 1));
  }
  if (SPEAKER) {
    document.body.classList.add("speaker");
    document.title = "Presenter view · " + document.title;
    const vp = document.querySelector(".viewport");
    const curBox = document.createElement("div"); curBox.className = "sp-box sp-cur";
    curBox.append(stage); vp.append(curBox);
    const side = document.createElement("div"); side.className = "sp-side";
    const nl = document.createElement("p"); nl.className = "sp-label"; nl.textContent = "Next";
    spNext = document.createElement("div"); spNext.className = "sp-box"; spNext.style.aspectRatio = "16 / 9";
    spNextStage = stage.cloneNode(true); spNextStage.querySelectorAll("[data-poll-results], [data-timer]").forEach(x => x.removeAttribute("data-poll-results"));
    spNext.append(spNextStage);
    const meta = document.createElement("div"); meta.className = "sp-meta";
    spSlideNo = document.createElement("span"); spClock = document.createElement("span");
    const rb = document.createElement("button"); rb.textContent = "Reset elapsed"; rb.onclick = () => { t0 = Date.now(); };
    meta.append(spSlideNo, spClock, rb);
    const lab = document.createElement("p"); lab.className = "sp-label"; lab.textContent = "Notes";
    spNotes = document.createElement("div"); spNotes.className = "sp-notes";
    side.append(nl, spNext, meta, lab, spNotes); vp.append(side);
    t0 = Date.now();
    setInterval(() => { const s = Math.floor((Date.now() - t0) / 1000); spClock.textContent = "elapsed " + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0") + "  ·  " + new Date().toTimeString().slice(0, 5); }, 500);
  }
  const resize = () => {
    if (SPEAKER) { fit(stage.parentElement, stage); fit(spNext, spNextStage); }
    else fit(document.querySelector(".viewport"), stage);
  };
  window.addEventListener("resize", resize);
  window.addEventListener("hashchange", () => show(fromHash(), "remote"));
  show(fromHash(), "remote");
  resize();
})();
