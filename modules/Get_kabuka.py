#yahoo finance apiを用いて東証全銘柄の株価データを取得するモジュール
import sys
import os
import pandas as pd
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from modules import Gene_list
from modules import kabuka_Set

#株価データ取得のための関数　引数はstr
def GetKABU (code):
    use_code = code +".T"
    my_share = share.Share(use_code)
    symbol_data = None
#日足のデータを２５年分取得
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                              25,
                                              share.FREQUENCY_TYPE_DAY,
                                              1)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

#タイムスタンプを日付に変換
    data = pd.DataFrame(symbol_data)
    data["datetime"] = pd.to_datetime(data.timestamp, unit="ms")
    data["datetime"] = pd.to_datetime(data["datetime"]).dt.strftime("%Y-%m-%d")
#データフレームを日付、始値、高値、安値、終値、出来高で再構築
    kobetu_data = data[["datetime", "open", "high", "low", "close", "volume"]]
# 東証営業日のみのデータに整形
    date_list = Gene_list.GetListEigyoubi()
    kobetu_data = kabuka_Set.KobetuDayShape(kobetu_data, date_list)

# 終値ベースの売買代金を追加
    list = []
    for i in range(0, len(kobetu_data)):
        daikin_temp = kobetu_data.iloc[i, 4] * kobetu_data.iloc[i, 5]
        list.append(daikin_temp)

    list_df = pd.DataFrame({'baibaidaikin': list})
    kobetu_data = pd.concat([kobetu_data, list_df], axis=1)
    list.clear()

# 対前日終値で各銘柄が上昇したか下落したかを判別し、CSVファイルに'touraku'カラムを追加して+1,-1,0で判別
    list = [0]
    for i in range(1, len(kobetu_data)):
        if (kobetu_data.iloc[i, 4] - kobetu_data.iloc[i - 1, 4] > 0):
            list.append(1)
        elif (kobetu_data.iloc[i, 4] - kobetu_data.iloc[i - 1, 4] < 0):
            list.append(-1)
        else:
            list.append(0)

    list_df = pd.DataFrame({'touraku': list})
    kobetu_data = pd.concat([kobetu_data, list_df], axis=1)
    list.clear()

#移動平均値や新高値安値を追加
    kobetu_data  = kabuka_Set.KobetuDayMA(kobetu_data)
    kobetu_data  = kabuka_Set.KobetuSintakane(kobetu_data)
    kobetu_data  = kabuka_Set.KobetuSinyasune(kobetu_data)

#個別銘柄のコード毎にディレクトリ作成
    new_dir_path = "I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ\\" + code

    if os.path.exists(new_dir_path) == False :
        os.mkdir(new_dir_path)

#csvファイルに出力
    kobetu_data.to_csv(new_dir_path + "//"  + "hiasi.csv", index=False, encoding='cp932')

    return

