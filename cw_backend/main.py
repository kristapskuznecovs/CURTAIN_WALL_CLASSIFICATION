import ProcessFile
import FlaskApp

"""
web - set to True for default use together with React
    - set to False to run in Python console for debug purposes
"""
web = True

if __name__ == '__main__':
    if web:
        FlaskApp.app.run()
    else:
        result = ProcessFile.process_files("GeelyError1.csv")
        print('Finished')
