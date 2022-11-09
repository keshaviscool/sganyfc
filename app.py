from flask import Flask, render_template, send_from_directory, request
import pymongo
import requests
import datetime
api_key = "2dfc3fb2b70149828b575e9a6a8c0c28"



app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://admin:heAaEjBCFxwNT334@cluster0.7zkgkmk.mongodb.net/?retryWrites=true&w=majority")
db = client['telegram-automated-website']

# get the collection
keywords = db["keywords"]

@app.route('/')
def hello_world():
    
    # get latest keyword
    wlnfc = keywords.find_one({"keyword": "WLNFC"}, sort=[("date", pymongo.DESCENDING)])
    wlfc = keywords.find_one({"keyword": "WLFC"}, sort=[("date", pymongo.DESCENDING)])
    wrnfc = keywords.find_one({"keyword": "WRNFC"}, sort=[("date", pymongo.DESCENDING)])
    wrfc = keywords.find_one({"keyword": "WRFC"}, sort=[("date", pymongo.DESCENDING)])
    tlnfc = keywords.find_one({"keyword": "TLNFC"}, sort=[("date", pymongo.DESCENDING)])
    tlfc = keywords.find_one({"keyword": "TLFC"}, sort=[("date", pymongo.DESCENDING)])
    trnfc = keywords.find_one({"keyword": "TRNFC"}, sort=[("date", pymongo.DESCENDING)])
    trfc = keywords.find_one({"keyword": "TRFC"}, sort=[("date", pymongo.DESCENDING)])

    # compare dates of 2 keywords and get the latest
    if wlnfc:
        if wlfc:
            if wlnfc['date'] > wlfc['date']:
                wl = wlnfc
            else:
                wl = wlfc
        else:
            wl = wlnfc
    else:
        if wlfc:
            wl = wlfc
        else:
            wl = None

        

    # if wrnfc['date'] > wrfc['date']:
    #     wr = wrnfc
    # else:
    #     wr = wrfc

    if wrnfc:
        if wrfc:
            if wrnfc['date'] > wrfc['date']:
                wr = wrnfc
            else:
                wr = wrfc
        else:
            wr = wrnfc
    else:
        if wrfc:
            wr = wrfc
        else:
            wr = None

    # if tlnfc['date'] > tlfc['date']:
    #     tl = tlnfc
    # else:
    #     tl = tlfc

    if tlnfc:
        if tlfc:
            if tlnfc['date'] > tlfc['date']:
                tl = tlnfc
            else:
                tl = tlfc
        else:
            tl = tlnfc
    else:
        if tlfc:
            tl = tlfc
        else:
            tl = None
        
    if trnfc:
        if trfc:
            if trnfc['date'] > trfc['date']:
                tr = trnfc
            else:
                tr = trfc
        else:
            tr = trnfc
    else:
        if trfc:
            tr = trfc
        else:
            tr = None

    # create final list
    final = [
        wl, wr, tl, tr
    ]
    articles = requests.get(f"https://newsapi.org/v2/everything?q=malaysia&from={datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}&sortBy=publishedAt&apiKey=2dfc3fb2b70149828b575e9a6a8c0c28").json()['articles'][:1]


    return render_template("index.html", records=final, articles=articles)

@app.route('/tnc')
def tnc():
    return render_template("tnc.html")

@app.route('/privacy-policy')
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route('/about-us')
def about_us():
    return render_template("about-us.html")

slug = {
    "malaysia-petrol": "Malaysia Petrol",
    "malaysia-ringgit": "Malaysia Ringgit",
    "malaysia-stock-index": "Malaysia Stock Index",
    "tuas-second-link": "Tuas Second Link",
}

@app.route('/news/<string:keyword>')
def news(keyword):
    articles = requests.get(f"https://newsapi.org/v2/everything?q={str(slug[keyword]).lower()}&from={datetime.datetime.now().year}-{datetime.datetime.now().month - 1}-{datetime.datetime.now().day}&sortBy=publishedAt&apiKey=2dfc3fb2b70149828b575e9a6a8c0c28").json()['articles'][:100]
    return render_template("news.html", articles = articles, title=slug[keyword], all_keywords=slug)

# site map
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    app.run(debug=True)
