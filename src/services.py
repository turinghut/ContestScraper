from datetime import datetime, timedelta
from dateutil import parser
from .models import Contest
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup as bs
import requests as req


class ImageGenerator:
    contests = []
    fontDirectory = "src/resources/fonts/RobotoBlack.ttf"
    storyTemplateDirectory = "src/resources/templates/storyTemplate.jpg"

    def __init__(self):
        self.getContestDetails()

    def getContestDetails(self):
        # Get it from Database
        self.contests.append(Contest('MAY20', 'May Challenge 2020',
                                     'Codechef.com', '01 MAY 2020 15:00:00', '11 MAY 2020 15:00:00'))

    def generateImages(self):
        generatedImages = []
        MAX_W = 1080
        font = ImageFont.truetype(self.fontDirectory, 50)
        count = 0
        for i in self.contests:
            image = Image.open(self.storyTemplateDirectory)
            draw = ImageDraw.Draw(image)
            w, h = font.getsize("Platform : " + i.platform)
            draw.text((((MAX_W - w) / 2), 900), "Platform : " +
                      i.platform, fill="white", font=font, align="center")
            w, h = font.getsize("Contest code : " + i.contestCode)
            draw.text((((MAX_W - w) / 2), 1000), "Contest code : " +
                      i.contestCode, fill="white", font=font, align="center")
            font = ImageFont.truetype(self.fontDirectory, 70)
            w, h = font.getsize(i.contestName)
            draw.text((((MAX_W - w) / 2), 1150), i.contestName,
                      fill="white", font=font, align="center")
            font = ImageFont.truetype(self.fontDirectory, 50)
            draw.text((150, 1300), "START : ",
                      fill="white", font=font, align="left")
            draw.text((400, 1300), i.startDateTime,
                      fill="white", font=font, align="left")
            draw.text((150, 1400), "END : ", fill="white",
                      font=font, align="right")
            draw.text((400, 1400), i.endDateTime,
                      fill="white", font=font, align="right")
            timeDifference = datetime.strptime(
                i.endDateTime, '%d %b %Y %H:%M:%S') - datetime.strptime(i.startDateTime, '%d %b %Y %H:%M:%S')
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
            generatedImages.append(image)
            count += 1
        return generatedImages


class ContestsRetreiver:
    def getContestDetails(self):
        # 2020-05-11 15:00:00
        contestsJson = []
        contests = []
        codechefContests = self.getContestsfromCodechef()
        for contest in codechefContests:
            if(datetime.now().date == parser.parse(contest['start_time']).date):
                contestsJson.append(contest)
        codeforcesContests = self.getContestsfromCodeforces()
        for contest in codeforcesContests:
            if(datetime.now().date == parser.parse(contest['start_time']).date):
                contestsJson.append(contest)

        for json in contestsJson:
            # self, contestCode, contestName, platform, startDateTime, endDateTime
            contests.append(Contest(
                json['code'], json['name'], json['resource'], json['start_time'], json['end_time']))
        return contests

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
                contests.append(contest)
        return contests
