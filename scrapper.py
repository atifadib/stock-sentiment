from flask import Flask,render_template
from datetime import time
app=Flask(__name__,template_folder=r'C:\Users\ATIF ADIB\Desktop\wealth_management\myflaskapp\template')

@app.route('/')
def index():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                        61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                        70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = [time(hour=11, minute=14, second=15),
                 time(hour=11, minute=14, second=30),
                 time(hour=11, minute=14, second=45),
                 time(hour=11, minute=15, second=00),
                 time(hour=11, minute=15, second=15),
                 time(hour=11, minute=15, second=30),
                 time(hour=11, minute=15, second=45),
                 time(hour=11, minute=16, second=00),
                 time(hour=11, minute=16, second=15),
                 time(hour=11, minute=16, second=30),
                 time(hour=11, minute=16, second=45),
                 time(hour=11, minute=17, second=00),
                 time(hour=11, minute=17, second=15),
                 time(hour=11, minute=17, second=30),
                 time(hour=11, minute=17, second=45),
                 time(hour=11, minute=18, second=00),
                 time(hour=11, minute=18, second=15),
                 time(hour=11, minute=18, second=30)]
    return render_template('index.html', values=temperatures, labels=times, legend=legend, users=users)
    #return render_template('index.html')

@app.route('/about_us')
def about():
    return render_template('about_us.html')

if(__name__=="__main__"):
    app.run()
