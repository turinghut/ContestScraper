#pip install pillow
from datetime import datetime
from Contest import  Contest
from PIL import Image, ImageFont, ImageDraw
class ImageGenerator:
    contests = []
    #change location accordingly
    saveLocation = '/home/sindhuja/Pictures/'
    def __init__(self):
        print('New Object has been generated')
    def getContestDetails(self):
        print('Contest details have been updated')
        #sample data, comment the next line out for testing
        #self.contests.append(Contest('MAY20','May Challenge 2020','Codechef.com','01 MAY 2020 15:00:00','11 MAY 2020 15:00:00'))
    def generateImages(self):
        MAX_W, MAX_H = 1080, 1720
        letterInPixel = 26.667
        font = ImageFont.truetype(r'Roboto-Black.ttf', 50)
        count = 0
        for i in self.contests:
            image = Image.open('storyTemplate.jpg')
            draw = ImageDraw.Draw(image)
            w, h = font.getsize("Platform : " + i.platform)
            draw.text((((MAX_W - w) / 2), 900), "Platform : " + i.platform, fill="white", font=font, align="center")
            w, h = font.getsize("Contest code : " + i.contestCode)
            draw.text((((MAX_W - w) / 2), 1000), "Contest code : " + i.contestCode, fill="white", font=font, align="center")
            font = ImageFont.truetype(r'Roboto-Black.ttf', 70)
            w, h = font.getsize(i.contestName)
            # draw.text((((MAX_W-w)/2), 5), contestName, fill ="white", font=font, align="center")
            draw.text((((MAX_W - w) / 2), 1150), i.contestName, fill="white", font=font, align="center")
            font = ImageFont.truetype(r'Roboto-Black.ttf', 50)
            draw.text((150, 1300), "START : ", fill="white", font=font, align="left")
            draw.text((400, 1300), i.startDateTime, fill="white", font=font, align="left")
            draw.text((150, 1400), "END : ", fill="white", font=font, align="right")
            draw.text((400, 1400), i.endDateTime, fill="white", font=font, align="right")
            timeDifference = datetime.strptime(i.endDateTime,'%d %b %Y %H:%M:%S') - datetime.strptime(i.startDateTime,'%d %b %Y %H:%M:%S')
            secondsTaken = timeDifference.total_seconds()
            hours = divmod(secondsTaken, 3600)[0]
            secondsTaken = timeDifference.total_seconds()
            days  = divmod(secondsTaken, 86400)[0]
            if(int(hours) > 24):
                duration = str(int(days)) + " Days"
            else:
                duration = str(int(hours)) + " Hours"
            w, h = font.getsize("DURATION : " +duration)
            draw.text((((MAX_W - w) / 2), 1500), "DURATION : " + str(duration), fill="white", font=font, align="right")
            image.save(self.saveLocation + "Image-" + str(count) + ".png")
            count += 1
#to run
imageGenerator =  ImageGenerator()
imageGenerator.getContestDetails()
imageGenerator.generateImages()


