class MockCore:
    def __init__(self):
        pass

from main_window import MainWindow

if __name__ == "__main__":
    mock_core = MockCore()
    app = MainWindow(mock_core)
    app.run()