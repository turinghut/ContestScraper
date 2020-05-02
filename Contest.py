class Contest:
    contestCode = ''
    contestName = ''
    platform = ''
    startDateTime = ''
    endDateTime = ''
    def __init__(self,contestCode,contestName,platform,startDateTime,endDateTime):
        self.contestCode = contestCode
        self.contestName = contestName
        self.platform = platform
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime