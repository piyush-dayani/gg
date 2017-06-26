import datetime
import time

from model import *


def read_json(file):
    user_map = {}
    game_map = {}
    with open(file) as infile:
        lines = infile.readlines()
    for line in lines:
        instance = Instance.get_instance(line)
        users_instances = user_map.get(instance.headers.ai5, [])
        game_instances = game_map.get(instance.bottle.game_id, [])
        users_instances.append(instance)
        game_instances.append(instance)
        user_map[instance.headers.ai5] = users_instances
        game_map[instance.bottle.game_id] = game_instances
    return user_map, game_map


def game_sessions(user_instances):
    sessions = []
    for ai5, instances in user_instances.items():
        instances.sort(key=lambda x: x.bottle.timestamp_in_seconds)
        flag = True
        start = None  # start instance of session(ggstart)
        previous = None  # previous instance to current instance of session
        end = None  # last instance of session(ggstop)
        total_sessions = 0  # total number of sessions per user
        valid_sessions = 0  # total number of valid sessions
        total_time = 0  # total time including all sessions
        for instance in instances:
            # handling premier failures(ggstop in the beginning)
            if flag:
                if instance.post.event == "ggstart":
                    previous = start = instance
                    flag = False
                continue
            diff = instance.bottle.timestamp_in_seconds - previous.bottle.timestamp_in_seconds
            # if valid ggstop encountered then end is this instance
            if previous.post.event == "ggstart" and instance.post.event == "ggstop":
                previous = end = instance
            elif diff > 30:  # more than 30 secs session is to be considered different
                if previous.post.event == instance.post.event == "ggstop":
                    flag = True
                elif previous.post.event == "ggstop" and instance.post.event == "ggstart":
                    previous = start = instance
                elif previous.post.event == "ggstart" and instance.post.event == "ggstart":
                    previous = start = instance
                if end:
                    session_time = end.bottle.timestamp_in_seconds - start.bottle.timestamp_in_seconds
                # checking whether session is valid or not
                if session_time >= 60:
                    valid_sessions += 1
                    total_time += session_time
                # checking whether session to ignore or not
                if session_time > 1:
                    total_sessions += 1
        sessions.append(
            Session(ai5, valid_sessions, total_sessions, (total_time / valid_sessions) if valid_sessions != 0 else 0))
    return sessions


def datetime_to_seconds(time_):
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    strptime = datetime.datetime.strptime(time_, datetime_format)
    return int(time.mktime(strptime.timetuple()))
