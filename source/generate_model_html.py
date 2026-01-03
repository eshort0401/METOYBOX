import glob
from pathlib import Path

# Note we wrap in a container div and scope js to allow multiple models on one page
_div_open = """<div id="{container_id}">
    <div id="loading-screen">
        <div class="spinner"></div>
        <p>Loading...</p>
        <p><small>This can take a few minutes!</small></p>
    </div>
    <div id="main-content">
        <div id="figure-output">
            <!-- Use two layers to prevent flickering in firefox -->
            <div id="{container_id}-figure-output-A" class="figure-layer is-active"></div>
            <div id="{container_id}-figure-output-B" class="figure-layer is-passive"></div>
        </div>
        <div id="controls"></div>
        <script>
"""

_div_close = """
        </script>
        <py-script 
            src="{python_path}" 
            config="{config_path}"
            data-container-id="{container_id}">
        </py-script>
    </div>
</div>"""


def generate_html(
    stub_path,
    html_path=None,
    python_path=None,
    config_path="/METOYBOX/_static/assets/pyscript.toml",
    local_parent=None,
    container_id=None,
):
    """Generate the full HTML for a given js stub."""
    with open(stub_path, "r") as stub_file:
        stub = stub_file.read()
    if html_path is None:
        html_path = stub_path.replace(".js", ".html")
    # Ensure the output directory exists
    Path(html_path).parent.mkdir(parents=True, exist_ok=True)
    if local_parent is None:
        local_parent = Path(__file__).parent
    web_parent = Path("/METOYBOX/_static")
    # Assume python file in same directory as javascript stub
    python_path = stub_path.replace(".js", ".py")
    # Now convert to web path
    python_path = str(web_parent / Path(python_path).relative_to(local_parent))

    if container_id is None:
        # Use the filename without extension as container id
        container_id = Path(stub_path).stem

    div_open = _div_open.format(container_id=container_id)
    div_close = _div_close.format(
        python_path=python_path, config_path=config_path, container_id=container_id
    )

    # Wrap the stub in a function to scope it to the container and indent appropriately
    stub_lines = stub.splitlines()
    indented_stub_content = "\n".join(["    " + line for line in stub_lines])
    wrapped_stub = f"(function(containerID) {{\n{indented_stub_content}\n}})('{container_id}');"
    indented_stub = "\n".join(["            " + line for line in wrapped_stub.splitlines()])

    with open(html_path, "w") as f:
        # f.write(_header)
        f.write(div_open)
        f.write(indented_stub)
        f.write(div_close)


def generate_all_html(stub_directory=None, local_parent=None):
    """Generate HTML files for all JS stubs in this directory."""
    if stub_directory is None:
        stub_directory = Path(__file__).parent / "_static/models"
    if local_parent is None:
        local_parent = Path(__file__).parent / "_static"
    js_stubs = glob.glob(str(stub_directory / "**/*.js"), recursive=True)
    for js_stub in js_stubs:
        generate_html(js_stub, local_parent=local_parent)


if __name__ == "__main__":
    generate_all_html()
