import os
from appcore.app import create_app
from appcore.db import db

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=os.environ.get("is_dev", False))
