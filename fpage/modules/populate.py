# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect

# import requests


blueprint = Blueprint('populate', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/populate/<size>", methods=['GET'])
def populate(size):
    """
    Populate database with number of submissions from reddit
    """
    return redirect(url_for('page.page'))
    # api_url = "http://www.reddit.com/r/all/new/.json?limit={}".format(size)
    # headers = {"user-agent": "/u/wub_wub test script"}
    #
    # r = requests.get(api_url, headers=headers)
    # data = r.json()
    #
    # added = 0
    # for item in data['data']['children']:
    #     try:
    #         item = item['data']
    #         user = User(username=item['author'],
    #                     email="{}@{}.com".format(item['author'], item['subreddit']),
    #                     password=item['author'])
    #         db.session.add(user)
    #         sub = Submission(title=item['title'],
    #                          url=item['url'],
    #                          ups=item['ups'],
    #                          downs=item['downs'],
    #                          timestamp=item['created_utc'],
    #                          author=user)
    #
    #         db.session.add(sub)
    #         db.session.commit()
    #         added += 1
    #     except:
    #         db.session.rollback()
    #         db.session.commit()
    #
    # flash("Added {} submissions".format(added), 'success')
    # return redirect(url_for('page.page'))
