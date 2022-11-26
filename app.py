from flask import Flask, render_template, request, redirect, url_for
from features import domain_based_features, url_based_features, content_based_features
import joblib
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        url = request.form['url']

        # -- url based features
        url_len =  url_based_features.get_url_length(url) # length_url

        if url_based_features.is_shortened_url(url) == True: # shotening_service
            is_shortened = 1
        else:
            is_shortened = 0

        nb_at = url_based_features.get_nb_at(url) # nb_at

        nb_hyphens = url_based_features.get_nb_hyphen(url) # nb_hyphens

        if url_based_features.use_https(url) == True: # https_token
            use_https = 1
        else:
            use_https = 0

        nb_www = url_based_features.get_nb_www(url) # nb_www

        # --  domain based features
        if domain_based_features.has_dns_record(url) == True: # dns_record
            has_dns_record = 1
        else:
            has_dns_record = 0

        page_rank = domain_based_features.get_page_rank(url) # page_rank

        if domain_based_features.is_indexed(url) == True:
            is_indexed = 1
        else:
            is_indexed = 0

        # -- content based features
        if content_based_features.get_nb_hyperlinks(url) == -1:
            return render_template('index.html') # 에러가 나면 메인 페이지로 돌아감
        else:
            nb_hyperlinks = content_based_features.get_nb_hyperlinks(url)

        model = joblib.load('./phishing_sites_detector.pkl')

        param = [[url_len, is_shortened, nb_at, nb_hyphens, use_https, nb_www, # url_based_features
                 has_dns_record, page_rank, is_indexed, # domain_based_features
                 nb_hyperlinks]] # content_based_feature

        prob = model.predict_proba(param)[0][1]
        prob = np.float64(prob).item()
        prob = round(prob, 2)
        prob = round(prob * 100, 2)

        return render_template('result.html', prob=prob)
    elif request.method == 'GET':
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port=5000)
