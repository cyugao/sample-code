import os
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from time import clock
from sklearn.model_selection import GridSearchCV

train_path = "../resource/lib/publicdata/aclImdb/train/"  # use terminal to ls files under this directory
test_path = "../resource/asnlib/public/imdb_te.csv"  # test data for grade evaluation

with open("stopwords.en.txt") as f_stop:
    stop_words = f_stop.read().splitlines()


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
	and combine text files under train_path directory into
    imdb_tr.csv. Each text file in train_path should be stored
    as a row in imdb_tr.csv. And imdb_tr.csv should have two
    columns, "text" and label'''
    count = 0
    pos_path = inpath + 'pos/'
    neg_path = inpath + 'neg/'
    with open(name, 'w') as csv_file:
        print(',text,polarity', file=csv_file)
        for file in os.listdir(pos_path):
            with open(pos_path + file) as file:
                content = file.read().replace('"', '')
            print('%d,"%s",1' % (count, content), file=csv_file)
            count += 1
        for file in os.listdir(neg_path):
            with open(neg_path + file) as file:
                content = file.readline().replace('"', '')
            print('%d,"%s",0' % (count, content), file=csv_file)
            count += 1

start = clock()
# imdb_data_preprocess(train_path)
end = clock()
print("Data combined in %.2fs" % (end - start))

start = clock()
train_file = "imdb_tr.csv"
test_path = "imdb_te.csv"
# train_file = 'test.csv'
# test_file = 'imdb_tr.sample.csv'

df = pd.read_csv(train_file, index_col='Unnamed: 0', encoding="ISO-8859-1")
X_train = df['text']
y_train = df['polarity']

df_test = pd.read_csv(test_path, index_col='Unnamed: 0', encoding="ISO-8859-1")
X_test = df_test['text']
# y_test = df_test['polarity']
end = clock()
print("Data loaded in %.2fs" % (end - start))

start = clock()
uni = CountVectorizer(stop_words=stop_words)
bi = CountVectorizer(ngram_range=(1, 2), stop_words=stop_words)

Tf_uni_trans = TfidfTransformer(sublinear_tf=True)
Tf_bi_trans = TfidfTransformer(sublinear_tf=True)

X_uni = uni.fit_transform(X_train)
X_uni_tfidf = Tf_uni_trans.fit_transform(X_uni)

X_bi = bi.fit_transform(X_train)
X_bi_tfidf = Tf_bi_trans.fit_transform(X_bi)

X_test_uni = uni.transform(X_test)
X_test_uni_tfidf = Tf_uni_trans.transform(X_test_uni)

X_test_bi = bi.transform(X_test)
X_test_bi_tfidf = Tf_bi_trans.transform(X_test_bi)
end = clock()
print("Data transformed in %.2fs" % (end - start))

data_dict = {
    "unigram": (X_uni, X_test_uni),
    # "unigramtfidf": (X_uni_tfidf, X_test_uni_tfidf),
    # "bigram": (X_bi, X_test_bi),
    # "bigramtfidf": (X_bi_tfidf, X_test_bi_tfidf)
}

paras = {
    'alpha': [1e-7, 5e-7, 1e-6, 5e-6, 5e-5, 1e-5],
    'penalty': ['l1', 'l2']
}


for name, pair in data_dict.items():
    xx, xx_test = pair
    start = clock()
    clf = GridSearchCV(SGDClassifier(max_iter=10, penalty='l1'), paras, cv=3)
    clf.fit(xx, y_train)
    end = clock()
    print("%s:" % name)
    print("Fitting...")
    print("Fit in %.2fs" % (end - start))
    result = clf.predict(xx_test)
    # score = clf.score(xx_test, y_test)
    print("Best param:", clf.best_params_)
    print("Best score:", clf.best_score_)
    output = name + ".output.txt"
    with open(output, 'w') as f:
        for i in result:
            print(i, file=f)
