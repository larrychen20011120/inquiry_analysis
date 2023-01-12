import os

class Config:
    pjdir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(pjdir, 'app.db')
    SECRET_KEY = 'hard to guess string'
    SESSION_PROTECTION = 'strong'
    ENTRY = os.path.join(pjdir, 'app')
    ALLOWED_EXTENSIONS = set(['m4a', 'wav', 'mp3'])
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024    # 20MB for maximum

    # API KEY FILL IN HERE!!
    PYANNOTE_AUDIO_KEY = "YOUR KEY"
    AZURE_KEY = "YOUR KEY"
    AZURE_REGION = "YOUR KEY"
    IMGUR_KEY = 'YOUR KEY'
    WMMKS_NER_KEY = "YOUR KEY"
    CHINESE_FONT_URL = "YOUR DIRECTORY(.otf)"
