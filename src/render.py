from flask import Flask, request, render_template, redirect, url_for
import PEHAKS

app = Flask(__name__)


@app.route('/')

@app.route('/pehaks/input')
def inputPage():
    return render_template('input.html')

@app.route('/run',methods=['POST'])
def run():
    if request.method == 'POST':
        W = request.form['W']
        W_p = request.form['W_p']
        W_c = request.form['W_c']
        return redirect(url_for('pehaksResult', W=W, W_p=W_p, W_c=W_c))


@app.route('/pehaks/result/<W>&<W_p>&<W_c>')
def pehaksResult(W, W_p, W_c):
    result = PEHAKS.pehaks(W, W_p, W_c)
    return render_template('pehaks.html', result=result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)