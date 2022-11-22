#市場ごとに騰落レシオを計算するコード
import pandas as pd
from modules import Gene_list

# 遅いのでこっちは使わない
def cal_touraku_ratioCSV(meigaralist,sijou_name):
    # 2000年大発会以降の騰落数の集計
    touraku_hi = {}

    date_list = Gene_list.GetListEigyoubi()

    # 予め騰落数カウント用の辞書型ファイルを作成
    for j in range(0, len(date_list)):
        touraku_hi[date_list[j]] = [0, 0, 0]

    # 全個別銘柄を呼び出して騰落値のカウントの繰り返し処置
    for i in range(0, len(meigaralist)):
        ticker_code = str(meigaralist[i])
        df = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ\\"
                                            + ticker_code + "\hiasi.csv", encoding="ms932", sep=",")
        df = df.set_index("datetime")
        d = df.to_dict()

        # 個別銘柄ごとに対前日の騰落値をカウントするループ null値はescape処理
        for j in range(0, len(date_list)):
            try:
                touraku = d["touraku"][date_list[j]]
                if touraku == 1:
                    touraku_hi[date_list[j]][0] = touraku_hi[date_list[j]][0] + 1
                if touraku == -1:
                    touraku_hi[date_list[j]][1] = touraku_hi[date_list[j]][1] + 1
                elif touraku == 0:
                    touraku_hi[date_list[j]][2] = touraku_hi[date_list[j]][2] + 1
            except KeyError:
                pass

    # インデックスと騰落銘柄数をデータフレームに追加
    touraku_df = pd.DataFrame.from_dict(touraku_hi, orient="index")
    touraku_df["date"] = date_list
    touraku_df_new = touraku_df.rename(columns={0: '値上がり', 1: "値下がり", 2: "変わらず"})
    touraku_data_old = touraku_df_new[["date", '値上がり', "値下がり", "変わらず"]]
    touraku_data = touraku_data_old.reset_index()

    # 騰落レシオの計算
    # 計算値を格納する辞書
    touraku_dict = {"25日騰落レシオ": [], "50日騰落レシオ": [], "75日騰落レシオ": [], "150日騰落レシオ": [], "200日騰落レシオ": []}
    # 値上がり数、値下がり数のリストを取得
    neagari_list = touraku_data["値上がり"].to_list()
    nesagari_list = touraku_data["値下がり"].to_list()

    for i in range(0, len(neagari_list)):
        neagari = 0.0
        nesagari = 0.0
        tourakusuu = 0.0
        for a in [25, 50, 75, 150, 200]:
            inde = str(a) + "日騰落レシオ"
            if i > a:
                for j in range(0, a):
                    neagari = neagari + neagari_list[i - j]
                    nesagari = nesagari + nesagari_list[i - j]
                    if nesagari > 0:
                        tourakusuu = neagari / nesagari * 100
                    else:
                        tourakusuu = 100
                touraku_dict[inde].append(tourakusuu)
                neagari = 0.0
                nesagari = 0.0
                tourakusuu = 0.0
            else:
                touraku_dict[inde].append(0.0)
                neagari = 0.0
                nesagari = 0.0
                tourakusuu = 0.0

    touraku_dict_df = pd.DataFrame(touraku_dict)
    touraku_data_new = touraku_data.join(touraku_dict_df)
    touraku_data_last = touraku_data_new.reset_index()
    touraku_data_last.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\相場テクニカル指標\騰落レシオ\\" + sijou_name + "騰落レシオ.csv", index=False, encoding='cp932')

# 第１引数はdataflameを格納したリスト　第２引数は市場の名前str
def cal_touraku_ratioDF(df_meigara_list,sijou_name):
    # 2000年大発会以降の騰落数の集計
    touraku_hi = {}

    date_list = Gene_list.GetListEigyoubi()

    # 予め騰落数カウント用の辞書型ファイルを作成
    for j in range(0, len(date_list)):
        touraku_hi[date_list[j]] = [0, 0, 0]

    # 全個別銘柄を呼び出して騰落値のカウントの繰り返し処置
    for i in range(0, len(df_meigara_list)):
        df = df_meigara_list[i]
        df = df.set_index("datetime")
        d = df.to_dict()

        # 個別銘柄ごとに対前日の騰落値をカウントするループ null値はescape処理
        for j in range(0, len(date_list)):
            try:
                touraku = d["touraku"][date_list[j]]
                if touraku == 1:
                    touraku_hi[date_list[j]][0] = touraku_hi[date_list[j]][0] + 1
                if touraku == -1:
                    touraku_hi[date_list[j]][1] = touraku_hi[date_list[j]][1] + 1
                elif touraku == 0:
                    touraku_hi[date_list[j]][2] = touraku_hi[date_list[j]][2] + 1
            except KeyError:
                pass

    # インデックスと騰落銘柄数をデータフレームに追加
    touraku_df = pd.DataFrame.from_dict(touraku_hi, orient="index")
    touraku_df["date"] = date_list
    touraku_df_new = touraku_df.rename(columns={0: '値上がり', 1: "値下がり", 2: "変わらず"})
    touraku_data_old = touraku_df_new[["date", '値上がり', "値下がり", "変わらず"]]
    touraku_data = touraku_data_old.reset_index()

    # 騰落レシオの計算
    # 計算値を格納する辞書
    touraku_dict = {"25日騰落レシオ": [], "50日騰落レシオ": [], "75日騰落レシオ": [], "150日騰落レシオ": [], "200日騰落レシオ": []}
    # 値上がり数、値下がり数のリストを取得
    neagari_list = touraku_data["値上がり"].to_list()
    nesagari_list = touraku_data["値下がり"].to_list()

    # n日間の騰落レシオのカウント&計算
    for i in range(0, len(neagari_list)):
        neagari = 0.0
        nesagari = 0.0
        tourakusuu = 0.0
        for a in [25, 50, 75, 150, 200]:
            inde = str(a) + "日騰落レシオ"
            if i > a:
                for j in range(0, a):
                    neagari = neagari + neagari_list[i - j]
                    nesagari = nesagari + nesagari_list[i - j]
                    if nesagari > 0:
                        tourakusuu = neagari / nesagari * 100
                    else:
                        tourakusuu = 100
                touraku_dict[inde].append(tourakusuu)
                neagari = 0.0
                nesagari = 0.0
                tourakusuu = 0.0
            else:
                touraku_dict[inde].append(0.0)
                neagari = 0.0
                nesagari = 0.0
                tourakusuu = 0.0

    touraku_dict_df = pd.DataFrame(touraku_dict)
    touraku_data_new = touraku_data.join(touraku_dict_df)
    touraku_data_last = touraku_data_new[["date", "値上がり", "値下がり", "変わらず", "25日騰落レシオ", "50日騰落レシオ", "75日騰落レシオ", "150日騰落レシオ", "200日騰落レシオ"]]
    touraku_data_last["NIKKEI225"] = Gene_list.GetNIKKEI225value()
    touraku_data_last.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\相場テクニカル指標\騰落レシオ\\" + sijou_name + "騰落レシオ.csv", index=False, encoding='cp932')







