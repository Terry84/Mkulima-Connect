import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    debug_flag = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_flag)
