import pandas as pd

def Wariaihanbetu(wariai):
    if wariai < 5.0:
        return 0
    elif 5.0 <= wariai < 10.0:
        return 1
    elif 10.0 <= wariai < 15.0:
        return 2
    elif 15.0 <= wariai < 20.0:
        return 3
    elif 20.0 <= wariai < 25.0:
        return 4
    elif 25.0 <= wariai < 30.0:
        return 5
    elif 30.0 < wariai:
        return 6

dict1 = {}
dict2 = {}
list_a = [0,0,0,0,0,0,0]
dflist = []
df1 = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ\\" + "3063" + "\hiasi.csv")
df2 = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ\\" + "6146" + "\hiasi.csv")
df3 = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ\\" + "2676" + "\hiasi.csv")
dflist = [df1,df2,df3]

for i in range (0,len(dflist)):
    df = dflist[i].drop(dflist[i].index[-1])
    dflist[i] = df

for k in dflist:
    df = k
    date_list = df["datetime"].to_list()
    df = df.set_index('datetime',drop=False)
#全銘柄の売買代金の合計金額を集計し、日ごとの辞書型にまとめる
    for i in date_list:
         try :
             dict1[i] = dict1[i] + df.at[i,"baibaidaikin"]
         except:
             dict1[i] = df.at[i, "baibaidaikin"]

#集計した売買代金から個別銘柄ごとに売買代金に占める割合を計算し、占める割合毎の銘柄数を集計
for k in dflist:
    df = k
    date_list = df["datetime"].to_list()
    df = df.set_index('datetime', drop=False)
    for i in date_list:
            if (dict1[i] > 0.0):
                wariai = df.at[i,"baibaidaikin"] / dict1[i] * 100.0
                j = Wariaihanbetu(wariai)
                try:
                    dict2[i][j] += 1
                except:
                    list_a[j] += 1
                    dict2[i] = list_a
                    list_a = [0, 0, 0, 0, 0, 0, 0]

kekka = pd.DataFrame.from_dict(dict2, orient="index")
kekka = kekka.reset_index()
kekka = kekka.sort_values('index', inplace=False)
kekka = kekka.rename(columns={'index': 'datetime'})

print(kekka)