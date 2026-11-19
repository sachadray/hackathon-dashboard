"""QR codes for the deck and the handout: python build/make_qr.py (needs: pip install segno)."""
from pathlib import Path
import segno

BASE = "https://sachadray.github.io/hackathon-dashboard/"
OUT = Path(__file__).resolve().parent.parent / "docs" / "assets"
for name, url in {"poll-start": BASE + "poll.html?p=start", "poll-end": BASE + "poll.html?p=end",
                  "handout": BASE + "handout.html", "deck": BASE}.items():
    segno.make(url, error="m").save(OUT / f"qr-{name}.svg", scale=10, border=2, dark="#0E1B2C", light="#F6F4EE")
    print(name, url)
