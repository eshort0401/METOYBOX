# Remove docs and regenerate using sphinx
rm -rf docs && sphinx-build -b html source docs

# Initiate server with python
python -m http.server --directory docs 8000