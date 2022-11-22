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

        # url based features
        if url_based_features.is_shortened_url(url) == True:
            is_shortened = 1
        else:
            is_shortened = 0

        if url_based_features.use_https(url) == True:
            use_https = 1
        else:
            use_https = 0

        # domain based features
        if domain_based_features.has_dns_record(url) == True:
            has_dns_record = 1
        else:
            has_dns_record = 0

        if domain_based_features.is_indexed(url) == True:
            is_indexed = 1
        else:
            is_indexed = 0

        return render_template('result.html', url=url)
    elif request.method == 'GET':
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port=5000)
