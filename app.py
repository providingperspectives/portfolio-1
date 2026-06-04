import os
from flask import Flask
from views import main

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)