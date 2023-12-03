# %%
# !%matplotlib qt
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
import seaborn as sns
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image

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


acc_1 = [0.9, 1, 0.833333333, 0.916666667, 0.923076923]
acc_2 = [0.636363636, 0.916666667, 0.923076923, 0.916666667, 0.916666667]
acc_3 = [1, 0.923076923, 0.846153846, 0.923076923, 1]

# Convert the data into a DataFrame
df = pd.DataFrame(
    {
        'Configuration 1': np.array(acc_1) * 100,
        'Configuration 2': np.array(acc_2) * 100,
        'Configuration 3': np.array(acc_3) * 100,
    }
)

# Create the box plots
ax = sns.barplot(data=df)

# File paths to your images in the folder (replace these with your image file paths)
image_paths = ['conf_1.png', 'conf_2.png', 'conf_3.png']

ax.set_xticks(range(len(image_paths)))
ax.set_xticklabels(['', '', ''])

# Load images and set them as x-axis tick labels
for i, path in enumerate(image_paths):
    img = plt.imread(os.path.join('figures', path))  # Check folder structure
    img = OffsetImage(img, zoom=0.3)
    img.image.axes = ax

    ab = AnnotationBbox(
        img,
        (i, 0),
        xybox=(0.0, -45.0),
        frameon=False,
        xycoords='data',
        boxcoords="offset points",
        pad=0,
    )
    ax.add_artist(ab)

plt.title('Vibrotactile Placement Comparison')
plt.ylabel('Accuracy (in %)')
plt.tight_layout()
plt.savefig('figures/exp_2-placement.png', dpi=300)
plt.savefig('figures/exp_2-placement.svg')
plt.show()

# %%
n_total_1 = [11, 12, 13, 12, 12]
n_total_2 = [13, 13, 13, 13, 12]
n_total_3 = [10, 8, 12, 12, 13]

time_1 = [55, 60, 56, 46, 48]
time_2 = [54, 57, 57, 51, 46]
time_3 = [50, 50, 50, 50, 50]

itr_1 = []
itr_2 = []
itr_3 = []

for n_trials, time, acc in zip(n_total_1, time_1, acc_1):
    itr_1.append(compute_itr_bpm(4, acc, n_trials, time / 60))

for n_trials, time, acc in zip(n_total_2, time_2, acc_2):
    itr_2.append(compute_itr_bpm(4, acc, n_trials, time / 60))

for n_trials, time, acc in zip(n_total_3, time_3, acc_3):
    itr_3.append(compute_itr_bpm(4, acc, n_trials, time / 60))

# Convert the data into a DataFrame
df = pd.DataFrame(
    {
        'Configuration 1': np.array(itr_1),
        'Configuration 2': np.array(itr_2),
        'Configuration 3': np.array(itr_3),
    }
)

# Create the box plots
ax = sns.barplot(data=df)

# File paths to your images in the folder (replace these with your image file paths)
image_paths = ['conf_1.png', 'conf_2.png', 'conf_3.png']

ax.set_xticks(range(len(image_paths)))
ax.set_xticklabels(['', '', ''])

# Load images and set them as x-axis tick labels
for i, path in enumerate(image_paths):
    img = plt.imread(os.path.join('figures', path))  # Check folder structure
    img = OffsetImage(img, zoom=0.3)
    img.image.axes = ax

    ab = AnnotationBbox(
        img,
        (i, 0),
        xybox=(0.0, -45.0),
        frameon=False,
        xycoords='data',
        boxcoords="offset points",
        pad=0,
    )
    ax.add_artist(ab)

plt.title('Vibrotactile Placement Comparison')
plt.ylabel('Information Transfer Rate (in bits/min)')
plt.tight_layout()
plt.savefig('figures/exp_2-placement_itr.png', dpi=300)
plt.savefig('figures/exp_2-placement_itr.svg')
plt.show()

# %%
