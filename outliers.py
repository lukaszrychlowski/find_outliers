from matplotlib import pyplot as plt
import pandas as pd 
import os

cols = ['d theor. [A]', 'theta difference [deg]']
path = '/Users/user/Desktop/profiles/Profiles extraction/Results/'
#path = '/Users/user/Desktop/2/'

def reader_text(file):
    df = pd.read_csv(file.path, encoding='UTF-16 LE', delimiter=';', skiprows=7, usecols=cols)
    df.insert(2, 'z_score', 0)
    df.insert(3, 'is_outlier', False)
    return df

def plotter(df, df_outliers, entry):
    ax = df.plot(x=cols[0], y=cols[1], kind='scatter', s=8, c='black', title=entry.name)
    df_outliers.plot(x=cols[0], y=cols[1], kind='scatter', s=8, c='red', ax=ax)
    plt.xlim(left=0, right=3)
    plt.ylim(bottom=-10, top=10)
    plt.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.savefig(path+str(subentry.name)+'.png')
    plt.close()

def z_score_mad(df):
    coeff = 1.4826
    median_df = df.median()
    mad = coeff*abs((df - median_df)).median()
    return abs(df-median_df) * mad**-1

for entry in os.scandir(path):
    if entry.is_file():
        continue
    else:
        for subentry in os.scandir(entry):
            if subentry.name.endswith('Summary.txt'):
                df = reader_text(subentry)
                df['z_score'] = z_score_mad(df[cols[1]])
                df['is_outlier'] = df['z_score'] > 10
                df_outliers = df[df['is_outlier'] == True]
                plotter(df, df_outliers, subentry)
                
                print(subentry.name)
                print(df)
                print('')
            else:
                continue