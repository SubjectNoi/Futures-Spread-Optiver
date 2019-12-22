from flask import Flask,redirect
from flask import request
from flask import render_template
import os
import sys
sys.path.append("..")
sys.path.append("../src/stage3_Regression")
from src.stage3_Regression.make_policy import experiment
import datetime
import random

app = Flask(__name__)


@app.route('/')
@app.route('/<img>/<begin_date>/<end_date>/<start_founding>/<policy_idx>/<bulin_coeff>')
def hello(img="optiver.png",begin_date="20170105",end_date="20181227",start_founding="2000000",policy_idx="0",bulin_coeff="2"):
    return render_template('home.html', img=img, begin_date=begin_date,end_date=end_date,start_founding=start_founding, policy_idx=policy_idx,bulin_coeff=bulin_coeff)

def get_uniq_num():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum

@app.route('/update_img', methods=['POST'])
def update_img():
    # experiment(begin_date, end_date, start_founding, policy_idx, bulin_coeff)
    begin_date=request.form['begin_date']
    end_date = request.form['end_date']
    start_founding = float(request.form['start_founding'])
    policy_idx = int(request.form['policy_idx'])
    bulin_coeff = float(request.form["bulin_coeff"])
    out_img_name="out_"+str(get_uniq_num())+".png"
    experiment(begin_date, end_date, start_founding, policy_idx, bulin_coeff, out_img_name)
    # compute with params
    return redirect("/"+"/".join([out_img_name,begin_date, end_date, str(start_founding), str(policy_idx), str(bulin_coeff)]))

if __name__ == '__main__':
    app.run()