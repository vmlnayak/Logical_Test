#!/usr/bin/env python
# coding: utf-8

# In[23]:


# importing libraries(in case to install manually use pip install pandas from console)
import pandas as pd
import datetime

# read data from csv file keep the file in the same location with python main file else specify the full path
df = pd.read_csv('test.csv')

# preprocessing of data 
df1=df
df1['date']=pd.to_datetime(df1.date, dayfirst=True)
df1=df1.sort_values('date')

#performing logical operation to create new column of final_value
final_value = []

for index, row in df1.iterrows():
    if row['value_overlayed'] == 'Y':
        final_value.append(150)
    else:
        if row['element'] == 'A':
            # print(row['element'], row['value'], row['date'])
            d1=row['date'].date()

            date_1yr_ago  = datetime.date(d1.year-1, d1.month, d1.day)
            local_A = df1[(df1['date'] < row['date']) & (row['date'] > date_1yr_ago) & (df1['element'] == 'A') & (df1['value_overlayed'] == 'Y')]
            row_A = local_A[local_A.date == local_A.date.min()]
            # Parametes calculation and appending to a list for element A
            F_A_value = row_A['value'].tolist()
            T_A_value = row['value']
            if F_A_value == []:
                final_value.append(row['value'])
            else:
                previous_date = (row_A['date'].tolist())[0].date()
                current_date = row['date'].date()
                n = (current_date - previous_date).days
                result = int(T_A_value - (((F_A_value[0]-150)/365)*(365-n)))
                final_value.append(result)        
        else:
            # print(row['element'], row['value'], row['date'])
            d1=row['date'].date()
            date_1yr_ago  = datetime.date(d1.year-1, d1.month, d1.day)
            local_B = df1[(df1['date'] < row['date'] ) & (row['date'] > date_1yr_ago) & (df1['element'] == 'B') & (df1['value_overlayed'] == 'Y')]
            row_B = local_B[local_B.date == local_B.date.min()]
            # Parametes calculation and appending to a list for element A
            F_B_value = row_B['value'].tolist()
            T_B_value = row['value']
            if F_B_value == []:
                final_value.append(row['value'])
            else:
                previous_date = (row_B['date'].tolist())[0].date()
                current_date = row['date'].date()
                n = (current_date - previous_date).days
                result = round(int(T_B_value - (((F_B_value[0]-150)/365)*(365-n))))
                final_value.append(result)

# preparing final_value column
df1['final_value']= final_value

#resetting of index
df1.reset_index(drop=True, inplace=True)

#exporting file to csv format
df1.to_csv('output.csv',index=False)
