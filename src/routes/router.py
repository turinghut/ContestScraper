from flask import(Blueprint)
from flask import send_from_directory

bluePrint = Blueprint('router', __name__)


@bluePrint.route('/')
def index():
    response = {"data": "Index Route"}
    return response


@bluePrint.route('/download')
def test():
    templatePath = "./resources/templates/"
    generatedImg = send_from_directory(
        directory=templatePath, filename="sample_image.jpg", as_attachment=True)
    return generatedImg
