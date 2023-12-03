# %%
# !%matplotlib qt
import sys

import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

plt.style.use(['science', 'grid', 'notebook', 'no-latex'])
plt.rcParams.update(
    {
        'xtick.minor.bottom': False,
        'xtick.minor.top': False,
        'ytick.minor.left': False,
        'ytick.minor.right': False,
    }
)
# High-DPI monitor settings
if 'qApp' not in vars():
    from matplotlib.backends.qt_compat import QtWidgets

    qApp = QtWidgets.QApplication(sys.argv)
    plt.matplotlib.rcParams['figure.dpi'] = qApp.desktop().physicalDpiX()


# %%
def compute_itr_bpm(n, p, trials, time):
    if p == 1:
        b = np.log2(n)
    else:
        b = np.log2(n) + p * np.log2(p) + (1 - p) * np.log2((1 - p) / (n - 1))
    information_transfer = b * trials
    itr = information_transfer / time
    return itr


n_rec_letters = np.array(
    [
        9,
        8,
        10,
        11,
        12,
        11,
        12,
        11,
        12,
        13,
        11,
        13,
        8,
        10,
        13,
        14,
        13,
        14,
        14,
        15,
    ]
)
n_wrong_received = np.array(
    [0, 2, 1, 0, 0, 2, 1, 0, 1, 2, 0, 4, 2, 2, 1, 0, 0, 2, 1, 2]
)
n_correct_received = n_rec_letters - n_wrong_received

n_sent_letters = np.array(
    [
        13,
        12,
        15,
        14,
        15,
        15,
        16,
        17,
        18,
        18,
        16,
        16,
        11,
        14,
        15,
        19,
        16,
        18,
        18,
        18,
    ]
)
n_wrong_sent = np.array([0, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 2, 2, 1, 0, 2, 0, 0, 0])
n_correct_sent = n_sent_letters - n_wrong_sent


# %%
# Define a logarithmic function
def logarithmic_function(x, a, b):
    return a * np.log(x) + b


# Get the default color cycle
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
n_trial = np.arange(1, 21)
n_trial_interp = np.arange(1, 20, 1 / 50)

f_sent = interp1d(n_trial, n_sent_letters, kind='quadratic')
f_sent_correct = interp1d(n_trial, n_correct_sent, kind='quadratic')
f_rec = interp1d(n_trial, n_rec_letters, kind='quadratic')
f_rec_correct = interp1d(n_trial, n_correct_received, kind='quadratic')

plt.figure()
plt.plot(
    n_trial_interp,
    f_sent(n_trial_interp),
    label='Sent Letters',
    color=default_colors[0],
    alpha=0.2,
    lw=1,
)
plt.plot(
    n_trial_interp,
    f_sent_correct(n_trial_interp),
    label='Correctly Sent',
    color=default_colors[0],
    lw=1,
)

params, covariance = curve_fit(logarithmic_function, n_trial, n_correct_sent)
a_fit, b_fit = params
plt.plot(
    n_trial,
    logarithmic_function(n_trial, a_fit, b_fit),
    ls='dashdot',
    label='Sender Learning Curve',
    color=default_colors[0],
)


plt.plot(
    n_trial_interp,
    f_rec(n_trial_interp),
    label='Received Letters',
    color=default_colors[1],
    alpha=0.2,
    lw=1,
)
plt.plot(
    n_trial_interp,
    f_rec_correct(n_trial_interp),
    label='Correctly Received',
    color=default_colors[1],
    lw=1,
)

params, covariance = curve_fit(logarithmic_function, n_trial, n_correct_received)
a_fit, b_fit = params
plt.plot(
    n_trial,
    logarithmic_function(n_trial, a_fit, b_fit),
    ls='dashdot',
    label='Receiver Learning Curve',
    color=default_colors[1],
)

plt.scatter(n_trial, n_sent_letters, alpha=0.2, s=20, color=default_colors[0])
plt.scatter(n_trial, n_correct_sent, s=20, color=default_colors[0])
plt.scatter(n_trial, n_rec_letters, alpha=0.2, s=20, color=default_colors[1])
plt.scatter(n_trial, n_correct_received, s=20, color=default_colors[1])


plt.title('Sent & Received Letters')
plt.xlabel('Trial')
plt.ylabel('Number of Letters')
plt.xticks(range(1, 21))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=2)
plt.tight_layout()
plt.grid()
plt.savefig('figures/exp_3-n_letters.png', dpi=300)
plt.savefig('figures/exp_3-n_letters.svg')
plt.show()

# %%
itr_sent = []
itr_rec = []

for n_trials in n_sent_letters:
    itr_sent.append(compute_itr_bpm(30, 1, n_trials, 1))

for n_trials, acc in zip(n_rec_letters, n_correct_received / n_rec_letters):
    itr_rec.append(compute_itr_bpm(30, acc, n_trials, 1))

np.mean(itr_sent)
np.mean(itr_rec)
np.std(itr_sent)
np.std(itr_rex)

# %%
import seaborn as sns

sns.catplot(itr_sent, label='Sender')
sns.catplot(itr_rec, label='Receiver')
# %%
