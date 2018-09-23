import platform
if platform.system() == 'Windows':
    import os
    import sys

    activate_this = f'{os.path.dirname(__file__)}/venv/Scripts/activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

    sys.path.append(os.path.dirname(__file__))


from app import app as application

if __name__ == '__main__':
    application.run()
