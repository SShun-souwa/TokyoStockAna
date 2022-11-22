import pandas as pd
from modules import Gene_list

def cal_baibaidaikinDF(df_meigara_list,sijou_name):

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
    dict3 = {}
    joui_meigara = [4,9,14,19]

    #for i in range(0, len(dflist)):
        #df = dflist[i].drop(dflist[i].index[-1])
        #dflist[i] = df

    for k in df_meigara_list:
        date_list = k["datetime"].to_list()
        k = k.set_index('datetime', drop=False)
        # 全銘柄の売買代金の合計金額を集計し、日ごとの辞書型にまとめる
        for i in date_list:
            try:
                #print(k.at[i, "baibaidaikin"])
                dict1[i] = dict1[i] + float(k.at[i, "baibaidaikin"])
                dict2[i].append(float(k.at[i, "baibaidaikin"]))
            except:
                dict1[i] = float(k.at[i, "baibaidaikin"])
                dict2[i] = [0.0]
                dict3[i] = 0.0

    date_list_all = Gene_list.GetListEigyoubi()

    for j in joui_meigara:

        for i in date_list_all:
            try:
                a = dict1[i]
                if dict1[i] > 0:
                    if len(dict2[i]) > j:
                        dict2[i].sort(reverse=True)
                        temp_value = 0.0
                        for k in range(0, j):
                            temp_value = temp_value + dict2[i][k]
                        dict3[i] = temp_value / dict1[i] * 100
                    else:
                        dict3[i] = 0.0
                else:
                    dict3[i] = 0.0
            except:
                dict3[i] = 0.0

        n = str(j + 1)
        kekka = pd.DataFrame.from_dict(dict3, orient="index")
        kekka = kekka.reset_index()
        kekka = kekka.sort_values('index', inplace=False)
        kekka = kekka.rename(columns={'index': 'datetime'})
        kekka.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\相場テクニカル指標\売買代金\\" + sijou_name + n + "上位銘柄日足.csv", index=False,
                         encoding='cp932')




