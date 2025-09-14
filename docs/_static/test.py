from pyscript import when, display, document


# Add this to your mountain_valley.py for testing:
class SimpleTestController:

    def __init__(self):
        self._register_handlers()

    def _register_handlers(self):
        @when("click", "#test-btn")
        def _test_handler(event):
            self.test_handler(event)

    def test_handler(self, event):
        print("SUCCESS: Class method @when decorator works!")
        display("Event handler fired from class method!", target="output")


def hide_loading_screen():
    """Hide loading screen and show main content"""
    loading_screen = document.getElementById("loading-screen")
    main_content = document.getElementById("main-content")

    loading_screen.style.display = "none"
    main_content.style.display = "block"


# Instantiate it:
test_controller = SimpleTestController()
hide_loading_screen()
