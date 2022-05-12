import numpy as np
import pandas as pd
import scipy
from tabulate import tabulate
from scipy.stats import ttest_rel, ttest_ind, wilcoxon
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, RandomForestClassifier

scores = np.load('results/gmean_results.npy').T
m_scores = np.mean(scores, axis = 1)
me_scores = [[m] for m in m_scores]
mean_scores = np.array(me_scores)

datasets = ['ecoli-0-1_vs_2-3-5', 'ecoli-0-1_vs_5', 'ecoli-0-1-4-6_vs_5', 'ecoli-0-3-4_vs_5', 'ecoli-0-4-6_vs_5',
            'ecoli-0-6-7_vs_5', 'glass-0-1-4-6_vs_2', 'glass-0-1-5_vs_2', 'glass-0-1-6_vs_2', 'glass-0-1-6_vs_5', 'glass-0-4_vs_5',
            'glass-0-6_vs_5']

ens_d = {
    'Bagging': BaggingClassifier(),
    'AdaBoost': AdaBoostClassifier(),
    'RandomForest': RandomForestClassifier()
}

n_datasets = len(datasets)
n_ens = len(ens_d)
n_splits = 5
n_repeats = 2

alpha = 0.05

t_stat, p_val, adv, sig, s_better = (np.zeros(shape=(n_ens, n_ens), dtype=float) for _ in range(5))

for i in range(n_ens):
    for j in range(n_ens):
            t_stat[i,j], p_val[i,j] = ttest_rel(scores.T[i] , scores.T[j])

headers = list(ens_d.keys())
names_column = np.expand_dims(np.array(list(ens_d.keys())), axis=1)

adv[t_stat > 0] = 1
sig[p_val <= alpha] = 1
s_better = adv*sig

mean_table = tabulate(np.concatenate((names_column, mean_scores), axis = 1), floatfmt=".2f")
t_stat_table = tabulate(np.concatenate((names_column, t_stat), axis = 1), headers, floatfmt=".2f")
p_val_table = tabulate(np.concatenate((names_column, p_val), axis = 1), headers, floatfmt=".2f")
adv_table = tabulate(np.concatenate((names_column, adv), axis = 1), headers, floatfmt=".2f")
sig_table = tabulate(np.concatenate((names_column, sig), axis = 1), headers, floatfmt=".2f")
result_table = tabulate(np.concatenate((names_column, s_better), axis = 1), headers, floatfmt=".2f")

print(f"\navg gmean:\n{mean_table}\n")
print(f"t-stat:\n{t_stat_table}\n\np-value:\n{p_val_table}\n\nadvantage:\n{adv_table}\n\nsignificance:\n{sig_table}\n\nstat-better:\n{result_table}\n")