# %%
# !%matplotlib qt
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
data_folder = os.path.join('csv_data', 'sender_receiver_data')

# Trials to be excluded from the analysis
trials_exclude = (16, 21)

# Initialize dataframes
encoder_df = pd.DataFrame()
decoder_df = pd.DataFrame()

for file in os.listdir(data_folder):
    # Get the trial number
    idx = int(file.split('_')[2].split('.')[0])
    if idx not in trials_exclude:
        # Adjust the trial number after excluding bad trials
        if idx > 21:
            idx = idx - 2
        elif idx > 16:
            idx = idx - 1

        # Read the data
        tmp_df = pd.read_csv(
            os.path.join(data_folder, file),
            names=['Input', 'Letter', 'Time'],
        )
        # Drop the first two trials required to start the recording
        tmp_df = tmp_df.iloc[2:].reset_index(drop=True)
        tmp_df.index += 1

        # Add the trial number
        tmp_df['Trial'] = idx

        # Convert 'Time' to datetime
        tmp_df['Time'] = pd.to_datetime(tmp_df['Time'])
        # Calculate the time difference between two neighboring rows
        tmp_df['Time_diff'] = tmp_df['Time'].diff()

        # Handle the case where the difference is calculated across two different trials
        tmp_df.loc[tmp_df['Trial'] != tmp_df['Trial'].shift(), 'Time_diff'] = None

        # Convert the time difference to seconds
        tmp_df['Time_diff'] = tmp_df['Time_diff'].dt.total_seconds()

        # Filter and reorder the columns
        tmp_df = tmp_df[['Trial', 'Letter', 'Time', 'Time_diff']]

        # Store the data in the corresponding dataframe
        if 'encoder' in file:
            encoder_df = pd.concat((encoder_df, tmp_df))
        elif 'decoder' in file:
            decoder_df = pd.concat((decoder_df, tmp_df))

encoder_df

# %%
# Get the number of letters sent per trial and the number of correctly encoded letters
enc_df = encoder_df.groupby('Trial').agg(
    {'Letter': ['count', lambda x: (x == 'backspace').sum()]}
)

# Rename the columns
enc_df.columns = ['n_encoded', 'n_wrong']
enc_df['n_correct'] = enc_df['n_encoded'] - enc_df['n_wrong']

# Reset the index
enc_df = enc_df.reset_index()

# %%

# %%
# Get the default color cycle
def_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# Define the x-axis values
trial_range = range(1, 21)

plt.plot(
    trial_range,
    enc_df['n_encoded'],
    '-o',
    label='Encoded Letters',
    color=def_colors[0],
    alpha=0.5,
)
plt.plot(
    trial_range,
    enc_df['n_correct'],
    '-o',
    label='Correctly Encoded',
    color=def_colors[0],
)

plt.title('Experiment 1 - Sent & Received Letters')
plt.xlabel('Trial')
plt.ylabel('Number of Letters')
plt.xticks(trial_range)
plt.yticks(range(6, 21))
plt.ylim(5, 21)
plt.legend()
plt.tight_layout()
# plt.savefig('figures/exp_1.png', dpi=300)
# plt.savefig('figures/exp_1.svg')
plt.show()

# %%
# Group by trial and take the mean and standard deviation
mean_time_encoder = encoder_df.groupby('Trial')['Time_diff'].mean()
std_time_encoder = encoder_df.groupby('Trial')['Time_diff'].std()

mean_time_decoder = decoder_df.groupby('Trial')['Time_diff'].mean()
std_time_decoder = decoder_df.groupby('Trial')['Time_diff'].std()

plt.plot(mean_time_encoder, '-o', label='Encoder Speed', color=def_colors[0])
plt.fill_between(
    mean_time_encoder.index,
    mean_time_encoder - std_time_encoder,
    mean_time_encoder + std_time_encoder,
    color=def_colors[0],
    alpha=0.2,
)


# plt.plot(mean_time_decoder, '-o', label='Decoder Speed', color=def_colors[1])
# plt.fill_between(
#     mean_time_decoder.index,
#     mean_time_decoder - std_time_decoder,
#     mean_time_decoder + std_time_decoder,
#     color=def_colors[1],
#     alpha=0.2,
# )

plt.title('Experiment 1 - Sent & Received Letters')
plt.xlabel('Trial')
plt.ylabel('Time in Seconds')
plt.xticks(trial_range)
plt.legend()
plt.tight_layout()
plt.show()
# %%
