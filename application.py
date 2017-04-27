@app.route("/")
#@login_required
def index():
    rows = db.execute("SELECT * FROM users WHERE username = :username", username='dog')
    session["user_id"] = rows[0]["id"]
    
    user=db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    tickers=db.execute("SELECT DISTINCT ticker FROM portfolio WHERE id = :id", id=session["user_id"])
    shares=[]
    prices=[]
    stockvalue=[]
    totalstock=0
    totalvalue=0
    cash=user[0]['cash']
    length=len(tickers)
    for i in range(length):
        shares.append(db.execute("SELECT SUM(quantity) AS shares FROM portfolio where id=:id AND ticker=:ticker",id=session["user_id"], ticker=tickers[i]['ticker'])[0]['shares'])
        prices.append(lookup(tickers[i]['ticker'])['price'])
        stockvalue.append(shares[i]*prices[i])
        totalstock+=stockvalue[i]
        prices[i]=usd(prices[i])
        stockvalue[i]=usd(stockvalue[i])
    totalvalue=totalstock+cash
    
    if request.method == "POST":
        print("Post")
        cash=db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"][0]['cash'])
        print("cash=",cash)
        add=request.form.get("add")
        print("add=",add)
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash+add, id=session["user_id"])
        return render_template("index.html", user=user[0]['username'], tickers=tickers, length=length, shares=shares, prices=prices, cash=usd(cash), stockvalue=stockvalue, totalstock=usd(totalstock), totalvalue=usd(totalvalue))
    else:
        print("Get")
        return render_template("index.html", user=user[0]['username'], tickers=tickers, length=length, shares=shares, prices=prices, cash=usd(cash), stockvalue=stockvalue, totalstock=usd(totalstock), totalvalue=usd(totalvalue))
