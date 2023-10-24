import pandas as pd

df_codes = pd.read_csv('./true_code.csv')

for type_csv in ['PN']:
  for i in range(2012,2021):
    df = pd.read_csv('../dataCorrectedCSV/Services '+type_csv+' '+str(i)+'.csv')
    df['new_type'] = 'Autres'
    for index, row in df.iterrows():
      row['code'] = row['code'].strip()
      value = row['code']
      try:
        # row['new_type'] = df_codes[value]
        df.at[index,'new_type'] = df_codes[value]
      except:
        df.at[index,'new_type'] = 'Autres'
        # row['new_type'] = 'Autres'
        
        
    df.to_csv('./maximeCleanData/Services '+type_csv+' '+str(i)+'.csv')
  
    
  
  