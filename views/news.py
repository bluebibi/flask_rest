from flask import Blueprint

news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/main')
def news_main():
    return 'welcome news {0}'.format("yhhan")

@news_blueprint.route('/sports')
def news_sports():
    return 'welcome sports news {0}'.format("yhhan")

@news_blueprint.route('/science')
def news_science():
    return 'welcome science news {0}'.format("yhhan")
