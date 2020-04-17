from flask import(Blueprint)
from flask import send_from_directory

bp = Blueprint('scraper', __name__)


@bp.route('/')
def index():
    response = {"data": "Index Route"}

    return response


@bp.route('/download')
def test():
    templatePath = "./resources/templates/"
    generatedImg = send_from_directory(
        directory=templatePath, filename="sample_image.jpg", as_attachment=True)

    return generatedImg
