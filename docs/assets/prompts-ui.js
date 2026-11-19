/* Render prompt cards (with a Copy button) on the handout and prompts pages.
 * The prompt text comes from window.PROMPTS, which build/build_site.py embeds
 * from the files in prompts/. Everything is inserted as text, never as HTML,
 * except the tiny markdown subset below, which escapes first. */
(function () {
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  // **bold**, `code`, <https://link>
  function md(s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/&lt;(https:\/\/[^&\s]+)&gt;/g, '<a href="$1">$1</a>');
  }
  function paragraphs(s) {
    return s.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean).map(p => "<p>" + md(p.replace(/\n/g, " ")) + "</p>").join("");
  }
  async function copy(text, btn) {
    try { await navigator.clipboard.writeText(text); }
    catch (e) { const ta = document.createElement("textarea"); ta.value = text; document.body.append(ta); ta.select(); document.execCommand("copy"); ta.remove(); }
    btn.textContent = "Copied"; btn.classList.add("done");
    setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("done"); }, 1600);
  }
  function card(p, label) {
    const box = document.createElement("div"); box.className = "prompt";
    if (label) { const h = document.createElement("div"); h.className = "head"; h.textContent = label; box.append(h); }
    const pre = document.createElement("pre"); pre.textContent = p.text;
    const b = document.createElement("button"); b.className = "copy"; b.type = "button"; b.textContent = "Copy";
    b.setAttribute("aria-label", "Copy prompt: " + p.title);
    b.addEventListener("click", () => copy(p.text, b));
    box.append(pre, b);
    return box;
  }
  const find = (set, id) => (window.PROMPTS[set].prompts.find(p => p.id === id));
  window.PromptsUI = { card, find, md, paragraphs };
})();
