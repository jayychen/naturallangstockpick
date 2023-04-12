
ExploreDict = {
    "which large cap has high low range twice larger than 10 day average?":
    '{"Date":"today", "Expr": "marketcap(t=daily)>8200&h(t=day,n=0)-l(t=day,n=0)>2*(h(t=day,n=10,s=mean)-l(t=day,n=10,s=mean))"}',

    "which mid cap stocks gain more than 5% on Apr 3, 2023?":
    '{"Date":"2023-04-03", "Expr": "marketcap(t=daily)>100&marketcap(t=daily)<8200&c(t=day,n=0)/c(t=day,n=1)-1>0.05"}',

    "small cap with 5 fold increase in volume vs 20 day average":
    '{"Date":"today", "Expr": "marketcap(t=daily)<100&qlmt(t=day,n=0)/qlmt(t=day,n=20)>5"}',

    "list small cap meme stocks":
    'Sorry, I cannot provide an answer to that question as the database does not have data for meme stocks yet.',

    "I maintain the database and has added column idx under table meme, where 1 is for meme stocks. list small cap meme stocks":
    '{"Date":"today", "Expr": "marketcap(t=daily)<100&idx(t=meme,n=0)=1"}',

    "big cap with large percent of trading from institutions":
    'I\'m sorry, I cannot provide an answer as the requested table/column "institutional trading" is not in the database and not supported by the translator.',

    "big cap with close price max drawdown more than 10% in last 20 days":
    '{"Date":"today", "Expr": "marketcap(t=daily)>8200&c(t=day,n=020,s=mdd)<-0.1"}',

    "which larget cap stocks has low below 20 days low today?":
    '{"Date":"today", "Expr": "marketcap(t=daily)>8200&l(t=day)<l(t=day,n=20,s=min)"}',

    "how are things going?":
    'Sorry, that is not a relevant question. Please provide a valid query in the format specified.',

    "stocks making 20 day new high":
    '{"Date":"today", "Expr": "h(t=day,n=0)>h(t=day,n=20,s=max)"}',

    "which display unusual high volume on Apr 5, 2023?":
    '{"Date":"2023-04-05", "Expr": "qlmt(t=day,n=0)>qlmt(t=day,n=20,s=mean)*10"}',

    "big cap stock making 5 day new high on 23/04/03":
    '{"Date":"2023-04-03", "Expr": "marketcap(t=daily)>8200&h(t=day,n=0)>h(t=day,n=5,s=max)"}',

    "which small cap stock has 9 day sma cross above 20 day sma today?":
    '{"Date":"today", "Expr": "marketcap(t=daily)<100&c(t=day,n=9,s=mean)<c(t=day,n=20,s=mean)&c(t=day,n=09,s=mean)>c(t=day,n=020,s=mean)"}'
}
