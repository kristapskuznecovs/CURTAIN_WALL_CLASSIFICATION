import ProcessFile
import FlaskApp

import os

"""
web - set to True for default use together with React
    - set to False to run in Python console for debug purposes
"""
web = False

current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    if web:
        FlaskApp.set_current_directory(current_dir)
        FlaskApp.app.run()
    else:
        result = ProcessFile.process_files("Geely2.csv")
        print('Finished')
