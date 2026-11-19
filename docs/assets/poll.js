/* Live poll for the session, with no account and no server of our own.
 *
 * Answers are posted to a topic on ntfy.sh, a free public relay that keeps
 * messages for 12 hours and lets any page read them back (it sends the CORS
 * headers browsers need). The deck subscribes to the same topic and redraws as
 * answers arrive.
 *
 * Anyone who knows the topic name can read or post to it, so: answers are
 * anonymous, every message is validated before it is counted, text is shown
 * with textContent only, and the presenter can hide an answer on their screen.
 *
 * Rehearse with ?topic=any-other-name on both the poll page and the deck, so
 * test answers never reach the real topic.
 */
(function () {
  const params = new URLSearchParams(location.search);
  const TOPIC = (params.get("topic") || "vietleap-dash-2026-k7q3mx").replace(/[^A-Za-z0-9_-]/g, "");
  const RELAY = "https://ntfy.sh/";
  const BASE = "https://sachadray.github.io/hackathon-dashboard/";

  const POLLS = {
    start: {
      title: "Before we start",
      questions: [
        { id: "ai", text: "How often do you use AI tools (ChatGPT, Claude, Gemini…) for your studies?",
          options: ["Never", "A few times a month", "Every week", "Every day"] },
        { id: "dash", text: "Have you ever built a dashboard (in Excel, Power BI, Tableau or code)?",
          options: ["Never", "Once, for a class", "A few times", "Often, for work or projects"] },
        { id: "git", text: "Have you used GitHub or another version-control tool?",
          options: ["Never heard of it", "Heard of it, never used it", "Used it a few times", "I use it regularly"] },
      ],
    },
    end: {
      title: "Before you go",
      questions: [
        { id: "learned", text: "What is one thing you learned today?", open: true },
        { id: "impression", text: "Your impressions: what worked, and what would you change?", open: true },
      ],
    },
  };
  const MAXLEN = 280;

  // one id per browser, so a student who answers twice replaces their answer
  function deviceId() {
    try {
      let id = localStorage.getItem("poll-device");
      if (!id) { id = Math.random().toString(36).slice(2, 10); localStorage.setItem("poll-device", id); }
      return id;
    } catch (e) { return Math.random().toString(36).slice(2, 10); }
  }

  // keep only well-formed answers to known questions
  function clean(raw) {
    let m;
    try { m = typeof raw === "string" ? JSON.parse(raw) : raw; } catch (e) { return null; }
    if (!m || m.v !== 1 || !POLLS[m.p] || typeof m.id !== "string" || !m.a || typeof m.a !== "object") return null;
    const out = { p: m.p, id: m.id.slice(0, 16), a: {} };
    for (const q of POLLS[m.p].questions) {
      const v = m.a[q.id];
      if (typeof v !== "string") continue;
      if (q.open) { const t = v.trim().slice(0, MAXLEN); if (t) out.a[q.id] = t; }
      else if (q.options.includes(v)) out.a[q.id] = v;
    }
    return Object.keys(out.a).length ? out : null;
  }

  async function submit(p, answers) {
    const body = JSON.stringify({ v: 1, p, id: deviceId(), a: answers });
    for (let i = 0; i < 4; i++) {
      try {
        const r = await fetch(RELAY + TOPIC, { method: "POST", body });
        if (r.ok) return true;
        if (r.status !== 429 && r.status < 500) return false;
      } catch (e) { /* network error: retry */ }
      await new Promise(res => setTimeout(res, 1500 * (i + 1)));
    }
    return false;
  }

  /* Subscribe to every answer kept on the relay, then new ones as they come.
   * onChange(state) receives { start: [...], end: [...] }: one entry per
   * device for multiple-choice polls (latest wins), and every message for the
   * open questions. Returns a function that stops the subscription. */
  function subscribe(onChange, onStatus) {
    const seen = new Set(), latest = { start: new Map(), end: [] };
    let es = null, stopped = false, timer = null;
    const emit = () => onChange({ start: [...latest.start.values()], end: latest.end.slice() });
    function handle(ev) {
      let msg; try { msg = JSON.parse(ev.data); } catch (e) { return; }
      if (msg.event !== "message" || seen.has(msg.id)) return;
      seen.add(msg.id);
      const m = clean(msg.message); if (!m) return;
      m.time = msg.time; m.mid = msg.id;
      if (m.p === "start") {
        const prev = latest.start.get(m.id);
        if (!prev || prev.time <= m.time) latest.start.set(m.id, m);
      } else latest.end.push(m);
      clearTimeout(timer); timer = setTimeout(emit, 150);
    }
    function open() {
      if (stopped) return;
      es = new EventSource(RELAY + TOPIC + "/sse?since=all");
      es.onmessage = handle;
      es.onopen = () => onStatus && onStatus("live");
      es.onerror = () => { onStatus && onStatus("reconnecting"); };
    }
    open(); emit();
    return () => { stopped = true; es && es.close(); };
  }

  // spreadsheet of every answer currently held by the relay
  function toCSV(state) {
    const rows = [["poll", "device", "time_utc", "question", "answer"]];
    const iso = t => new Date(t * 1000).toISOString();
    for (const p of ["start", "end"]) for (const m of state[p]) for (const [q, a] of Object.entries(m.a)) rows.push([p, m.id, iso(m.time), q, a]);
    return rows.map(r => r.map(x => '"' + String(x).replace(/"/g, '""') + '"').join(",")).join("\n");
  }

  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };

  // multiple choice: one block per question, one bar per option (count and share)
  function renderStart(box, state, since) {
    const rows = state.start.filter(m => !since || m.time >= since);
    box.replaceChildren();
    for (const q of POLLS.start.questions) {
      const block = h("div", "pr-q"), counts = q.options.map(o => rows.filter(m => m.a[q.id] === o).length);
      const n = counts.reduce((a, b) => a + b, 0);
      block.append(h("p", "pr-qtext", q.text));
      q.options.forEach((o, i) => {
        const row = h("div", "pr-row"), bar = h("div", "pr-bar"), fill = h("div", "pr-fill");
        fill.style.width = (n ? 100 * counts[i] / n : 0) + "%";
        bar.append(fill);
        row.append(h("span", "pr-opt", o), bar, h("span", "pr-n", n ? Math.round(100 * counts[i] / n) + "% · " + counts[i] : "–"));
        block.append(row);
      });
      box.append(block);
    }
    return rows.length;
  }

  // open questions: a wall of answers per question, newest first; click hides one
  function renderEnd(box, state, since, hidden, onHide, limit) {
    const rows = state.end.filter(m => (!since || m.time >= since));
    box.replaceChildren();
    let total = 0;
    for (const q of POLLS.end.questions) {
      const col = h("div", "pr-col"), items = rows.filter(m => m.a[q.id] && !(hidden && hidden.has(m.mid + q.id))).sort((a, b) => b.time - a.time);
      total = Math.max(total, rows.filter(m => m.a[q.id]).length);
      col.append(h("p", "pr-qtext", q.text + " (" + items.length + ")"));
      const wall = h("div", "pr-wall");
      items.slice(0, limit || 999).forEach(m => {
        const card = h("p", "pr-card", m.a[q.id]);
        if (onHide) { card.title = "Click to hide on this screen"; card.addEventListener("click", () => onHide(m.mid + q.id)); }
        wall.append(card);
      });
      if (!items.length) wall.append(h("p", "pr-empty", "Waiting for answers…"));
      col.append(wall); box.append(col);
    }
    return total;
  }

  window.Poll = { TOPIC, BASE, POLLS, MAXLEN, submit, subscribe, toCSV, clean, renderStart, renderEnd,
    url: p => BASE + "poll.html?p=" + p + (params.get("topic") ? "&topic=" + TOPIC : "") };
})();
