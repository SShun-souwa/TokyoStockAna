import pandas as pd
from modules import Gene_list
from modules import kabuka_Set
from modules import Touraku_ana
from modules import kabuka_Set
from modules import TakaYasu_ana
from modules import Baibaidaikin_ana

df_allkobetucode = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\リスト\東証個別銘柄リスト\東証個別株リスト.csv"
                         , encoding="ms932", sep=",")
all_code_list = df_allkobetucode["コード"].to_list()
all_meigara_DFdic = {}

for i in all_code_list:
    if i < 10000:
        code = str(i)
        df_kobetu = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\個別銘柄データ\\" + code + "\hiasi.csv")
        if df_kobetu.iat[0,-1] == df_kobetu.iat[0,-2]:
            df_kobetu = df_kobetu.drop(df_kobetu.index[-1])
        df_kobetu = df_kobetu.fillna(0)
        all_meigara_DFdic[code] = df_kobetu

sijou_list = ["プライム","スタンダード","グロース","プライムスタンダード"]

#指定した市場の個別銘柄のデータを読み込み、リスト化してモジュールに渡す
for j in sijou_list:
    df_sijoubetumeigaracode = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\リスト\東証個別銘柄リスト\\" + j + "個別株リスト.csv"
                         , encoding="ms932", sep=",")
    code_list = df_sijoubetumeigaracode["コード"].to_list()
    meigara_list =[]

    for i in code_list:
        code = str(i)
        meigara_list.append(all_meigara_DFdic[code])

    Baibaidaikin_ana.cal_baibaidaikinDF(meigara_list,j)
    Touraku_ana.cal_touraku_ratioDF(meigara_list,j)
    TakaYasu_ana.cal_takane_yasune_ratioDF(meigara_list,j)