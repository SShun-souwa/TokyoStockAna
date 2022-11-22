import pandas as pd


data_input = pd.read_csv(filepath_or_buffer="I:\投資資料\個人的な分析\プログラム\個別銘柄分析\sp500.csv",
                         encoding="ms932",
                         sep=",")

data_input["datetime"] = pd.to_datetime(data_input["datetime"]).dt.strftime("%Y-%m-%d")
date_list = data_input["datetime"].to_list()

data_input = data_input.set_index("datetime")
data_input = data_input["1950-01-01":"2022-02-24"]
data_input["close"] = data_input["close"].replace(',', '').astype(float)
close_list = data_input["close"].to_list()


takayasu = {}
for i in date_list:
    takayasu[i] = [0,0]

takanecount = []
yasunecount = []

for i in range (0,len(close_list)):

    if i > 52:
        kaisi = i - 52
        high = 0.0
        count = 0
        for j in range (kaisi,i):
            if close_list[j] > high:
                high = close_list[j]

        for j in range (kaisi,i):
            if close_list[i] > high:
                count = 1

        takanecount.append(count)
    else:
        takanecount.append(0)

for i in range (0,len(close_list)):

    if i > 52:
        kaisi = i - 52
        low = 100000000000
        count = 0
        for j in range (kaisi,i):
            if close_list[j] < low:
                low = close_list[j]

        for j in range (kaisi,i):
            if close_list[i] < low:
                count = 1

        yasunecount.append(count)
    else:
        yasunecount.append(0)

data_input["takane"] = takanecount
data_input["yasune"] = yasunecount
touraku = []
d = data_input.to_dict(orient='index')

inde = 0

for i in range (0,len(yasunecount)):

    if yasunecount[i] == 1:

        for j in range(0,i):
           if takanecount[j] == 1:
                 inde = j

        touraku.append(close_list[i]/close_list[inde])

    else:touraku.append(0)

data_input["gerakuritu"] = touraku
data_input = data_input.reset_index()
date_list = data_input["datetime"].to_list()

gerakubi = []

for i in range (0,len(touraku)):

    if touraku[i] > 0:
      if 0.8 < touraku[i] < 0.9:

         gerakubi.append(date_list[i])

with open('I:\投資資料\個人的な分析\プログラム\個別銘柄分析\gerakubi10-20.txt', 'w') as f:
    for d in gerakubi:
        f.write("%s\n" % d)

sagehaba = []

for i in range (0,len(takanecount)):
    if takanecount[i] == 1:
        for j in range (i,len(close_list)):
            if 0.8 < close_list[j] / close_list[i] <= 0.9:
             sagehaba.append(date_list[j])
             break

sagehaba = list(dict.fromkeys(sagehaba))

with open('I:\投資資料\個人的な分析\プログラム\個別銘柄分析\sagehaba10-20.txt', 'w') as f:
    for d in sagehaba:
        f.write("%s\n" % d)

data_input.to_csv("I:\投資資料\個人的な分析\プログラム\個別銘柄分析\sp500new.csv", index=False, encoding='cp932')