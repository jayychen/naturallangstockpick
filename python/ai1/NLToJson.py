import openai
import os
import argparse
openai.api_key = os.getenv("OPENAI_API_KEY")
# logging
import logging
log_fname = '/tmp/ai1-query-hist.log'
logging.basicConfig(filename=log_fname, filemode='a',
                    level=logging.INFO, format='%(asctime)s: %(message)s')

Role = """
You are a very cautious natural language to json translator
"""

# Be extremely cautious. DO NOT use unspecificed tables and columns. Return short error stating requested table/column not in database.
MsgHead = """
Return json in following format: {"Date":"xxx", "Expr": "xxx"}. 
Date is either in YYYY-MM-DD format, or today.
Expr is an expression composed of tokens and common math operations of tokens are supported. eg. log10({token1}/{token2})+exp((token3))
Token has following format: {column_name}(n={day},t={table_name},s={summary_function}), where 
table_name/column_name list as following (this are the only tables/columns supported now, anything can't be matched exactly should generate a short error stating requested table/column not in database):
    - daily/marketcap: market cap (in million)
    - day/c: daily close price
    - day/h: daily high 
    - day/l: daily low 
    - day/vw: daily vwap 
    - day/qlmt: daily volume
day: day shift
    - 0 for current day;
    - positive num for history;
    - positive num start with 0 for history including today;
summary_function:
    only used when n!=0, for summarizing vector of data into a single number. 
    supported functions: mean, sd, max, min, mid, ema, mdd
---
Notes:
marketcap(t=daily)>8200: large cap
marketcap(t=daily)<8200&marketcap(t=daily)>100: mid cap
marketcap(t=daily)<100: small cap
c(t=day,n=9,s=ema): yesterday 9 day ema
c(t=day,n=09,s=ema): today 9 day ema
c(t=day,n=020,s=mdd): 20 day close price max drawdown, negative number between -1 and 0
---
Examples:
Q: stocks making 20 day new high
A: {"Date":"today", "Expr": "h(t=day,n=0)>h(t=day,n=20,s=max)"}
Q: which display unusual high volume on Apr 5, 2023?
A: {"Date":"2023-04-05", "Expr": "qlmt(t=day,n=0)>qlmt(t=day,n=20,s=mean)*10"}
Q: big cap stock making 5 day new high on 23/04/03
A: {"Date":"2023-04-03", "Expr": "marketcap(t=daily)>8200&h(t=day,n=0)>h(t=day,n=5,s=max)"}
Q: which small cap stock has 9 day sma cross above 20 day sma today?
A: {"Date":"today", "Expr": "marketcap(t=daily)<100&c(t=day,n=9,s=mean)<c(t=day,n=20,s=mean)&c(t=day,n=09,s=mean)>c(t=day,n=020,s=mean)"}
Q: only meme stocks
A: database not has data for meme stocks yet
Q: how are things going?
A: not a relevant question
"""

# testing results, may not match prompt
OOSExamples = """
Q: which large cap has high low range twice larger than 10 day average?
A: {"Date":"today", "Expr": "marketcap(t=daily)>8200&h(t=day,n=0)-l(t=day,n=0)>2*(h(t=day,n=10,s=mean)-l(t=day,n=10,s=mean))"}
Q: which mid cap stocks gain more than 5% on Apr 3, 2023?
A: {"Date":"2023-04-03", "Expr": "marketcap(t=daily)>100&marketcap(t=daily)<8200&c(t=day,n=0)/c(t=day,n=1)-1>0.05"}
Q: small cap with 5 fold increase in volume vs 20 day average
A: {"Date":"today", "Expr": "marketcap(t=daily)<100&qlmt(t=day,n=0)/qlmt(t=day,n=20)>5"}
Q: list small cap meme stocks
A: Sorry, I cannot provide an answer to that question as the database does not have data for meme stocks yet.
Q: I maintain the database and has added column idx under table meme, where 1 is for meme stocks. list small cap meme stocks
A: {"Date":"today", "Expr": "marketcap(t=daily)<100&idx(t=meme,n=0)=1"}
Q: big cap with large percent of trading from institutions
A: I'm sorry, I cannot provide an answer as the requested table/column "institutional trading" is not in the database and not supported by the translator.
Q: big cap with close price max drawdown more than 10% in last 20 days
A: {"Date":"today", "Expr": "marketcap(t=daily)>8200&c(t=day,n=020,s=mdd)<-0.1"}
Q: which larget cap stocks has low below 20 days low today?
A: {"Date":"today", "Expr": "marketcap(t=daily)>8200&l(t=day)<l(t=day,n=20,s=min)"}
Q: how are things going?
A: Sorry, that is not a relevant question. Please provide a valid query in the format specified.
"""

# testing fail
"""
Q: mid cap, 9 day ema cross below 26 day today
A: {"Date":"today", "Expr": "marketcap(t=daily)>100&marketcap(t=daily)<8200&c(t=day,n=9,s=ema)>c(t=day,n=26,s=ema)&c(t=day,n=09,s=ema)<c(t=day,n=026,s=ema)"}
N: cross side is wrong
Q: big cap with large percent of trading from institutional investors
A: {"Date":"today", "Expr": "marketcap(t=daily)>8200&qlmt(t=daily,n=0)/qlmt(t=daily,n=0,s=sum)>0.5"}
N: made up column name
"""


def NLToJson(q) -> str:
    content = f"{MsgHead}\n---\nQ:{q}\nA:\n"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": Role},
            {"role": "user", "content": content}
        ],
        temperature=0,
        max_tokens=256
    )
    logging.info(q)
    logging.info(res)
    return res["choices"][0]['message']['content']


def ConnectionCheck():
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "assistant"},
            {"role": "user", "content": "connection check. simply reply read"}
        ],
        temperature=0,
        max_tokens=4
    )
    logging.info(res)
    return res["choices"][0]['message']['content']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-Q', type=str,
                        default="big cap with vwap above 10 day average vwap and high volume today?")
    pars, _ = parser.parse_known_args()
    #
    res = NLToJson(pars.Q)
    # res = ConnectionCheck()
    print(res)
