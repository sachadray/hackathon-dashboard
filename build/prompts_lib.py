"""Read the prompt files in prompts/ into plain Python data.

Each file is markdown. Text before the first "## " heading is the file's intro.
Each prompt is a "## id | track | step | title" heading, optional paragraphs, and
one fenced block holding the prompt text itself.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEAD = re.compile(r"^## (?P<id>[\w-]+) \| (?P<track>\w+) \| (?P<step>\d+) \| (?P<title>.+)$")


def read_file(name):
    text = (ROOT / "prompts" / name).read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = text.splitlines()
    title, intro, prompts, cur = "", [], [], None
    in_code, buf = False, []
    for line in lines:
        if line.startswith("```"):
            if in_code:
                cur["text"] = "\n".join(buf).strip("\n")
                buf, in_code = [], False
            else:
                in_code = True
            continue
        if in_code:
            buf.append(line)
            continue
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        m = HEAD.match(line)
        if m:
            cur = dict(m.groupdict(), step=int(m["step"]), note="", text="")
            prompts.append(cur)
            continue
        if cur is None:
            intro.append(line)
        elif line.strip():
            cur["note"] = (cur["note"] + " " + line.strip()).strip()
    return {"title": title, "intro": "\n".join(intro).strip(), "prompts": prompts}


def all_prompts():
    return {k: read_file(f"{k}.md") for k in ["handson", "replicate-land", "replicate-pfm", "claude-code"]}


if __name__ == "__main__":
    for k, v in all_prompts().items():
        print(k, "|", v["title"], "|", [(p["id"], len(p["text"])) for p in v["prompts"]])
