# %%
# !%matplotlib qt
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
import seaborn as sns

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


data_folder = os.path.join('csv_data', 'sender')

# Initialize dataframes
tree_df = pd.DataFrame()
grid_df = pd.DataFrame()
dom_df = pd.DataFrame()
non_dom_df = pd.DataFrame()

for subfolder in os.listdir(data_folder):
    for file in os.listdir(os.path.join(data_folder, subfolder)):
        # Get the trial number
        idx = int(file.split('_')[2].split('.')[0])

        # Read the data
        tmp_df = pd.read_csv(
            os.path.join(data_folder, subfolder, file),
        )

        if subfolder in ('dominant', 'non_dominant'):
            tmp_df = tmp_df.iloc[::2, :].reset_index(drop=True)

        # Add the trial number
        tmp_df['Trial'] = idx

        # Convert 'Time' to datetime
        tmp_df['Time'] = pd.to_datetime(tmp_df['Time'])
        # Calculate the time difference between two neighboring rows
        tmp_df['Time_diff'] = tmp_df['Time'].diff()

        # Handle the case where the difference is calculated across two different trials
        tmp_df.loc[tmp_df['Trial'] != tmp_df['Trial'].shift(), 'Time_diff'] = None

        # Convert the time difference to seconds
        tmp_df['Time_Diff'] = tmp_df['Time_diff'].dt.total_seconds()

        # Calculate the completion time
        tmp_df['Completion_Time'] = tmp_df['Time'].iloc[-1] - tmp_df['Time'].iloc[0]
        tmp_df['Completion_Time'] = tmp_df['Completion_Time'].dt.total_seconds() / 60

        if 'backspace' in tmp_df['Letter'].values:
            n_wrongs = tmp_df['Letter'].value_counts()['backspace']
        else:
            n_wrongs = 0
        n_total = tmp_df.shape[0]
        acc = (n_total - n_wrongs) / n_total

        # Calculate the ITR
        tmp_df['ITR'] = compute_itr_bpm(
            30, acc, n_total, tmp_df['Completion_Time'].iloc[0]
        )

        # Filter and reorder the columns
        tmp_df = tmp_df[
            ['Trial', 'Letter', 'Time', 'Time_Diff', 'Completion_Time', 'ITR']
        ]

        # Store the data in the corresponding dataframe
        if subfolder == 'tree':
            tree_df = pd.concat((tree_df, tmp_df))
        elif subfolder == 'grid':
            grid_df = pd.concat((grid_df, tmp_df))
        elif subfolder == 'dominant':
            dom_df = pd.concat((dom_df, tmp_df))
        elif subfolder == 'non_dominant':
            non_dom_df = pd.concat((non_dom_df, tmp_df))

tree_df.head()

# %%
# Get the default color cycle
def_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# Define the x-axis values
trial_range = range(1, 21)

# %%
# Combine the dataframes
combined_df = pd.concat(
    [
        tree_df.assign(dataset='Tree\nInterface'),
        grid_df.assign(dataset='Grid\nInterface'),
        dom_df.assign(dataset='Dominant\nTyping'),
        non_dom_df.assign(dataset='Non-Dominant\nTyping'),
    ]
)

# Create the violin plot
sns.violinplot(
    x='dataset',
    y='Time_Diff',
    data=combined_df,
    # inner_kws=dict(box_width=1, whis_width=0.1, color=".8"),
    linewidth=0.8,
)

plt.title('Sender Interface Comparison')
plt.xlabel('')
plt.ylabel('Time to Select a Letter (in s)')
# plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figures/exp_1-interface_time.png', dpi=300)
plt.savefig('figures/exp_1-interface_time.svg')
plt.show()
# %%
# Combine the dataframes
combined_df = pd.concat(
    [
        dom_df.assign(dataset='Dominant\nTyping'),
        non_dom_df.assign(dataset='Non-Dominant\nTyping'),
        tree_df.assign(dataset='Tree\nInterface'),
        grid_df.assign(dataset='Grid\nInterface'),
    ]
)

# Create the violin plot
sns.barplot(x='dataset', y='ITR', data=combined_df)

plt.title('Sender Interface Comparison')
plt.xlabel('')
plt.ylabel('Information Transfer Rate (in bits/min)')
# plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figures/exp_1-interface_itr.png', dpi=300)
plt.savefig('figures/exp_1-interface_itr.svg')
plt.show()

# %%
# Group by 'Trial' and get the mean of 'Completion_Time'
mean_completion_dom = dom_df.groupby('Trial')['Completion_Time'].mean()
mean_completion_non_dom = non_dom_df.groupby('Trial')['Completion_Time'].mean()
mean_completion_tree = tree_df.groupby('Trial')['Completion_Time'].mean()
mean_completion_grid = grid_df.groupby('Trial')['Completion_Time'].mean()

# Plot the mean completion time
mean_completion_dom.plot(kind='line', label='Keyboard (Dominant)')
mean_completion_non_dom.plot(kind='line', label='Keyboard (Non-Dominant)')
mean_completion_tree.plot(kind='line', label='Tree')
mean_completion_grid.plot(kind='line', label='Grid')

plt.title('Experiment 1 - Time to Complete a Trial')
plt.xlabel('Trial')
plt.ylabel('Time in Seconds')
plt.legend()
plt.show()

# %%
