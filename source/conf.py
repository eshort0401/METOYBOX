# Configuration file for the Sphinx documentation builder.
# First add the project root to the path
import sys
from pathlib import Path
import subprocess
import shutil

print(str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import source._static.utils as utils

# -- Project information

project = "metoybox"
copyright = "2025, Ewan Short"
author = "Ewan Short"

release = "0.0.1"
version = "0.0.1"
numfig = True

math_numfig = True
mathjax3_config = {
    "tex": {
        "tags": "ams",  # auto-number AMS-style
        "useLabelIds": True,  # allow :label: / \label cross refs
    },
    "chtml": {"displayAlign": "center"},
}


# -- General configuration
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.autosectionlabel",
]

autodoc_default_options = {
    "exclude-members": "model_post_init",
    "members": True,
    "private-members": False,
    "undoc-members": True,
    "show-inheritance": True,
}
autosectionlabel_prefix_document = True
autosummary_generate = True
autosummary_ignore_module_all = False

autodoc_pydantic_model_show_json = False
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_field_list_validators = False
autodoc_pydantic_model_show_config_summary = False


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]
html_static_path = ["_static"]
html_extra_path = [".nojekyll"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
# html_logo = "images/logo_white.svg"

# -- Options for EPUB output
epub_show_urls = "footnote"
html_baseurl = "https://eshort0401.github.io/METOYBOX/"

html_css_files = [
    "assets/css/base.css",
    "assets/css/controls.css",
    "https://pyscript.net/releases/2024.1.1/core.css",
]

html_js_files = [
    ("https://pyscript.net/releases/2024.1.1/core.js", {"type": "module"}),
    "assets/js/model-controls.js", 
]


_parent = Path(__file__).resolve().parents[1]


def _should_rebuild_wheel():
    """Check if wheel needs rebuilding based on timestamps."""
    dist_dir = _parent / "dist"
    wheel_files = list(dist_dir.glob("metoybox-*.whl"))
    if not wheel_files:
        return True

    latest_wheel = max(wheel_files, key=lambda p: p.stat().st_mtime)
    wheel_time = latest_wheel.stat().st_mtime

    # Check if any Python file in metoybox is newer than the wheel
    metoybox_dir = _parent / "metoybox"
    for py_file in metoybox_dir.rglob("*.py"):
        if py_file.stat().st_mtime > wheel_time:
            return True

    return False


def setup(app):
    """Setup function for Sphinx."""
    # Build the metoybox wheel
    if _should_rebuild_wheel():
        print("Building metoybox wheel...")
        subprocess.run(["python", "-m", "build"], cwd=_parent, check=True)
        dist_directory = _parent / "dist"
        wheel_files = list(dist_directory.glob("metoybox-*-py3-none-any.whl"))
        if wheel_files:
            latest_wheel = max(wheel_files, key=lambda p: p.stat().st_mtime)
            dest = _parent / "source" / "_static" / "assets" / latest_wheel.name
            shutil.copy2(latest_wheel, dest)
            print(f"Copied {latest_wheel.name} to {dest}")
    else:
        print("Wheel is up to date; skipping build.")

    # Build the html snippets for each model from the js stubs
    stub_directory = _parent / "source" / "_static"
    utils.generate_all_html(stub_directory)
