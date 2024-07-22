import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename, newline='') as csvfile:
        shop = csv.DictReader(csvfile)
        evidence = []
        label = []
        for d in shop:
            adm = int(d['Administrative'])
            adm_dur = float(d['Administrative_Duration'])
            inf = int(d['Informational'])
            inf_dur = float(d['Informational_Duration'])
            pro = int(d['ProductRelated'])
            pro_dur = float(d['ProductRelated_Duration'])
            bou = float(d["BounceRates"])
            exi = float(d['ExitRates'])
            pag = float(d['PageValues'])
            spe = float(d['SpecialDay'])
            match d['Month']:
                case 'Jan':
                    mon = 0
                case 'Feb':
                    mon = 1
                case 'Mar':
                    mon = 2
                case 'Apr':
                    mon = 3
                case 'May':
                    mon = 4
                case 'Jun':
                    mon = 5
                case 'Jul':
                    mon = 6
                case 'Aug':
                    mon = 7
                case 'Sep':
                    mon = 8
                case 'Oct':
                    mon = 9
                case 'Nov':
                    mon = 10
                case 'Dec':
                    mon = 11
            ops = int(d['OperatingSystems'])
            bro = int(d['Browser'])
            reg = int(d['Region'])
            tra = int(d['TrafficType'])
            match d['VisitorType']:
                case 'Returning_Visitor':
                    vis = 1
                case 'New_Visitor':
                    vis = 0
            match d["Weekend"]:
                case 'TRUE':
                    wee = 1
                case 'FALSE':
                    wee = 0
            match d["Revenue"]:
                case 'TRUE':
                    rav = 1
                case 'FALSE':
                    rav = 0
            evidence.append([adm, adm_dur, inf, inf_dur, pro, pro_dur, bou, 
                             exi, pag, spe, mon, ops, bro, reg, tra, vis, wee])
            label.append(rav)
        return evidence, label     


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(evidence, labels)
    return model  


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    buy_num = 0
    watch_num = 0
    buy_good = 0
    watch_good = 0
    for l, p in zip(labels, predictions):
        if l == 0:
            watch_num += 1
            if l == p:
                watch_good += 1
        else:
            buy_num += 1
            if l == p:
                buy_good += 1
    return buy_good / buy_num, watch_good/watch_num
                
    
if __name__ == "__main__":
    main()

