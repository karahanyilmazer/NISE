# %%
# !%matplotlib qt
import sys

import matplotlib.pyplot as plt
import numpy as np
import scienceplots

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
        12,
        13,  # Check this one
        13,  # Check this one
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
        18,  # Check this one
        18,
    ]
)
n_trial = np.arange(1, 21)

# Get the default color cycle
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
# %%
plt.plot(
    n_trial, n_sent_letters, label='Encoded Letters', color=default_colors[0], alpha=0.5
)
plt.plot(n_trial, n_sent_letters, label='Correctly Encoded', color=default_colors[0])
plt.plot(
    n_trial, n_rec_letters, label='Decoded Letters', color=default_colors[1], alpha=0.5
)
plt.plot(
    n_trial, n_correct_received, label='Correctly Decoded', color=default_colors[1]
)

plt.plot(n_trial, n_sent_letters, 'o', color=default_colors[0], alpha=0.5)
plt.plot(n_trial, n_sent_letters, 'o', color=default_colors[0])
plt.plot(n_trial, n_rec_letters, 'o', color=default_colors[1], alpha=0.5)
plt.plot(n_trial, n_correct_received, 'o', color=default_colors[1])

plt.title('Experiment 1 - Sent & Received Letters')
plt.xlabel('Trial')
plt.ylabel('Number of Letters')
plt.xticks(n_trial)
plt.yticks(range(6, 21))
plt.ylim(5, 21)
plt.legend()
plt.tight_layout()
plt.savefig('figures/exp_1.png', dpi=300)
plt.savefig('figures/exp_1.svg')
plt.show()

# %%
