Mountain Valley Breeze Test
=======================================

Introductory paragraph. Some math :math:`E = mc^2`.

.. raw:: html

   <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css" />
    <link rel="stylesheet" href="assets/css/mathjax.css" />
    <link rel="stylesheet" href="assets/css/base.css" />
    <link rel="stylesheet" href="assets/css/controls.css" />
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
    <script src="assets/js/mathjax-config.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

   <div id="loading-screen">
    <div class="spinner"></div>
    <p>Loading...</p>
    <p><small>This can take a few minutes!</small></p>
  </div>

    <div id="main-content">
      <div id="figure-output"></div>
      <div id="controls"></div>
      <script src="assets/js/model-controls.js"></script>
      <script>
        const configs = coreWaveConfigs();
        // Add an imshow selection control row above the sliders
        const imshow_sel_config = imshowSelectionConfig();
        configs.unshift(imshow_sel_config);
        const MStep = 3 * stepRatio
        const MDimMax = 1e-2
        const MDimStep = MDimMax * stepRatio
        let args = ["\\(M:\\)", "M-slider", 0, 3, 0.2, MStep, "non-dimensional"];
        configs.push(sliderConfig(...args));
        args = ["\\(M:\\)", "M_dim-slider", 0, MDimMax, Omega * 1e2, MDimStep]
        args.push("dimensional", "m m⁻¹");
        configs.push(sliderConfig(...args));
        createModelControls(configs, "controls");
      </script>
      <py-script src="mountain_valley_test.py" config="assets/pyscript.toml"></py-script>
    </div>

Some more text.
This is after the raw HTML block.