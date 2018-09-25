import pandas as pd

files = 9

df=pd.DataFrame();

for x in range(0, files+1):
    name = "Day_" + str(x) + ".xlsx"
    interm = pd.read_excel(name, sheet_name='sheet1')
    if x!=0:
        interm.drop(interm.index[0])
    df = pd.concat([df, interm])
    
df = df.reset_index()
del df['index']
df.to_excel("Overall.xlsx", sheet_name='sheet1', index=False)
print("Done")
