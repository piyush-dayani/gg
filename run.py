from optparse import OptionParser

import util


def parser():
    parser_ = OptionParser()
    parser_.add_option("-f", "--file", dest="file", help="data set location", metavar="FILE")
    parser_.add_option("-o", "--output", dest="output", help="output file", metavar="FILE")
    return parser_.parse_args()


if __name__ == '__main__':
    (options, args) = parser()
    user_instances, game_instances = util.read_json(options.file)
    sessions = util.game_sessions(user_instances)
    with open(options.output, "w") as fp:
        for session in sessions:
            fp.write(session.to_json() + "\n")
