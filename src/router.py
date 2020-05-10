from .services import ImageGenerator, ContestsRetreiver
from flask import(Blueprint, request)
import io
from flask import send_file
import json
from .models import Contest


bluePrint = Blueprint('router', __name__)


@bluePrint.route('/')
def index():
    response = {"data": "Index Route"}
    return response


@bluePrint.route('/download')
def test():
    imageGenerator = ImageGenerator()
    contestJson = request.json
    if(contestJson != None):
        contest = Contest.fromJson(contestJson)
        generatedImage = imageGenerator.generateImage(contest)
        imageIO = io.BytesIO()
        generatedImage.save(imageIO, 'JPEG', quality=100)
        imageIO.seek(0)
        return send_file(imageIO, mimetype='image/jpeg')
    else:
        return "No Contest"


@bluePrint.route('/contests')
def fun():
    retriever = ContestsRetreiver()
    return json.dumps(retriever.getContestDetails())
