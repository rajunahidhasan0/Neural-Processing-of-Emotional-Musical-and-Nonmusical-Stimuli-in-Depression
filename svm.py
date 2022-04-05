import pandas as pd
import os 
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics

INPUT_PATH = 'G:/nhr/fMRI/restructured/'

def svm_on_roi(roi_name, result_list):

    # roi_name = 'AngularGyrus'
    dir=INPUT_PATH+roi_name+ '/'


    catagories = []
    data = []
    for sub in os.listdir(dir):
        roi_path = dir + sub
        # print(sub)
        # sub=swarsub-control01-AngularGyrus.csv
        roi_data = pd.read_csv(roi_path, sep=' ')
        roi_data = roi_data.values
        tmp_sub_roi = roi_data[:20]

        flatten = []
        for tmp in tmp_sub_roi:
            flatten.extend(tmp[3:])

        cat = 0 if "control" in sub else 1

        catagories.append(cat)
        data.append(flatten)
        # break
        
    # train test split
    X_train, X_test, y_train, y_test = train_test_split(data, catagories, test_size=0.2,random_state=39)



    clf = svm.SVC(kernel='poly') # Linear Kernel
    clf.fit(X_train, y_train)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)

    print('ROI name : {}   -------------------------------------------------------'.format(roi_name))
    # Model Accuracy: how often is the classifier correct?

    ac = metrics.accuracy_score(y_test, y_pred)*100
    pc = metrics.precision_score(y_test, y_pred)*100
    rc = metrics.recall_score(y_test, y_pred)*100

    # Precision = TP / (TP+FP)
    # Recall = TP / (TP+FN)
    # Accuracy = (TP + TN) / (TP + TN + FP + FN)

    print("Accuracy:",ac)

    # Model Precision: what percentage of positive tuples are labeled as such?
    print("Precision:",pc)

    # Model Recall: what percentage of positive tuples are labelled as such?
    print("Recall:",rc)   
    print("\n")

    tmp_list = [roi_name[:-4], ac, pc, rc]
    result_list.append(tmp_list)

    return result_list


# controlling
result_list = []
for roi in sorted(os.listdir(INPUT_PATH)):
    result_list = svm_on_roi(roi, result_list)
    # if "ParietalOperculumCortex" in roi: break

cols = ['roi_name'+'%', 'accuracy(%)', 'precision', 'recall']
out_result = pd.DataFrame(result_list, columns = cols)
file_name = 'each_roi_accuracy_polynomial.csv'
out_result.to_csv(file_name, encoding='utf-8', index=False)