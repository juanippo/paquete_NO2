import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# agrego opcion para que devuelva el objeto de plt?
# sm.graphics.tsa.plot_acf(df_autocor[columna], lags=22,missing='conservative') esto es mucho más cortito y quizás mas lindo pero
# no marca los significativos (para autocorr)

# date format: YYYY-MM-DD
def plot_series(df, start = pd.Timestamp.min, end = pd.Timestamp.max, filename = 'series.png', width = 15, height = 4, show = False):

	gas = 'NO2_trop'
	columna='NO2_trop_mean'
	gasname = 'NO2 troposferico'

	rango=np.logical_and(df['Fecha_datetime']>= start,df['Fecha_datetime']<=end)
	df=df[rango]

	figsize=(width,height)
	plt.close("all")
	fig, ax = plt.subplots(figsize=figsize)
	ax.plot(df.Fecha_datetime,df[columna],'ro:')
	fig.suptitle('Serie de '+gasname)
	ax.grid(axis='y',alpha=0.4)
	plt.ylabel(gasname+ ' (mol/m2)')
	
	fig.savefig(filename,bbox_inches='tight',dpi=500)
	if show:
		plt.show()


def plot_autocorr(df, lags, alpha = 0.01, width = 30, height=5, filename = 'autocorrelogram.png', show = False):

	columna='NO2_trop_mean'
	color_significativo = 'blue'
	color_no_sig = 'white'
	titulo = 'Autocorrelograma de la serie diaria'
	df_autocor=df.loc[:,['Fecha_datetime','NO2_trop_mean']]

	for i in range(lags+1):
	    df_autocor['lag_'+str(i)]=df_autocor[columna].shift(i)

	rho=[]
	pval=[]
	for i in range(lags+1):
	    lagfila='lag_'+str(i)
	    columnas=[columna,lagfila]
	    a=df_autocor[columnas]
	    b=a.dropna()._get_numeric_data()
	    rho.append(pearsonr(b[columna], b[lagfila])[0])
	    pval.append(pearsonr(b[columna], b[lagfila])[1])

	rhoenmascarado=np.copy(rho)

	for i in range(len(pval)):
	    if pval[i]>alpha:
	        rhoenmascarado[i]=0

	figsize=(width,height)
	plt.close("all")
	fig, ax = plt.subplots(figsize=figsize)
	ax.bar(np.arange(1,lags+1),rho[1:],color=color_no_sig,edgecolor='black')
	ax.bar(np.arange(1,lags+1),rhoenmascarado[1:],color=color_significativo,edgecolor=color_significativo)
	ax.grid(color='black',alpha=0.4)
	ax.set_xlabel('Lags (dias)')
	ax.set_title(titulo)

	fig.savefig(filename,bbox_inches='tight',dpi=500)
	if show:
		plt.show()

#df_m un df agrupado por mes, que contiene a ambos años enteros
def barplot_year_cmp(df_m, year1, year2, width = 10, height=4, filename='compared_series.png', show = False):

	columna = 'NO2_trop_mean'
	no2_year1 = df_m[df_m.Year==year1][columna].values
	no2_year2 = df_m[df_m.Year==year2][columna].values
	months = ['J','F','M','A','M','J','J','A','S','O','N','D']
	df_bar = pd.DataFrame({str(year1): no2_year1,str(year2): no2_year2}, index=months)

	ax = df_bar.plot.bar(rot=0,color=['r','y'],figsize=(width,height))
	plt.grid(axis='y',alpha=0.5)

	plt.savefig(filename,bbox_inches='tight',dpi=500)
	if show:
		plt.show()

def interanual_variation(df_m, year1, year2, month_num):

	columna = 'NO2_trop_mean'
	no2_year1 = df_m[df_m.Year==year1][columna].values
	no2_year2 = df_m[df_m.Year==year2][columna].values
	
	var =np.round(100*(no2_year2[month_num]-no2_year1[month_num])/no2_year1[month_num],decimals=2)
	return var
