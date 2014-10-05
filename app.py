# -*- coding: utf-8 -*-

import os, requests
from bs4 import BeautifulSoup

from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.args.get('q'):
        q = request.args.get('q')
    else:
        q = ""
    google_search = 'https://www.google.com/search?hl=zh-CN&q=site:weibo.com+' + q
    
    # dict
    result = {}
    
    # requests
    r = requests.get(google_search)
    
    # beautifulsoup
    html_doc = r.text
    
    soup = BeautifulSoup(html_doc)
    h3 = soup.find_all("h3")
    for a in h3:
        result[a.find('a').get('href')] = a.find('a').get_text()
    
    # template
    return render_template(
        'index.html',
        result=result,
        google_search=google_search,
        q=q,
        active='index'
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        active='about'
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

