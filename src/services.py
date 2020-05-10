from datetime import datetime, timedelta
from dateutil import parser
# from .models import Contest
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup as bs
import requests as req

from src.models import Contest


class ImageGenerator:
    fontDirectory = "src/resources/fonts/RobotoBlack.ttf"
    storyTemplateDirectory = "src/resources/templates/storyTemplate.jpg"

    def generateImage(self, contest):
        MAX_W = 1080
        font = ImageFont.truetype(self.fontDirectory, 50)
        count = 0
        image = Image.open(self.storyTemplateDirectory)
        draw = ImageDraw.Draw(image)
        w, h = font.getsize("Platform : " + contest.platform)
        draw.text((((MAX_W - w) / 2), 900), "Platform : " +
                  contest.platform, fill="white", font=font, align="center")
        w, h = font.getsize("Contest code : " + contest.contestCode)
        draw.text((((MAX_W - w) / 2), 1000), "Contest code : " +
                  contest.contestCode, fill="white", font=font, align="center")
        font = ImageFont.truetype(self.fontDirectory, 70)
        w, h = font.getsize(contest.contestName)
        draw.text((((MAX_W - w) / 2), 1150), contest.contestName,
                  fill="white", font=font, align="center")
        font = ImageFont.truetype(self.fontDirectory, 50)
        draw.text((150, 1300), "START : ",
                  fill="white", font=font, align="left")
        timeDifference = contest.endDateTime - contest.startDateTime
        contest.startDateTime = str(
            contest.startDateTime.strftime('%d-%m-%Y %H:%M:%S'))
        contest.endDateTime = str(
            contest.endDateTime.strftime('%d-%m-%Y %H:%M:%S'))
        draw.text((400, 1300), contest.startDateTime,
                  fill="white", font=font, align="left")
        draw.text((150, 1400), "END : ", fill="white",
                  font=font, align="right")
        draw.text((400, 1400), contest.endDateTime,
                  fill="white", font=font, align="right")
        #timeDifference = datetime.datetime.strptime(contest.endDateTime, '%y-%m-%d %H:%M:%S') - datetime.datetime.strptime(contest.startDateTime, '%y-%m-%d %H:%M:%S')
        secondsTaken = timeDifference.total_seconds()
        hours = divmod(secondsTaken, 3600)[0]
        secondsTaken = timeDifference.total_seconds()
        days = divmod(secondsTaken, 86400)[0]
        if(int(hours) > 24):
            duration = str(int(days)) + " Days"
        else:
            duration = str(int(hours)) + " Hours"
        w, h = font.getsize("DURATION : " + duration)
        draw.text((((MAX_W - w) / 2), 1500), "DURATION : " +
                  str(duration), fill="white", font=font, align="right")
        # image.save(self.saveLocation + "Image-" + str(count) + ".png")
        count += 1
        return image


class ContestsRetreiver:
    def getContestDetails(self):
        # 2020-05-11 15:00:00
        contestsJson = []
        codechefContests = self.getContestsfromCodechef()
        for contest in codechefContests:
            if(datetime.now().date() == parser.parse(contest['start_time']).date()):
                contestsJson.append(contest)
        codeforcesContests = self.getContestsfromCodeforces()
        for contest in codeforcesContests:
            if(datetime.now().date() == parser.parse(contest['start_time']).date()):
                contestsJson.append(contest)

        return contestsJson

    def getContestsfromCodechef(self):
        URL = "https://www.codechef.com/contests"
        soup = bs(req.get(URL).content, 'lxml')
        allTables = soup.find_all('table', attrs={'class': 'dataTable'})
        presentTables = allTables[0]  # Present table is the first one
        contests = []
        allRows = presentTables.find_all('tr')
        for row in allRows:
            contest = {}
            strippedData = []
            datas = row.find_all('td')
            for data in datas:
                strippedData.append(data.text.strip())
            if(len(strippedData) == 4):
                startDate = datetime.strptime(
                    strippedData[2], "%d %b %Y  %H:%M:%S")
                endDate = datetime.strptime(
                    strippedData[3], "%d %b %Y  %H:%M:%S")
                contest['code'] = strippedData[0]
                contest['name'] = strippedData[1]
                contest['start_time'] = str(startDate)
                contest['end_time'] = str(endDate)
                contest['duration'] = str(endDate - startDate)
                contest['resource'] = "codechef"
                contest['id'] = "codechef_"+strippedData[0]
                contests.append(contest)
        return contests

    def getContestsfromCodeforces(self):
        URL = "http://codeforces.com/contests"
        soup = bs(req.get(URL).content, 'lxml')
        allTables = soup.find_all('div', attrs={'class': 'datatable'})
        presentTables = allTables[0]  # Present table is the first one
        contests = []
        allRows = presentTables.find_all('tr')
        for row in allRows:
            contest = {}
            strippedData = []
            datas = row.find_all('td')
            for data in datas:
                strippedData.append(data.text.strip())
            if(len(strippedData) == 6):
                startTime = datetime.strptime(
                    strippedData[2], "%b/%d/%Y %H:%M")
                contest['name'] = strippedData[0]
                contest['code'] = strippedData[0].split()[2]
                contest['start_time'] = str(startTime)
                if(len(strippedData[3]) == 5):
                    tempDate = datetime.strptime(strippedData[3], "%H:%M")
                contest['duration'] = str(timedelta(
                    hours=tempDate.hour, minutes=tempDate.minute, seconds=tempDate.second))
                contest['end_time'] = str(startTime + timedelta(
                    hours=tempDate.hour, minutes=tempDate.minute, seconds=tempDate.second))
                contest['resource'] = "codeforces"
                contest['id'] = "codeforces_"+strippedData[0].split()[2]
                contests.append(contest)
        return contests