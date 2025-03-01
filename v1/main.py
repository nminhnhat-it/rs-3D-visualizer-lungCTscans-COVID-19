from src.app import App
import sys

def main():
    app = App(sys.argv)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
