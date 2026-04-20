from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

LINKS_FILE = "links.txt"


def load_links() -> dict:
    links = {}
    try:
        with open(LINKS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    short, _, full = line.partition("=")
                    links[short.strip()] = full.strip()
    except FileNotFoundError:
        pass
    return links


@app.get("/")
def home():
    links = load_links()
    rows = "".join(
        f"<tr><td><a href='/{k}'>/{k}</a></td><td>{v}</td></tr>"
        for k, v in links.items()
    )
    html = f"""
    <html>
    <head><title>ahadreports.com links</title></head>
    <body style="font-family:sans-serif;max-width:700px;margin:40px auto;padding:0 20px">
      <h2>ahadreports.com — Short Links</h2>
      <table border="1" cellpadding="8" cellspacing="0" style="width:100%;border-collapse:collapse">
        <tr><th>Short Link</th><th>Destination</th></tr>
        {rows if rows else "<tr><td colspan='2'>No links defined yet.</td></tr>"}
      </table>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/{short_code}")
def redirect(short_code: str):
    links = load_links()
    destination = links.get(short_code)
    if destination:
        return RedirectResponse(url=destination, status_code=301)
    return HTMLResponse(
        f"<h2>404 — No link found for <code>/{short_code}</code></h2>"
        "<p><a href='/'>Back to home</a></p>",
        status_code=404,
    )
