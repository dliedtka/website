#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap

import os
from datetime import datetime


app = Flask(__name__)
Bootstrap(app)

cur_dir = os.path.dirname(os.path.abspath(__file__))

def get_last_edited_date():
    '''
    Return the most recent date a file in the website project was edited.
    '''
    dir_names = [cur_dir]
    fnames = []
    while len(dir_names) != 0:
        dir_ = dir_names.pop(0)
        for fname in os.listdir(dir_):
            if fname[0] == '.':
                continue
            if os.path.isdir(f"{dir_}/{fname}"):
                dir_names.append(f"{dir_}/{fname}")
            else:
                fnames.append(f"{dir_}/{fname}")
    max_ = 0
    for fname in fnames:
        if os.path.getmtime(fname) > max_:
            max_ = os.path.getmtime(fname)
    return datetime.fromtimestamp(max_).strftime("%m/%d/%Y")
        

@app.route("/")
def index():
    return render_template("index.html", date=get_last_edited_date())

@app.route("/images/<filename>")
def images(filename):
    image_dir = f"{cur_dir}/images"
    return send_from_directory(image_dir, filename)


if __name__ == "__main__":
    app.run(debug=True)
    