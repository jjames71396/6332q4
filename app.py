from flask import Flask, render_template, jsonify
import pandas as pd

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

counts = dict()
data = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vert', methods=['GET', 'POST'])
def vert():
    global counts
    global data
    arg = request.form.get('name')
    print(arg)
    args = arg.split(' ')
    if len(args) < 3 or len(args) >17:
        return render_template('index.html')
    counts = dict()
    for i in args:
      counts[i] = counts.get(i, 0) + 1
    data = pd.DataFrame(counts.items(), columns=['Letter', 'Value'])
    
    
    total_values = data['Value'].sum()
    print(total_values)
    data['Percentage'] = round((data['Value'] / total_values) * 100,2)
    print(data['Percentage'][0])
    print(data.head())
    
    return render_template('vertical.html')
    
@app.route('/horiz', methods=['GET', 'POST'])
def horiz():
    return render_template('horizontal.html')
    
@app.route('/pie', methods=['GET', 'POST'])
def pie():
    global counts
    global data
    arg = request.form.get('name')
    print(arg)
    args = arg.split(' ')
    if len(args) < 3 or len(args) >17:
        return render_template('index.html')
    counts = dict()
    for i in args:
      counts[i] = counts.get(i, 0) + 1
    data = pd.DataFrame(counts.items(), columns=['Letter', 'Value'])
    
    
    total_values = data['Value'].sum()
    print(total_values)
    data['Percentage'] = round((data['Value'] / total_values) * 100,2)
    print(data['Percentage'][0])
    print(data.head())
    
    return render_template('pie.html')
    
@app.route('/scatter', methods=['GET', 'POST'])
def scatter():
    return render_template('scatter.html')

@app.route('/line', methods=['GET', 'POST'])
def line():
    return render_template('line_scatter.html')
    
@app.route('/data')
def get_data():
    # Load the data from a CSV file or any other source
    #data = pd.read_csv("city.csv")
    # Perform any necessary data preprocessing
    
    pie_chart_data = [{'label': row['Letter'], 'value': row['Value'], 'percent': row['Percentage']} for _, row in data.iterrows()]
    bar_chart_data = [{'label': row['Letter'], 'value': row['Value'], 'percent': row['Percentage']} for _, row in data.iterrows()]

    #state_populations = data.groupby('State')['Population'].sum().reset_index()
    #state_populations = state_populations[state_populations['Population'] > 2500000]
    #total_population = state_populations['Population'].sum()
    #state_populations['Percentage'] = round((state_populations['Population'] / total_population) * 100,2)
    # Convert the data to a format suitable for D3.js
    #bar_chart_data = [{'label': row['State'], 'value': row['Population']} for _, row in state_populations.iterrows()]
    #pie_chart_data = [{'label': row['State'], 'value': row['Percentage']} for _, row in state_populations.iterrows()]
    #scatter_plot_data = [{'x': i+1, 'y': row[1]['Population']} for i, row in enumerate(state_populations.iterrows())]
    # Prepare the data to be sent as JSON
    chart_data = {
        'bar_chart': bar_chart_data,
        'pie_chart': pie_chart_data,
        #'scatter_plot': scatter_plot_data
    }

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
