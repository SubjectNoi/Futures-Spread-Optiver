from flask import Flask,redirect
from flask import request
from flask import render_template
import os

app = Flask(__name__)


@app.route('/')
@app.route('/<img>')
def hello(img=None):
    return render_template('home.html', img=img)

@app.route('/update_img', methods=['POST'])
def update_img():
    para1=request.form['para1']
    para2 = request.form['para2']
    # compute with params
    img_rst="optiver1.jpg"
    return redirect("/"+img_rst)

if __name__ == '__main__':
    app.run()