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
You are a natural language to json translator
"""

MsgHead = """
Return json in following format: {"Date":"xxx", "Expr": "xxx"}
Date is either in YYYY-MM-DD format, or today.
Expr is an expression composed of tokens and common mathmatical operations of tokens are supported. eg. log10({token1}/{token2})+exp((token3))
Token has following format: {column_name}(n={day},t={table_name},s={summary_function}), where 
table_name, column_name: position in the database
  eg. daily, marketcap: market cap (in million)
  eg. day, c: daily close price
  eg. day, h: daily high 
  eg. day, l: daily low 
  eg. day, vw: daily vwap 
  eg. day, qlmt: daily volume
day: day shift (optional, default 0)
    0 for current day;
    positive num for history;
    positive num start with 0 for history including today;
    negative num for future;
    negative num start with 0 for future including today;
summary_function: (optional, default mean)
    only used when n!=0, for summarizing vector of data into a single number. 
---
Examples:
Q: which stocks closed above 20 days high on Apr 6, 2023?
A: {"Date":"2023-04-06", "Expr": "c(t=day,n=0)>h(t=day,n=20,s=max)"}
Q: which stocks has market cap above 1 trillion on 2023-01-02?
A: {"Date":"2023-01-02", "Expr": "marketcap(t=daily)>1e6"}
Q: which larget cap stocks has low below 20 days low today?
A: {"Date":"today", "Expr": "marketcap(t=daily)>8200&l(t=day)<l(t=day,n=20,s=min)"}
Q: small market cap stocks that close above 5 day mean today?
A: {"Date":"today", "Expr": "marketcap(t=daily)<8200&marketcap(t=daily)>100&c(t=day)>c(t=day,n=5,s=mean)"}
Q: micro market cap stocks that have unusual high volume on 23/02/01?
A: {"Date":"2023-02-01", "Expr": "marketcap(t=daily)<100&qlmt(t=day)>qlmt(t=day,n=5,s=max)*2"}
"""


def NLToJson(q):
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
