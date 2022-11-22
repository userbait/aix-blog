import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

if __name__ == "__main__":
    data = pd.read_csv('../urlSet.csv', nrows=10000)

    # 데이터 셋 분리
    x = data[['length_url', 'shortening_service', 'nb_at', 'nb_at',
             'https_token', 'nb_www', 'dns_record', 'web_traffic', 'google_index', 'nb_hyperlinks']]
    y = data['status']

    (x_train, x_test, y_train, y_test) = train_test_split(x, y, test_size=0.25)

    # RandomForest 모델 생성
    rf = RandomForestClassifier()

    # 모델 학습
    rf.fit(x_train, y_train)

    # 모델 저장
    joblib.dump(rf, '../phishing_sites_detector.pkl')
