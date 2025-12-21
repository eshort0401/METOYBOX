import glob
from pathlib import Path

_header = """<link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css" />
<link rel="stylesheet" href="/METOYBOX/_static/assets/css/base.css" />
<link rel="stylesheet" href="/METOYBOX/_static/assets/css/controls.css" />
<script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>

<div id="loading-screen">
    <div class="spinner"></div>
    <p>Loading...</p>
    <p><small>This can take a few minutes!</small></p>
</div>
"""

_div_open = """
<div id="main-content">
    <div id="figure-output">
        <!-- Use two layers to prevent flickering in firefox -->
        <div id="figure-output-A" class="figure-layer is-active"></div>
        <div id="figure-output-B" class="figure-layer is-passive"></div>
    </div>
    <div id="controls"></div>
    <script src="/METOYBOX/_static/assets/js/model-controls.js"></script>
    <script>
"""

_div_close = """
    </script>
    <py-script src="{python_path}" config="{config_path}"></py-script>
</div>"""


def generate_html(
    stub_path,
    html_path=None,
    python_path=None,
    config_path="/METOYBOX/_static/assets/pyscript.toml",
    local_parent=None,
):
    """Generate the full HTML for a given js stub."""
    with open(stub_path, "r") as stub_file:
        stub = stub_file.read()
    if html_path is None:
        html_path = stub_path.replace(".js", ".html")
    # Ensure the output directory exists
    Path(html_path).parent.mkdir(parents=True, exist_ok=True)
    # filename = Path(stub_path).name
    if local_parent is None:
        local_parent = Path(__file__).parent
    web_parent = Path("/METOYBOX/_static")
    # Assume python file in same directory as javascript stub
    python_path = stub_path.replace(".js", ".py")
    # Now convert to web path
    python_path = str(web_parent / Path(python_path).relative_to(local_parent))

    div_close = _div_close.format(python_path=python_path, config_path=config_path)

    indented_stub = "\n".join(["        " + line for line in stub.splitlines()])
    with open(html_path, "w") as f:
        f.write(_header)
        f.write(_div_open)
        f.write(indented_stub)
        f.write(div_close)


def generate_all_html(stub_directory=None):
    """Generate HTML files for all JS stubs in this directory."""
    if stub_directory is None:
        stub_directory = Path(__file__).parent
    js_stubs = glob.glob(str(stub_directory / "*.js"))
    for js_stub in js_stubs:
        generate_html(js_stub)


if __name__ == "__main__":
    generate_all_html()
