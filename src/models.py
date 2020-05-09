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
