from dateutil import parser


class Contest:
    contestCode = ''
    contestName = ''
    platform = ''
    startDateTime = ''
    endDateTime = ''
    id = ''

    def __init__(self, contestCode, contestName, platform, startDateTime, endDateTime, id):
        self.contestCode = contestCode
        self.contestName = contestName
        self.platform = platform
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.id = id

    @classmethod
    def fromJson(cls, contestJson):
        return cls(contestJson['code'], contestJson['name'], contestJson['platform'], parser.parse(contestJson['start_time']), parser.parse(contestJson['end_time']), contestJson['id'])
