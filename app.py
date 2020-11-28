from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('div', attrs={'class':'table-responsive'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
    row = table.find_all('tr')[i]

    #get date
    period = row.find_all('td')[0].text
    period = period.strip() #for removing the excess whitespace
    
    #get days
    days = row.find_all('td')[1].text
    days = days.strip() #for removing the excess whitespace
    
    #get price rate
    priceRate = row.find_all('td')[2].text
    priceRate = priceRate.strip() #for removing the excess whitespace
    
    #get notes
    notes = row.find_all('td')[3].text
    notes = notes.strip() #for removing the excess whitespace
       
    temp.append((period,days, priceRate, notes)) 
    
temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('period','days', 'priceRate', 'notes'))

#insert data wrangling here
df['period'] = df['period'].astype('datetime64')
df['days'] = df['days'].astype('category')
df['priceRate'] = df['priceRate'].str.replace(" IDR","")
df['priceRate'] = df['priceRate'].str.replace(",","")
df['priceRate'] = df['priceRate'].astype('float64')
df['priceRate'] = df['priceRate'].round(2)
df = df.set_index(['period'])

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["priceRate"].mean()}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
