import sys
import pandas as pd
from time import clock
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

input_file = sys.argv[1]
output = sys.argv[2]

alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.2]

debug = True

df = pd.read_csv(input_file)
op_file = open(output, 'w')

if debug:
    import matplotlib.pyplot as plt

    set0 = df[df['label'] == 0]
    set1 = df[df['label'] == 1]
    fig, ax = plt.subplots()
    ax.scatter(set0.A, set0.B, marker='x', color='red')
    ax.scatter(set1.A, set1.B, marker='o', color='green')
    ax.set_xlim(df.A.min() - .2, df.A.max() + .2)
    ax.set_ylim(df.B.min() - .2, df.B.max() + .2)
    plt.show()

n = len(df)
X_train, X_test, y_train, y_test = train_test_split(df.drop('label', axis=1)
                                                    , df['label'], test_size=0.4)

models = {
    "svm_linear": (SVC(), {"kernel": ("linear",), 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}),
    "svm_polynomial": (SVC(), {"kernel": ("poly",), 'C': [0.1, 1, 3],
                               'degree': [4, 5, 6], 'gamma': [0.1, 0.5]}),
    "svm_rbf": (SVC(), {"kernel": ("rbf",), 'C': [0.1, 0.5, 1, 5, 10, 50, 100],
                        'gamma': [0.1, 0.5, 1, 3, 6, 10]}),
    "logistic": (LogisticRegression(), {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}),
    "knn": (KNeighborsClassifier(), {'n_neighbors': range(1, 51), 'leaf_size': range(5, 61, 5)}),
    "decision_tree": (DecisionTreeClassifier(), {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}),
    "random_forest": (RandomForestClassifier(), {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)})

}

for model in models:
    start = clock()
    clf = GridSearchCV(*models[model], scoring='accuracy', cv=5)
    clf.fit(X_train, y_train)
    best_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    stop = clock()
    print('%s: Finished in %.2fs' % (model, stop - start))
    print('%s,%.3f,%.3f' % (model, best_score, test_score), file=op_file)

op_file.close()
