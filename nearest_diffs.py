import argparse
import pickle
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate.bleu_score import sentence_bleu
import re
from tqdm import tqdm
from lmg_eval import finding_bestK, finding_topK, clean_msg
import csv
from sys import exit


def read_args():
    parser = argparse.ArgumentParser()    
    parser.add_argument('-train_data', type=str, default='./data/lmg/train.pkl', help='the directory of our training data')
    parser.add_argument('-test_data', type=str, default='./data/lmg/test.pkl', help='the directory of our training data')

    parser.add_argument('-train_cc2ftr_data', type=str, default='./data/lmg/train_cc2ftr.pkl', help='the directory of our training data')
    parser.add_argument('-test_cc2ftr_data', type=str, default='./data/lmg/test_cc2ftr.pkl', help='the directory of our training data')
    return parser


if __name__ == '__main__':
    params = read_args().parse_args()
    data_train = pickle.load(open(params.train_data, "rb"))
    train_msg, train_diff = clean_msg(data_train[0]), data_train[1]

    data_test = pickle.load(open(params.test_data, "rb"))
    test_msg, test_diff = data_test[0], data_test[1]

    train_ftr = pickle.load(open(params.train_cc2ftr_data, "rb"))   
    test_ftr = pickle.load(open(params.test_cc2ftr_data, "rb"))
    
    final_list_cosine_sim=[['test_diff'],['given_LM'],['pred_diff'],['pred_LM'],['top1_diff'],['top1_LM'],['top2_diff'],['top2_LM']
     ,['top3_diff'],['top3_LM'],['top4_diff'],['top4_LM'],['top5_diff'],['top5_LM'],['top6_diff'],['top6_LM']
     ,['top7_diff'],['top7_LM'],['top8_diff'],['top8_LM'],['top9_diff'],['top9_LM'],['top10_diff'],['top10_LM']]
    
    for i, (_) in enumerate(tqdm([i for i in range(test_ftr.shape[0])])):
        temp=[]
        element = test_ftr[i, :]
        element = np.reshape(element, (1, element.shape[0]))
        cosine_sim = cosine_similarity(X=train_ftr, Y=element)
        topK_index = finding_topK(cosine_sim, topK=20)
        # taking top 10 diffs based on cosine similarity
        bestK = finding_bestK(diff_trains=train_diff, diff_test=test_diff[i], topK_index=topK_index)
        # bestK is the index of predicted log message
        predlm = train_msg[bestK].lower()
        givenlm = test_msg[i].lower()
        prediff = train_diff[bestK]
        final_list_cosine_sim[0].append(test_diff[i].replace('<nl>','\n'))
        final_list_cosine_sim[1].append(givenlm)
        final_list_cosine_sim[2].append(prediff.replace('<nl>','\n'))
        final_list_cosine_sim[3].append(predlm)
        x = 4
        for j in topK_index:
            final_list_cosine_sim[x].append(train_diff[j].replace('<nl>','\n'))
            final_list_cosine_sim[x+1].append(train_msg[j])
            x=x+2
        
    with open('nearest_diff.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(final_list_cosine_sim)
        
        
        
        
        
        
