"""Entry point Moodify. Jalankan dengan: python app.py"""
from moodify import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
