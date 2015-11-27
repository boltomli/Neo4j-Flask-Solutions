import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from asset import app

app.secret_key = os.urandom(24)
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
