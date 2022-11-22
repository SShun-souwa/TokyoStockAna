import pandas as pd

# 個別株データを暦日から営業日ベースの形に整形
# 引数はstr

def KobetuDayShape(df_kobetu, date_list):
    df_kobetu_new = pd.DataFrame()

    # 東証営業日のデータのみ抽出してデータフレームを再構成する
    for date in date_list:
        df_onetime = df_kobetu[(df_kobetu["datetime"] == date)]
        df_kobetu_new = df_kobetu_new.append(df_onetime)
        df_kobetu_new = df_kobetu_new.reset_index(drop=True)
    return df_kobetu_new

# 引数はstr 移動平均を計算する関数
def KobetuDayMA(df_kobetu):
    # 移動平均の計算
    # 計算値を格納する辞書を定義
    MA_dict = {"5MA": [], "25MA": [], "50MA": [], "75MA": [], "150MA": [], "200MA": []}
    # 終値のリスト取得
    owarine_list = df_kobetu["close"].to_list()
    for i in range(0, len(owarine_list)):
        MA = 0.0
        for days in [5, 25, 50, 75, 150, 200]:
            inde = str(days) + "MA"
            if i > days:
                for j in range(0, days):
                    MA = MA + owarine_list[i - j] / days
                MA_dict[inde].append(MA)
                MA = 0.0
            else:
                MA_dict[inde].append(0.0)
                MA = 0.0

    MA_dict_df = pd.DataFrame(MA_dict)
    df_kobetu_new = df_kobetu.join(MA_dict_df)

    return df_kobetu_new

# 引数はstr 新高値を判別する
def KobetuSintakane(df_kobetu):
    # 集計値を格納する辞書を定義
    takane_dict = {"25dayhigh": [], "75dayhigh": [], "150dayhigh": [], "200dayhigh": []}
    # 場中高値と終値のリストを取得
    high_list = df_kobetu["high"].to_list()
    owarine_list = df_kobetu["close"].to_list()

    for days in [25, 75, 150, 200]:

        for i in range(0, len(owarine_list)):
            high = 0
            inde = str(days) + "dayhigh"
            kaisi = i - days
            if i >= days:
                count = 0

                for j in range(kaisi, i):
                    if high_list[j] > high:
                        high = high_list[j]

                for j in range(kaisi, i):
                    if owarine_list[i] > high:
                        count = 1

                takane_dict[inde].append(count)

            else:
                count = 0
                takane_dict[inde].append(count)

    takane_dict_df = pd.DataFrame(takane_dict)
    df_kobetu_new = df_kobetu.join(takane_dict_df)

    return df_kobetu_new

# 引数はstr 新安値を判別する
def KobetuSinyasune(df_kobetu):
    # 集計値を格納する辞書を定義
    takane_dict = {"25daylow": [], "75daylow": [], "150daylow": [], "200daylow": []}
    # 場中高値と終値のリストを取得
    low_list = df_kobetu["low"].to_list()
    owarine_list = df_kobetu["close"].to_list()

    for days in [25, 75, 150, 200]:

        for i in range(0, len(owarine_list)):
            low = 100000000000000000
            inde = str(days) + "daylow"
            kaisi = i - days
            if i >= days:
                count = 0

                for j in range(kaisi, i):
                    if low_list[j] < low:
                        low = low_list[j]

                for j in range(kaisi, i):
                    if owarine_list[i] < low:
                        count = 1

                takane_dict[inde].append(count)

            else:
                count = 0
                takane_dict[inde].append(count)

    takane_dict_df = pd.DataFrame(takane_dict)
    df_kobetu_new = df_kobetu.join(takane_dict_df)

    return df_kobetu_new
