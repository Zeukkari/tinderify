import time

def get_unix_time(source_time):
        return time.mktime(source_time.timetuple())
