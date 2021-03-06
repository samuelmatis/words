from users import *
from auth import *
from words import *
from test import *
from flask import session, render_template
import os

# Route for homepage
@app.route('/')
def index():
    if 'email' in session:
        return render_template("index.html")
    else:
        return render_template("home.html")

# secret key for sessions
app.secret_key = os.urandom(24)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    # Start app
    app.run(host='0.0.0.0', port=port, debug=True)
