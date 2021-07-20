import argparse
import pickle
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate.bleu_score import sentence_bleu
import re
from tqdm import tqdm
from lmg_eval import load_kNN_model
import matplotlib.pyplot as plt
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
    

    org_diff_data = (train_diff, test_diff)
    tf_diff_data = (train_ftr, test_ftr)
    ref_data = (train_msg, test_msg)
    
    dict_k={}
    
    for k in range(1,20):
        blue_scores = load_kNN_model(org_diff_code=org_diff_data, tf_diff_code=tf_diff_data, ref_msg=ref_data, topK=k)
        dict_k[k] = sum(blue_scores) / len(blue_scores) * 100
        print('Average of blue scores for k=',k,': ', sum(blue_scores) / len(blue_scores) * 100)
        
    
    bleu_list=[]
    for i in range(1,11):
        bleu_list.append(dict_k[i])
        
    K = range(1,11)
    plt.plot(K, bleu_list, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Bleu_score')
    plt.show()
    plt.savfig('topK_graph_1to10.png')
    plt.close()
    
    
    bleu_list=[]
    for i in range(11,21):
        bleu_list.append(dict_k[i])
        
    K = range(11,21)
    plt.plot(K, bleu_list, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Bleu_score')
    plt.show()
    plt.savfig('topK_graph_11to20.png')
    plt.close()
