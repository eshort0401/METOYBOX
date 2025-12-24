from js import document

def initialize_from_controllers(model):
    """Convenience function to initialize model variables from controller sliders."""

    script = document.currentScript
    container_id = script.getAttribute('data-container-id')
    print(container_id)

    # Read initial values from the sliders
    for var_type in ["non_dimensional_variables", "dimensional_variables"]:
        var_dict = getattr(model, var_type)
        for var in var_dict.keys():
            slider = document.getElementById(f"{container_id}-{var}-slider")
            if slider:
                var_dict[var] = float(slider.value)
