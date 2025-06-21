from app import app

"""
this file is being used by gunicorn production's server
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0')
