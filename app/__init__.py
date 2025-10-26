from flask import Flask


app = Flask(__name__)

# Import routes to register URL handlers on the `app` instance
from . import routes  # noqa: F401,E402


if __name__ == '__main__':
    app.run(debug=True)