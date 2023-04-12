
ExploreVec = []
ExploreVec.append({
    "Q": "which large cap has high low range twice larger than 10 day average?",
    "A": '{"Date":"today", "Expr": "marketcap(t=daily)>8200&h(t=day,n=0)-l(t=day,n=0)>2*(h(t=day,n=10,s=mean)-l(t=day,n=10,s=mean))"}'
})

ExploreVec.append({
    "Q": "which mid cap stocks gain more than 5% on Apr 3, 2023?",
    "A": '{"Date":"2023-04-03", "Expr": "marketcap(t=daily)>100&marketcap(t=daily)<8200&c(t=day,n=0)/c(t=day,n=1)-1>0.05"}'
})

ExploreVec.append({
    "Q": "just as an experiment, now define maq as minimal of 1. log of market cap to the power of 2, 2. fourth root of volume. I want stock with maq larger than 30",
    "A": '{"Date":"today", "Expr": "min(log10(marketcap(t=daily))^2, qlmt(t=day,n=0)^(1/4))>30"}'
})

ExploreVec.append({
    "Q": "small cap with 5 fold increase in volume vs 20 day average",
    "A": '{"Date":"today", "Expr": "marketcap(t=daily)<100&qlmt(t=day,n=0)/qlmt(t=day,n=20)>5"}'
})

ExploreVec.append({
    "Q": "list small cap meme stocks",
    "A": 'Sorry, I cannot provide an answer to that question as the database does not have data for meme stocks yet.'
})

ExploreVec.append({
    "Q": "I maintain the database and has added column idx under table meme, where 1 is for meme stocks. list small cap meme stocks",
    "A": '{"Date":"today", "Expr": "marketcap(t=daily)<100&idx(t=meme,n=0)=1"}'
})

ExploreVec.append({
    "Q": "big cap with close price max drawdown more than 10% in last 20 days",
    "A": '{"Date":"today", "Expr": "marketcap(t=daily)>8200&c(t=day,n=020,s=mdd)<-0.1"}'
})

ExploreVec.append({
    "Q": "which larget cap stocks has low below 20 days low today?",
    "A": '{"Date":"today", "Expr": "marketcap(t=daily)>8200&l(t=day)<l(t=day,n=20,s=min)"}'
})

ExploreVec.append({
    "Q": "how are things going?",
    "A": 'Sorry, that is not a relevant question. Please provide a valid query in the format specified.'
})

ExploreVec.append({
    "Q": "stocks making 20 day new high",
    "A": '{"Date":"today", "Expr": "h(t=day,n=0)>h(t=day,n=20,s=max)"}'
})

ExploreVec.append({
    "Q": "which display unusual high volume on Apr 5, 2023?",
    "A": '{"Date":"2023-04-05", "Expr": "qlmt(t=day,n=0)>qlmt(t=day,n=20,s=mean)*10"}'
})

ExploreVec.append({
    "Q": "big cap stock making 5 day new high on 23/04/03",
    "A": '{"Date":"2023-04-03", "Expr": "marketcap(t=daily)>8200&h(t=day,n=0)>h(t=day,n=5,s=max)"}'
})

ExploreVec.append({
    "Q": "which small cap stock has 9 day sma cross above 20 day sma today?",
    "A": '{"Date":"today", "Expr": "marketcap(t=daily)<100&c(t=day,n=9,s=mean)<c(t=day,n=20,s=mean)&c(t=day,n=09,s=mean)>c(t=day,n=020,s=mean)"}'
})

ExploreDict = {item["Q"]: item["A"] for item in ExploreVec}
