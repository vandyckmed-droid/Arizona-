"""Bundle web/index.html + web/data.json into one self-contained page.

The repo UI fetches data.json, which needs a local server. This inlines the
data so the page can be opened straight from a file or a static host.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "screener", "standalone.html")
DATA = os.path.join(ROOT, "web", "data.json")


def main(out):
    with open(TEMPLATE) as fh:
        html = fh.read()
    with open(DATA) as fh:
        data = fh.read()
    # </script> inside a script block would close it early
    payload = data.replace("</", "<\\/")
    html = html.replace("/*__DATA__*/null", payload)
    with open(out, "w") as fh:
        fh.write(html)
    print(f"wrote {out} ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "web", "standalone.html"))
