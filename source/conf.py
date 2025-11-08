# Configuration file for the Sphinx documentation builder.
# First add the project root to the path
import sys
from pathlib import Path
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

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


# autodoc_mock_imports = [
#     "numba",
#     "scipy",
#     "scikit-image",
#     "cartopy",
#     "typing_extensions",
#     "codecov",
#     "netcdf4",
#     "h5netcdf",
#     "requests",
#     "tqdm",
#     "cdsapi",
#     "xesmf",
#     "skimage",
#     "cv2",
#     "nco",
#     "pytables",
#     "zarr",
#     "windrose",
#     "pydot",
#     "metpy",
#     "graphviz",
#     "pygraphviz",
#     "nbconvert",
#     "networkx",
#     "imageio",
# ]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]
html_static_path = ["_static"]
html_extra_path = [".nojekyll", "_static"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
# html_logo = "images/logo_white.svg"

# -- Options for EPUB output
epub_show_urls = "footnote"
html_baseurl = "https://eshort0401.github.io/METOYBOX/"


def setup(app):
    def copy_metoybox_to_build(app, docname, source):
        # Only run once during the build (not for every document)
        if not hasattr(app.env, "_metoybox_copied"):
            # Path to your metoybox code (outside source)
            repo_root = Path(__file__).resolve().parents[1]
            metoybox_src = repo_root / "metoybox"

            # Destination in the built output
            build_dir = Path(app.outdir)  # This is _build/html
            metoybox_dst = build_dir / "metoybox"

            # Only copy if source exists
            if metoybox_src.exists():
                # Ensure _static directory exists in build output
                metoybox_dst.parent.mkdir(parents=True, exist_ok=True)

                # Remove old copy if it exists
                if metoybox_dst.exists():
                    shutil.rmtree(metoybox_dst)

                # Copy the whole folder
                shutil.copytree(metoybox_src, metoybox_dst)
                print(f"Copied {metoybox_src} to {metoybox_dst}")

                # Mark as done so we don't copy multiple times
                app.env._metoybox_copied = True
            else:
                print(f"Source directory {metoybox_src} does not exist. Skipping copy.")

    # Connect to the source-read event (runs early in the build)
    app.connect("source-read", copy_metoybox_to_build)
