import json

import util


class Headers:
    """
    Headers object having fields like ai5(user), debug, random, sdk version
    """

    def __init__(self, ai5, debug, random, sdkv):
        self.ai5 = ai5
        self.debug = debug
        self.random = random
        self.sdkv = sdkv

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_headers(json_string):
        json_ = json.loads(json_string)
        return Headers(**json_)


class Post:
    """
    Post object having information about event
    event -> {"ggstart","ggstop"}
    ts -> timestamp in milli seconds
    """

    def __init__(self, event, ts):
        self.event = event
        self.ts = ts

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_post(json_string):
        json_ = json.loads(json_string)
        return Post(**json_)  # event=json_["event"], ts=json_["ts"]


class Bottle:
    """
    Bottle object having information about game id
    """

    def __init__(self, timestamp, game_id):
        self.timestamp = timestamp
        self.game_id = game_id
        self.timestamp_in_seconds = util.datetime_to_seconds(timestamp)

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_bottle(json_string):
        json_ = json.loads(json_string)
        return Bottle(**json_)


class Instance:
    """
    Instance object is having headers, post and bottle objects
    """

    def __init__(self, headers, post, bottle):
        self.headers = headers
        self.post = post
        self.bottle = bottle

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_instance(json_string):
        json_ = json.loads(json_string)
        headers = Headers.get_headers(json.dumps(json_["headers"]))
        post = Post.get_post(json.dumps(json_["post"]))
        bottle = Bottle.get_bottle(json.dumps(json_["bottle"]))
        return Instance(headers, post, bottle)


class Session:
    """
    Game session object
    """

    def __init__(self, ai5, valid_sessions, total_sessions, avg_session_time):
        self.ai5 = ai5
        self.valid_sessions = valid_sessions
        self.total_sessions = total_sessions
        self.avg_session_time = avg_session_time

    def to_json(self):
        return json.dumps(self.__dict__)
