import pandas as pd

if __name__ == '__main__':
    df = df = pd.DataFrame.from_csv('data/princeton.txt', sep='\t')
    # df = pd.read_csv('data/njit.txt', error_bad_lines=False, header=None)
    # print(df.iloc[0])
    # print(df.iloc[1])
    print(df.iloc[0])