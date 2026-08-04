import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mes=np.arange(1,14,1)
meses=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']

url1='https://docs.google.com/spreadsheets/d/e/2PACX-1vQZmuN0O2KSemx9d0QZT9ntJK31ZMGourGUqV4zAMG_hARMxI2U9mYK_yJSx-RjXa_QtYm-k6dm9UeG/pub?gid=0&single=true&output=csv'
url2='https://docs.google.com/spreadsheets/d/e/2PACX-1vQZmuN0O2KSemx9d0QZT9ntJK31ZMGourGUqV4zAMG_hARMxI2U9mYK_yJSx-RjXa_QtYm-k6dm9UeG/pub?gid=2093754426&single=true&output=csv'
url3='https://docs.google.com/spreadsheets/d/e/2PACX-1vQZmuN0O2KSemx9d0QZT9ntJK31ZMGourGUqV4zAMG_hARMxI2U9mYK_yJSx-RjXa_QtYm-k6dm9UeG/pub?gid=1959635478&single=true&output=csv'

df1=pd.read_csv(url1)
df2=pd.read_csv(url2)
df3=pd.read_csv(url3)

df1=df1[['Precio','Fecha','Gastos','Fecha gasto']].copy()
df2=df2[['Precio','Fecha','Envío','Gastos','Fecha gasto']].copy()
df2.loc[173:,'Precio']=df2.loc[173:,'Precio']-df2.loc[173:,'Envío']
df3=df3[['Precio','Fecha','m0','u','Envío','Gastos','Fecha gasto']].copy()

df1['Fecha']=pd.to_datetime(df1['Fecha'],dayfirst=True)
df1['Fecha gasto']=pd.to_datetime(df1['Fecha gasto'],dayfirst=True)
df2['Fecha']=pd.to_datetime(df2['Fecha'],dayfirst=True)
df2['Fecha gasto']=pd.to_datetime(df2['Fecha gasto'],dayfirst=True)
df3['Fecha']=pd.to_datetime(df3['Fecha'],dayfirst=True)
df3['Fecha gasto']=pd.to_datetime(df3['Fecha gasto'],dayfirst=True)

year1=[]
year2=[]
year3=[]

for i in mes:
    data=df1[df1['Fecha'].dt.month==np.where(mes==i)[0][0]]
    data=data.groupby('Fecha')['Precio'].sum()
    data=data.reset_index(name='Lks')
    data1=df1[df1['Fecha gasto'].dt.month==np.where(mes==i)[0][0]]
    data1=data1.groupby('Fecha gasto')['Gastos'].sum()
    data1=data1.reset_index(name='Gasto')
    data2=pd.concat([data,data1],axis=1)
    year1.append(data2)

    data_=df2[df2['Fecha'].dt.month==np.where(mes==i)[0][0]]
    data_=data_.groupby('Fecha')['Precio'].sum()
    data_=data_.reset_index(name='Lks')
    data1_=df2[df2['Fecha gasto'].dt.month==np.where(mes==i)[0][0]]
    data1_=data1_.groupby('Fecha gasto')['Gastos'].sum()
    data1_=data1_.reset_index(name='Gasto')
    data2_=pd.concat([data_,data1_],axis=1)
    year2.append(data2_)

    data__=df3[df3['Fecha'].dt.month==np.where(mes==i)[0][0]]
    data__=data__.groupby('Fecha')['Precio'].sum()
    data__=data__.reset_index(name='Lks')
    data1__=df3[df3['Fecha gasto'].dt.month==np.where(mes==i)[0][0]]
    data1__=data1__.groupby('Fecha gasto')['Gastos'].sum()
    data1__=data1__.reset_index(name='Gasto')
    data2__=pd.concat([data__,data1__],axis=1)
    year3.append(data2__)
    
year1.pop(0)
year2.pop(0)
year3.pop(0)

for i in range(0,12):
    dat=year1[i]
    dat_=year2[i]
    dat__=year3[i]

    dat_['Fecha']=dat_['Fecha'].apply(lambda x:x if x.month!=2 or x.day<=28 else x.replace(day=28))
    dat_['Fecha']=dat_['Fecha'].apply(lambda x:x.replace(year=2023))
    dat__['Fecha']=dat__['Fecha'].apply(lambda x:x.replace(year=2023))

    start_date=dat['Fecha'].min().replace(day=1)
    end_date=pd.date_range(start=start_date,periods=1,freq='ME')[0]

    x_full_range=pd.date_range(start=start_date,end=end_date)

    d=dat.set_index('Fecha').reindex(x_full_range,fill_value=0)
    d_=dat_.set_index('Fecha').reindex(x_full_range,fill_value=0)
    d__=dat__.set_index('Fecha').reindex(x_full_range,fill_value=0)

    ing_men1=np.sum(year1[i]['Lks'])
    ing_men2=np.sum(year2[i]['Lks'])
    ing_men3=np.sum(year3[i]['Lks'])

    plt.figure(figsize=(7,4))
    plt.plot(d.index,d['Lks'],label=f'Lks2023: {ing_men1}',marker='o',color='blue')
    plt.plot(d_.index,d_['Lks'],label=f'Lks2024: {ing_men2}',marker='o',color='red')
    plt.plot(d__.index,d__['Lks'],label=f'Lks2025: {ing_men3}',marker='o',color='orange')
    plt.title(f'Balance mensual (Mes {i+1})')
    plt.xlabel('Fecha')
    plt.ylabel('Lks')
    plt.grid()
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'm{i+1}')

y1=pd.concat(year1,axis=0).sort_values(by='Fecha')
y2=pd.concat(year2,axis=0).sort_values(by='Fecha')
y3=pd.concat(year3,axis=0).sort_values(by='Fecha')

y1=y1.set_index('Fecha')
y2=y2.set_index('Fecha')
y3=y3.set_index('Fecha')

date_range=pd.date_range(start='2023-01-01',end='2023-12-31')
y1=y1.reindex(date_range,fill_value=0)
y2=y2.reindex(date_range,fill_value=0)
y3=y3.reindex(date_range,fill_value=0)

plt.figure(figsize=(10,4))
plt.plot(y1.index,y1['Lks'],'b-',label='2023')
plt.plot(y2.index,y2['Lks'],'r-',label='2024')
plt.plot(y3.index,y3['Lks'],'-',label='2025',color='orange')

plt.title('Comparación anual',fontsize=14)
plt.xlabel('Fecha',fontsize=14)
plt.ylabel('Lks',fontsize=14)
plt.grid()
plt.xticks(pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME'), rotation=90)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig("2023_2024_2025.png")