import pandas as pd
import numpy as np
import random

COLS = ['drwtNo1', 'drwtNo2', 'drwtNo3', 'drwtNo4', 'drwtNo5', 'drwtNo6']
# COLS = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth'] 

TARGET_NUMBER = 141

class Lucky():

    def __init__(self,fname):
        self._df = self.get_file(fname)

    def get_df(self):
        return self._df

    def get_file(self, fname):
        df = pd.read_csv(fname)
        return df

    def make_cycle_count(self, df, cycle=3):

        result_arr = []
        for i in range(len(df)):
            result_dict = {}
            for col_number in range(1, 46):
                result_dict[col_number] = 0

            for col in COLS:
                value_counts = df[i:i+cycle][col].value_counts()
                value_dict = value_counts.to_dict()
                for key in value_dict.keys():
                    result_dict[key] += value_dict[key]
            result_arr.append(result_dict)

        tmp1 = pd.DataFrame([result_arr[0]])
        for r_a in result_arr[1:]:
            tmp1 = tmp1.append(r_a, ignore_index=True)

        return tmp1

    def get_count_zero(self,df=None):

        if df is None:
            df = self._df

        tmp_df = self.make_cycle_count(df,10)

        arr_count_zero = [[0 for col in range(45)] for row in range(len(tmp_df))]

        for col in range(1,46):
            count = 0
            for i in tmp_df.index:
                val = tmp_df._get_value(i,col)
                if val == 0:
                    count += 1
                else:
                    if count !=0:
                        arr_count_zero[col-1][count] += 1
                    count = 0

        for i in arr_count_zero :
            for j in i:
                print(j,end=" ")
            print()

    def get_ma(self, df=None):

        if df is None:
            df = self._df

        tmp_df = df.drop(columns=['title'])

        MIN = 9999
        MAX = -1

        for i in range(1, 4):
            tmp_number = 141 * (i * 2 + 1) - (tmp_df[0:i * 2].sum(axis=1).sum())
            if i == 1:
                MIN = MAX = tmp_number
            if (tmp_number > MAX):
                MAX = tmp_number
            elif (tmp_number < MIN):
                MIN = tmp_number
            print(f'min={MIN}, max={MAX}')

        return (MIN,MAX)

    def draw_lucky_number(self):
        arr = []

        while True:
            num = random.randint(1, 45)
            if num not in arr:
                arr.append(num)
            if len(arr) == 6:
                break

        return sorted(arr)

    def draw_lucky_number_using_ma(self, df=None, na=1):

        result_arr = []
        count_na = 0
        all_retry_count = 0

        if df is None:
            df = self._df

        min, max = self.get_ma()

        while 1:

            if(na == count_na):
                break
            draw_number = self.draw_lucky_number()
            sum_draw_number = sum(draw_number)
            all_retry_count +=1

            if sum_draw_number >= min and sum_draw_number <=max:
                count_na += 1
                result_arr.append(draw_number)

        return result_arr, all_retry_count



fname = 'lotto-winning-numbers.csv'

from GetWinningNumbers import Lotto

lotto = Lotto()
lotto.get_range_lottoDrwNum(start=600)
lotto.update_csv(fname)


lucky = Lucky(fname)

df = lucky.get_df()

lucky_numbers,a_r_c = lucky.draw_lucky_number_using_ma(na=20)
print (lucky_numbers)
print (f'총 시도횟수 : {a_r_c}')

tmp_df = lucky.make_cycle_count(df,cycle=12)

lucky_numbers_dict = {}
for l_number in lucky_numbers:

    tmp_score = 0

    for i in l_number:
        t = tmp_df[i][0:3].mean()
        f = tmp_df[i][0:5].mean()
        s = tmp_df[i][0:7].mean()

        tmp_score += s

        if s<f and f<t:
            tmp_score += t-s

    lucky_numbers_dict[round(tmp_score,2)] = l_number


sorted_keys = sorted(lucky_numbers_dict.keys(),reverse=True)

for sorted_key in sorted_keys:
    print (f'점수: {sorted_key} // 번호 {lucky_numbers_dict[sorted_key]}')

# tmp_df.to_csv('20210401_test_v0.2.csv')


# print (lucky.draw_lucky_number())
# df = lucky.get_file(fname)

# lucky.get_cycle_count(df,5)


# print (len(df))
# for i in range(len(df)):
#     print (f'{i}:{i+11}')

# for i in range(1,46):
#     print ("'"+str(i)+"',",end=' ')
'''
result_df = None

for i in range(0,3):
# for i in range(len(df)):

    result_dict = {}
    for col_number in range(1, 46):
        result_dict[col_number] = 0

    for col in COLS:
        value_counts = df[i:i+11][col].value_counts()
        value_dict = value_counts.to_dict()
        for key in value_dict.keys():
            result_dict[key] += value_dict[key]

    print (result_dict)

    if result_df is None:
        print (f'{i} none')
        result_df = pd.DataFrame([result_dict])
    else:
        print (f'{i} not none')
        print (result_df)
        result_df.append(result_dict,ignore_index=True)

print (result_df)



tmp1 = pd.DataFrame([result_dict])
tmp2 = pd.DataFrame.append(result_dict,  ignore_index=True)
print(tmp1)

print (type(tmp1))

print (tmp1.append(result_dict, ignore_index=True))
'''