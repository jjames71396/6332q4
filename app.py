from flask import Flask, render_template, jsonify
import pandas as pd

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

counts = dict()
data = None
scatters = False

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
    global counts
    global data
    global scatters
    scatters = False
    arg = request.form.get('name')
    print(arg)
    args = arg.split(',')
    if len(args) < 3 or len(args) >15:
        return render_template('index.html')
    counts = dict()
    for i in args:
      b = i.split(' ')
      counts[b[0]] = counts.get(b[0], 0) + int(b[1])
    data = pd.DataFrame(counts.items(), columns=['Letter', 'Value'])
    
    
    total_values = data['Value'].sum()
    data['Percentage'] = round((data['Value'] / total_values) * 100,2)
    data = data.sort_values('Value')
    return render_template('horizontal.html')
    
@app.route('/pie', methods=['GET', 'POST'])
def pie():
    global counts
    global data
    global scatters
    scatters = False
    arg = request.form.get('name')
    args = arg.split(',')
    if len(args) < 3 or len(args) >15:
        return render_template('index.html')
    counts = dict()
    for i in args:
      b = i.split(' ')
      counts[b[0]] = counts.get(b[0], 0) + int(b[1])
    data = pd.DataFrame(counts.items(), columns=['Letter', 'Value'])
    
    
    total_values = data['Value'].sum()
    data['Percentage'] = round((data['Value'] / total_values) * 100,2)
    
    return render_template('pie.html')
    
@app.route('/scatter', methods=['GET', 'POST'])
def scatter():
    global counts
    global data
    global scatters
    scatters = True
    arg = request.form.get('name')
    print(arg)
    args = arg.split(',')
    if len(args) >10:
        return render_template('index.html')
    counts = dict()
    data = pd.DataFrame()
    
    for j,i in enumerate(args):
      b = i.split(' ')
      if j == 0:
          dict1 = {'x': int(b[0]),
            'y': int(b[1]),
            'c': int(b[2])
          }
          data = pd.DataFrame(dict1, index=[0])
      else:
        data.loc[len(data.index)] = [int(b[0]), int(b[1]), int(b[2])] 
          
    return render_template('scatter.html')

@app.route('/line', methods=['GET', 'POST'])
def line():
    return render_template('line_scatter.html')
    
@app.route('/data')
def get_data():
    global scatters
    if not scatters:
        pie_chart_data = [{'label': row['Letter'], 'value': row['Value'], 'percent': row['Percentage']} for _, row in data.iterrows()]
        bar_chart_data = [{'label': row['Letter'], 'value': row['Value'], 'percent': row['Percentage']} for _, row in data.iterrows()]
        chart_data = {
            'bar_chart': bar_chart_data,
            'pie_chart': pie_chart_data
        }
    else:
        scatter_plot_data = []
        for i, row in enumerate(data.iterrows()):
            scatter_plot_data.append({'x': int(row[1]['x']), 'y': int(row[1]['y']), 'c': int(row[1]['c'])})
        chart_data = {
            'scatter_plot': scatter_plot_data
        }
    

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
