from flask import Flask, render_template, request, redirect, session
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from bokeh.resources import CDN
from bokeh.embed import json_item
import json
from bokeh.embed import file_html

app = Flask(__name__)



@app.route('/')
def index():
  return render_template('index.html')

@app.route('/index', methods=['POST'])
def graph():
	ticker = request.form['ticker']
	api = 'T3ZQM0W3TAZKYA3N'
	URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={api}'
	r = requests.get(url=URL)
	stock_prices = r.json()
	stock_price = pd.DataFrame(stock_prices['Time Series (Daily)'])
	stock_price = stock_price.transpose()
	#stock_price['Date'] = stock_price.index
	
	p = figure(title = f'Stock prices for {ticker}', x_axis_label='Date', x_axis_type='datetime')
	dates = pd.to_datetime(stock_price.index[:30])
	#print(stock_price.iloc[:,3][:30].astype('float'))

	if 'close' in request.form.getlist('features'):
		p.line(x=dates, y=stock_price.iloc[:,3][:30].astype("float"), line_width=2, legend_label="Close")
	if 'high' in request.form.getlist('features'):
		p.line(x=dates, y=stock_price.iloc[:,1][:30].astype("float"), line_width=2, legend_label="High", line_color="green")
	if 'open' in request.form.getlist('features'):
		p.line(x=dates, y=stock_price.iloc[:,0][:30].astype("float"), line_width=2, legend_label="Open", line_color="red")
	if 'low' in request.form.getlist('features'):
		p.line(x=dates, y=stock_price.iloc[:,2][:30].astype("float"), line_width=2, legend_label="High", line_color="purple")

	
	
	#script, div = components(p)
	#return render_template('graph.html', script=script, div=div)
	return file_html(p, CDN)
	
	
	
	#return render_template("graph2.html")

if __name__ == '__main__':
  app.run(port=33507, debug=True)
