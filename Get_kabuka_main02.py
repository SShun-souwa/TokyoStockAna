import time
from modules import Get_kabuka
from modules import Gene_list

Gene_list.CSVToushouMeigara()
code_list = Gene_list.GetListToushouMeigara()
day_list = Gene_list.GetListEigyoubi()
print(day_list)

for i in range (0,len(code_list)):
    if code_list[i] < 10000:
        ticker_code = str(code_list[i])
        print(ticker_code)
        Get_kabuka.GetKABU(ticker_code)
