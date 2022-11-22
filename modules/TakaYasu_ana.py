import pandas as pd
from modules import Gene_list

def cal_takane_yasune_ratioDF(df_meigara_list,sijou_name):
    # 株価データが手持ちに存在する銘柄のコードのセットを取得
    # kobetu_ticker_list = os.listdir("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ")

    # 日付データと日経平均の終値を取得
    date_list = Gene_list.GetListEigyoubi()
    value_list = Gene_list.GetNIKKEI225value()

    # n日高値安値のカラムのリストと新規データフレーム作成時のカラム作成用の辞書型を定義
    highlowlist = ["25dayhigh", "75dayhigh", "150dayhigh", "200dayhigh", "25daylow", "75daylow", "150daylow",
                   "200daylow"]
    highlowhanteidict = {"25dayhigh": 0, "75dayhigh": 1, "150dayhigh": 2, "200dayhigh": 3, "25daylow": 4, "75daylow": 5,
                         "150daylow": 6, "200daylow": 7}

    # n日高安銘柄数のカウント用の辞書型を定義キーは日付、要素はリスト
    highlowdic = {}
    for i in date_list:
        highlowdic[i] = [0, 0, 0, 0, 0, 0, 0, 0]
    meigarasuu = []

    # 騰落レシオの集計を利用して銘柄数をカウントする貯めのカウント用の辞書型を定義　キーは日付、要素は値上がり、値下がり、変わらず銘柄数のリスト
    touraku_hi = {}
    for j in range(0, len(date_list)):
        touraku_hi[date_list[j]] = [0, 0, 0]

    # 全個別銘柄を呼び出して新高値安値銘柄数カウントの繰り返し処置
    for i in range(0, len(df_meigara_list)):
        df = df_meigara_list[i]
        df_s = df.set_index('datetime')
        d = df_s.to_dict()
        # 個別銘柄ごとに対前Ｎ日各営業日毎の新高値安値かどうかを判別しカウント
        for k in date_list:
            for j in highlowlist:
                try:
                    atai = d[j][k]
                    highlowdic[k][highlowhanteidict[j]] = highlowdic[k][highlowhanteidict[j]] + atai
                except KeyError:
                    pass

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

    # 騰落レシオの値上がり、値下がり、変わらずを全て合算して当日の全銘柄数とする
    for j in range(0, len(date_list)):
        count = 0
        for i in range(0, 3):
            count = count + touraku_hi[date_list[j]][i]
        meigarasuu.append(count)

    # 日経平均の値と全銘柄数をデータフレームの新カラムとして追加し、CSVファイルに出力
    df_syuukei = pd.DataFrame.from_dict(highlowdic, orient="index")
    df_syuukei["NIKKEI225"] = value_list
    df_syuukei["allmeigarakazu"] = meigarasuu
    df_syuukei = df_syuukei.reset_index()
    df_syuukei = df_syuukei.rename(
        columns={'index': 'datetime', 0: "25dayhigh", 1: "75dayhigh", 2: "150dayhigh", 3: "200dayhigh",
                 4: "25daylow", 5: "75daylow", 6: "150daylow", 7: "200daylow"})

    df_syuukei.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\相場テクニカル指標\新高値新安値\\" + sijou_name + "日足.csv", index=False,
                             encoding='cp932')


