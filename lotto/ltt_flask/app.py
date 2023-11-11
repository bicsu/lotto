# /app.py
from flask import Flask, render_template, request
from help_funcs import get_date, get_num, lottodataUpdate
from flask import jsonify
#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/',methods=('GET', 'POST')) #
def index():

    # show today and this saturday dates

    today_, saturday_ = get_date()

    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        print(request.form.get('user')) 
        return render_template('index.html', today_=today_, satur=saturday_)
    elif request.method == "GET":
        return render_template('index.html', today_=today_, satur=saturday_)


@app.route('/show_num',methods=('GET', 'POST')) # 접속하는 url
def show_num():
    lottodataUpdate()
    sggstd_ltt_num = get_num()
    return render_template('show_num.html', suggested_num=sggstd_ltt_num)

@app.route('/info',) # 접속하는 url
def update_round():
    lottodataUpdate()
    today_, saturday_ = get_date()

    return render_template('info.html', )




if __name__=="__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)