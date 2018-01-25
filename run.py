import subprocess
import sys
import os

FLASK_EXEC = 'flask'

os.environ['FLASK_APP'] = os.path.abspath('app.py')
subprocess.Popen(['flask', 'run']).wait()
