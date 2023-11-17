# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np

# %%
#df = pd.read_excel('test_df.xlsx', index_col = 0)
t = pd.read_excel('test.xlsx', sheet_name = 'Sheet2', index_col = 0)


# %%
def days_buying_by_row(r):
    df = pd.DataFrame(r)
    df = df.rename(columns = {df.columns[0]: 'c'})
    df = df.iloc[::-1].reset_index(drop = True)
    df['row_1_zero_index'] = (df.index + 1) * (df['c'] == 0)
    days_buying = df.loc[df['row_1_zero_index'] > 0, 'row_1_zero_index'].min() - 1
    if np.isnan(days_buying):
        days_buying = df.shape[0]        
    return days_buying


# %%
def get_days_buying(df):
    tmp = pd.DataFrame()
    for r in df.index:
        tmp.loc[r, 'days_buying'] = days_buying_by_row(df.loc[r])
    return tmp


# %%
get_days_buying(t)


# %%
def zero_days_by_row(r):
    df = pd.DataFrame(r)
    df = df.rename(columns = {df.columns[0]: 'c'})
    df = df.iloc[::-1].reset_index(drop = True)
    df['row_zero_index'] = (df.index + 1) * (df['c'] != 0)
    res = df.loc[df['row_zero_index'] != 0, 'row_zero_index'].min() - 1
    if np.isnan(res):
        res = df.shape[0]        
        
    return res

zero_days_by_row(t.iloc[0])


# %%
def get_zero_days(df):
    tmp = pd.DataFrame()
    for r in df.index:
        tmp.loc[r, 'zero_days'] = zero_days_by_row(df.loc[r])
    return tmp

get_zero_days(t)


# %%
def zero_days_before_yesterday_by_row(r):
    df = pd.DataFrame(r)
    df = df.rename(columns = {df.columns[0]: 'c'})
    df = df.iloc[::-1].iloc[1:, :].reset_index(drop = True)
    df['row_zero_index'] = (df.index + 1) * (df['c'] != 0)
    res = df.loc[df['row_zero_index'] != 0, 'row_zero_index'].min() - 1
    if np.isnan(res):
        res = df.shape[0]        
        
    return res

zero_days_before_yesterday_by_row(t.iloc[0])


# %%
def get_zero_days_before_yesterday(df):
    tmp = pd.DataFrame()
    for r in df.index:
        tmp.loc[r, 'zero_days_before_yesterday'] = zero_days_before_yesterday_by_row(df.loc[r])
    return tmp

get_zero_days_before_yesterday(t)


# %%
def days_buying_before_yesterday_by_row(r):
    df = pd.DataFrame(r)
    df = df.rename(columns = {df.columns[0]: 'c'})
    df = df.iloc[::-1]
    df = df.iloc[1:, :].reset_index(drop = True)
    df['row_1_zero_index'] = (df.index + 1) * (df['c'] == 0)
    days_buying = df.loc[df['row_1_zero_index'] > 0, 'row_1_zero_index'].min() - 1
    if np.isnan(days_buying):
        days_buying = df.shape[0]        
    return days_buying


# %%
def get_days_buying_before_yesterday_by_row(df):
    tmp = pd.DataFrame()
    for r in df.index:
        tmp.loc[r, 'days_buying_before_yesterday'] = days_buying_before_yesterday_by_row(df.loc[r])
    return tmp


# %%
get_days_buying_before_yesterday_by_row(t)


# %%
def avg_by_row(r):
    df = pd.DataFrame(r)
    df = df.rename(columns = {df.columns[0]: 'c'}).iloc[::-1].iloc[1:, :]
    avg = df['c'].mean()
    return avg

avg_by_row(t.iloc[6])


# %%
def get_avg_by_row(df):
    tmp = pd.DataFrame()
    for r in df.index:
        tmp.loc[r, 'avg_by_row'] = avg_by_row(df.loc[r])
    return tmp

get_avg_by_row(t)


# %%
def avg_by_non_zero_by_row(r):
    df = pd.DataFrame(r)
    df = df.rename(columns = {df.columns[0]: 'c'}).iloc[::-1].iloc[1:, :]
    avg = df.loc[df['c']>0, 'c'].mean()
    if np.isnan(avg):
        avg = 0
    return avg
avg_by_non_zero_by_row(t.iloc[0])


# %%
def get_avg_by_non_zero_by_row(df):
    tmp = pd.DataFrame()
    for r in df.index:
        tmp.loc[r, 'avg_by_nonzero_row'] = avg_by_non_zero_by_row(df.loc[r])
    return tmp

get_avg_by_non_zero_by_row(t)


# %%
#is zero yesterday

# %%
def is_zero_yesterday(df):
    tmp = pd.DataFrame()
    tmp['is_zero_yesterday'] = df.iloc[:, -1] == 0
    return tmp['is_zero_yesterday']


# %%
t

# %%
is_zero_yesterday(t)


# %%
# share... + numbers_of_days_buying_before_yesterday and 

# %%
def stat_of_days_buying_before_yesterday(df):
    n_rows = len(df.index)
    df = df.iloc[:, :-1].T
    tmp = df > 0
    tmp.loc['share_non_zero_days']     = tmp.iloc[:n_rows+1, :].mean()
    tmp.loc['number_of_non_zero_days'] = tmp.iloc[:n_rows+1, :].sum()
    tmp.loc['number_of_days']          = tmp.iloc[:n_rows+1, :].count()
    ttmp = tmp.T
    ttmp['zero_days_stat'] = (
        '['
        +ttmp['number_of_non_zero_days'].astype(str)
        +'/'
        +ttmp['number_of_days'].astype(str)
        +']'
    )
    return ttmp[[
        'share_non_zero_days', 
    #    'number_of_days', 
    #    'number_of_non_zero_days', 
        'zero_days_stat'
    ]]
    
stat_of_days_buying_before_yesterday(t)

# %%
#alerts

# %%
tt = (
    t
    .join(get_days_buying(t))
    .join(get_days_buying_before_yesterday_by_row(t))
    .join(get_avg_by_row(t))
    .join(get_avg_by_non_zero_by_row(t))
    .join(is_zero_yesterday(t))
    .join(get_zero_days(t))
    .join(get_zero_days_before_yesterday(t))
    .join(stat_of_days_buying_before_yesterday(t))
)

tt

# %%
#set rules

# %%
#### partner X stop bying

print('Вывожу статистику партнёров, которые ранее были, а вчера исчезли:')
stop_buying_df = tt.query('is_zero_yesterday == True & zero_days_before_yesterday == 0')

for r in stop_buying_df.index:
    days_buying_before_yesterday = tt.loc[[r], 'days_buying_before_yesterday'][0]
    share_non_zero_days = tt.loc[[r], 'share_non_zero_days'][0]
    avg_by_nonzero_row = tt.loc[[r], 'avg_by_nonzero_row'][0]
    stat_of_days_buying_before_yesterday = tt.loc[[r], 'zero_days_stat'][0]

    print(
        ''
        + 'Партнёр ' 
        + r 
        + ', работал ' 
        + str(int(days_buying_before_yesterday)) 
        + ' дня до того, как пропасть. За период брал ' 
        + str(share_non_zero_days * 100) 
        + '% дней '
        + stat_of_days_buying_before_yesterday
        + ' в среднем по ' 
        + str(round(avg_by_nonzero_row, 1)) 
        + ' за день.'
    )

print('Job done!!!')

# %%
