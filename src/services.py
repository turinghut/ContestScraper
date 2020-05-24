import textwrap
import requests as req
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw
from dateutil import parser
from datetime import datetime, timedelta


class ImageGenerator:
    fontDirectory = "src/resources/fonts/RobotoBlack.ttf"
    storyTemplateDirectory = "src/resources/templates/storyTemplate.jpg"

    def generateImage(self, contest):
        MAX_W = 1080
        font = ImageFont.truetype(self.fontDirectory, 50)
        image = Image.open(self.storyTemplateDirectory)
        draw = ImageDraw.Draw(image)
        w, h = font.getsize("Platform : " + contest.platform)
        draw.text((((MAX_W - w) / 2), 900), "Platform : " +
                  contest.platform, fill="white", font=font, align="center")
        w, h = font.getsize("Contest code : " + contest.contestCode)
        draw.text((((MAX_W - w) / 2), 1000), "Contest code : " +
                  contest.contestCode, fill="white", font=font, align="center")
        font = ImageFont.truetype(self.fontDirectory, 70)
        lines = textwrap.wrap(contest.contestName, width=25)
        y_text = 1150
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((MAX_W - width) / 2, y_text),
                      line, font=font, fill="white")
            y_text += height
        font = ImageFont.truetype(self.fontDirectory, 50)
        draw.text((150, y_text+100), "START : ",
                  fill="white", font=font, align="left")
        timeDifference = contest.endDateTime - contest.startDateTime
        contest.startDateTime = str(
            contest.startDateTime.strftime('%d-%m-%Y %H:%M:%S'))
        contest.endDateTime = str(
            contest.endDateTime.strftime('%d-%m-%Y %H:%M:%S'))
        draw.text((400, y_text+100), contest.startDateTime,
                  fill="white", font=font, align="left")
        draw.text((150, y_text+200), "END : ", fill="white",
                  font=font, align="right")
        draw.text((400, y_text+200), contest.endDateTime,
                  fill="white", font=font, align="right")
        timeDifference = str(timeDifference)
        duration = ""
        print(timeDifference)
        durationList = timeDifference
        if "days" in timeDifference:
            daysList = timeDifference.split(" days, ")
            duration = daysList[0] + " days "
        if "days" in timeDifference:
            durationList = timeDifference.split(" days, ")
            durationList = durationList[1]
        # print(durationList)
        durationList = durationList.split(":")
        print("hi")
        if(durationList[0] != "00"):
            duration += str(durationList[0]) + " Hours "
        if(durationList[1] != "00"):
            duration += str(durationList[1]) + " Minutes "
        if(durationList[2] != "00"):
            duration += str(durationList[2]) + " Seconds"
        w, h = font.getsize("DURATION : " + duration)
        draw.text((((MAX_W - w) / 2), y_text+300), "DURATION : " +
                  str(duration), fill="white", font=font, align="right")
        return image


class ContestsRetreiver:
    def getTodaysContestDetails(self):
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

    def getAllUpcomingContestDetails(self):
        contestsJson = []
        codechefContests = self.getContestsfromCodechef()
        for contest in codechefContests:
            print(contest)
            contestsJson.append(contest)
        codeforcesContests = self.getContestsfromCodeforces()
        for contest in codeforcesContests:
            print(contest)
            contestsJson.append(contest)
        contestsJson.sort(key=lambda contest: contest['end_time'])
        return contestsJson

    def getContestsfromCodechef(self):
        try:
            URL = "https://www.codechef.com/contests"
            headers = {'User-Agent': 'Mozilla/5.0'}
            soup = bs(req.get(URL, headers=headers).content, 'lxml')
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
                    contest['platform'] = "codechef"
                    contest['id'] = "codechef_"+strippedData[0]
                    contests.append(contest)
            return contests
        except:
            print('Error retrieving codechef details')
            return []

    def getContestsfromCodeforces(self):
        try:
            URL = "http://codeforces.com/contests"
            headers = {'User-Agent': 'Mozilla/5.0'}
            soup = bs(req.get(URL, headers=headers).content, 'lxml')
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
                    startTime = startTime + timedelta(hours=2, minutes=30)
                    contest['name'] = strippedData[0]
                    contest['code'] = strippedData[0].split()[2]
                    contest['start_time'] = str(startTime)
                    if(len(strippedData[3]) != 5):
                        strippedData[3] = strippedData[3].split(':', 1)[1]
                    tempDate = datetime.strptime(strippedData[3], "%H:%M")
                    contest['duration'] = str(timedelta(
                        hours=tempDate.hour, minutes=tempDate.minute, seconds=tempDate.second))
                    contest['end_time'] = str(startTime + timedelta(
                        hours=tempDate.hour, minutes=tempDate.minute, seconds=tempDate.second))
                    contest['platform'] = "codeforces"
                    contest['id'] = "codeforces_"+strippedData[0].split()[2]
                    contests.append(contest)
            return contests
        except:
            print('Error retrieving codeforces details')
            return []
