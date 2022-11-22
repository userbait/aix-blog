from flask import Flask, render_template, request, redirect, url_for
from features import domain_based_features, url_based_features

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        url = request.form['url']
        return render_template('result.html', url=url)
    elif request.method == 'GET':
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port=5000)
