from os import path
import os
from eve import Eve

SETTINGS_PATH = path.join(path.dirname(os.path.abspath(__file__)), 'settings.py')

app = Eve(settings=SETTINGS_PATH)

if __name__ == '__main__':
    app.run()
