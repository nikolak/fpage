# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle

common_css = Bundle(
    "libs/bootstrap3/css/bootstrap.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

common_js = Bundle(
    "libs/jquery2/jquery.js",
    "libs/bootstrap3/js/bootstrap.min.js",
    "js/plugins.js",
    "js/script.js",
    # filters="jsmin", #painful to debug with it
    output="public/js/common.js"
)