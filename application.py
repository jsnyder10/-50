@app.route("/sell", methods=["GET", "POST"])
#@login_required
def sell():
    rows = db.execute("SELECT * FROM users WHERE username = :username", username="dog")
    session["user_id"] = rows[0]["id"]
    
    if request.method == "POST":
        if request.form["ticker"]:
            ticker=request.form["ticker"]
            toSell=request.form["quantity"]
            print("Ticker=",request.form["ticker"])
            print("Quantity=",toSell)
            return render_template("sold.html", ticker=ticker, toSell=toSell)
        else:
            return apology("Failed to SELL")
    elif request.method=="GET":
        shares=[]
        prices=[]
        tickers=db.execute("SELECT DISTINCT ticker FROM portfolio WHERE id = :id", id=session["user_id"])
        length=len(tickers)
        i=0
        for ticker in tickers:
            shares.append(db.execute("SELECT SUM(quantity) AS shares FROM portfolio where id=:id AND ticker=:ticker",id=session["user_id"], ticker=ticker['ticker'])[0]['shares'])
            prices.append(lookup(ticker['ticker'])['price'])
            #stockvalue.append(round(shares[i][0]['shares']*price[i]['price'],2))
            #totalstock+=stockvalue[i]
            i+=1
        return render_template("sell.html", length=length, shares=shares, tickers=tickers)
