import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from datetime import datetime



# r'C:\Users\moham\Desktop\FYP Test\distance\F.xlsx'
# ds = pd.read_excel(r'C:\Users\moham\Desktop\FYP Test\distance\F.xlsx')




# --------------------------------------


def item(hour, ds_):
    return ds_.loc[ds_['hour'] == hour]['city'].tolist()[0].split(',')[0]

# ---------------------------------------------------


def recommend(hour, num, ds_, results_):

    hr = str(hour)+':00'
    d = datetime.strptime(hr, "%H:%M")
    hr = d.strftime("%I:%M %p")

    print("Recommending " + str(num) + " places for time " + hr + ".")
    print("-------")
    recs = results_[hour][:num]
    resultArray = []
    for rec in recs:
        resultArray.append(item(rec[1], ds_))
        print("Recommended: " + item(rec[1],
                                     ds_) + " (score:" + str(rec[0]) + ")")

    return resultArray

# ------------------------------------------------------------------------------





def getRecommendations(Hour, Num, FileName):
    ds = pd.read_excel(FileName)
    tf = TfidfVectorizer(analyzer='word', ngram_range=(
        1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['city'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['hour'][i])
                         for i in similar_indices]

        results[row['hour']] = similar_items[1:]

    print('done!')
    return recommend(hour=Hour, num=Num, ds_=ds, results_=results)





# print(getRecommendations(Hour=8, Num=1, FileName= 'user 321 file.xlsx'))
