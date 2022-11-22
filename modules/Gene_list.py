import pandas as pd

def GetListEigyoubi():
    # 2000年大発会以降の東証営業日日付データを日経平均のヒストリカルデータからリストで取得
    date_input = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\指数時系列データ\日足\日経平均\\ni225.csv",
                         encoding="ms932",
                         sep=",")
    # 日付の書式を揃え、2000年大発会までのデータを削除
    date_input["datetime"] = pd.to_datetime(date_input["date"]).dt.strftime("%Y-%m-%d")
    date_list = date_input["datetime"].to_list()
    del date_list[0:date_list.index("2000-01-04")]

    return date_list

def GetNIKKEI225value():
    # 2000年大発会以降の東証営業日日付データを日経平均のヒストリカルデータからリストで取得
    date_input = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\指数時系列データ\日足\日経平均\\ni225.csv",
                         encoding="ms932",
                         sep=",")
    # 日付の書式を揃え、2000年大発会までのデータを削除
    date_input["date"] = pd.to_datetime(date_input["date"]).dt.strftime("%Y-%m-%d")
    date_list = date_input["date"].to_list()
    value_list = date_input[" value"].to_list()
    del value_list[0:date_list.index("2000-01-04")]

    return value_list

def GetListToushouMeigara():
    # 東証公表データxlsファイルの読込
    df = pd.read_excel("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\リスト\東証個別銘柄リスト\data_j.xls")

    # 個別銘柄の必要情報のみ抽出
    df_kobetu = df[
        (df["市場・商品区分"] == "プライム（内国株式）")
        | (df["市場・商品区分"] == "スタンダード（内国株式）")
        | (df["市場・商品区分"] == "グロース（内国株式）")
        ]
    kobetu_infomation = df_kobetu[["コード", "銘柄名", "市場・商品区分", "33業種コード", "33業種区分", "17業種コード", "17業種区分"]]

    # 個別銘柄コードのみリストで抽出
    code_list = kobetu_infomation["コード"].to_list()

    return code_list

def CSVToushouMeigara():
    # 東証公表データxlsファイルの読込
    df1 = pd.read_excel("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\リスト\東証個別銘柄リスト\data_j.xls")

    # 個別銘柄の必要情報のみ抽出
    df_kobetu = df1[
        (df1["市場・商品区分"] == "プライム（内国株式）")
        | (df1["市場・商品区分"] == "スタンダード（内国株式）")
        | (df1["市場・商品区分"] == "グロース（内国株式）")
        ]
    kobetu_infomation = df_kobetu[["コード", "銘柄名", "市場・商品区分", "33業種コード", "33業種区分", "17業種コード", "17業種区分"]]
    # 必要情報をcsv出力
    kobetu_infomation.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\リスト\東証個別銘柄リスト\\" + "東証個別株リスト.csv", index=False,
                             encoding='cp932')

    meigaraset = kobetu_infomation["コード"].to_list()

    # 市場ごとの抽出
    prime = df1[(df1["市場・商品区分"] == "プライム（内国株式）")]

    standard = df1[(df1["市場・商品区分"] == "スタンダード（内国株式）")]

    growth = df1[(df1["市場・商品区分"] == "グロース（内国株式）")]

    prime_standard = df1[(df1["市場・商品区分"] == "プライム（内国株式）")
                     | (df1["市場・商品区分"] == "スタンダード（内国株式）")]

    sijou_list = {"プライム": prime, "スタンダード": standard, "グロース": growth, "プライムスタンダード": prime_standard}

    for i in sijou_list.keys():
        # 空のデータフレームを作成
        df_concat = pd.DataFrame()

        sijou = sijou_list[i]
        for code in meigaraset:
            code = int(code)
            if code < 10000:
                try:
                    a = sijou[sijou["コード"] == code]
                    df_concat = pd.concat([df_concat, a])

                except:
                    pass

        # コードの昇順にソート
        df_concat = df_concat.sort_values('コード', ascending=True)
        # 必要情報をcsv出力
        kobetu_infomation = df_concat[["コード", "銘柄名", "市場・商品区分", "33業種コード", "33業種区分", "17業種コード", "17業種区分"]]
        kobetu_infomation.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\リスト\東証個別銘柄リスト\\" + i + "個別株リスト.csv", index=False,
                                 encoding='cp932')

    return
