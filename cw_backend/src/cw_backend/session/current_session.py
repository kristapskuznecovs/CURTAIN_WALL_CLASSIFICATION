import time

current_session = {"time": 0,
                   "id": None}


def session_valid(session):
    time_now = int(time.time())
    time_difference = time_now - current_session['time']
    if current_session['id'] is None:
        current_session['id'] = session
        current_session['time'] = time_now
        return True
    elif session == current_session['id']:
        current_session['time'] = time_now
        return True
    elif 0 < time_difference < 300:
        return False
    else:
        current_session['id'] = session
        current_session['time'] = int(time.time())
        return True
