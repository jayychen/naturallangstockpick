# Natural Language Stock Picker

Disclaimer: This is just a fun project to learn about the stock market and natural language processing. Do not rely on this for any financial decisions.

## Introduction
Sometimes it is not easy to find tickers that meet specific criteria. For example, one might want to find all small-cap stocks that have an unusually high trading volume today and a maximum drawdown of the close price of less than 10% in the last 20 days. This project aims to make this process easier by providing a natural language interface, allowing users to get the list of tickers by simply asking the question. Check out this [website](https://stockchatai.com) and keep clicking on the "Explore" button to see some examples.

## QExpr: An Intermediary Language
QExpr is an intermediary language between natural language and SQL queries. It is composed of tokens and common math operations of tokens are supported. eg.
$$
log10({token1}/{token2})+exp(token3) 
$$
Each token has the following format:
<p align="center">
{column_name}(n={day},t={table_name},s={summary_function})
</p>
, where

- table_name/column_name: refer to the position in database.
- day: a date shifter. When set to a positive number, a vector of data from the past n days will be retrieved from the database and passed to the summary function.
- summary_function: a function that converts a vector of data to a single value.

For example, 
<p align="center">
c(n=20,t=day,s=mean)
</p>
represents the average closing price of the last 20 days.

The equvilent QExpr for:
<blockquote>
small cap stocks that are having unusual high trading volume today and having maximum drawdown of close price less than 10% in the last 20 days
</blockquote> 
would be:
<p align="center">
marketcap(t=daily)<100&<br>
qlmt(t=day,n=0)>qlmt(t=day,n=20,s=mean)*10&<br>
c(t=day,n=20,s=mdd)<-0.1
</p>
where the first line selects stocks with a market cap larger than 100 million, the second line selects stocks with a trading volume larger than 10 times the average trading volume in the last 20 days, and the third line selects stocks with a maximum drawdown of the close price less than 10% in the last 20 days.

## QExpr to Ticker List
Each token is mapped to specific items in the database, and a function that converts them into a single number. For each filtering calculation, all relevant items are first retrieved from the database. Then, for each ticker, all tokens are calculated, and the result is a common mathematical expression, which can then be evaluated to a boolean. Finally, all tickers that pass the filtering will be returned.

## Natural language translation to QExpr
OpenAI models are used to translate natural language to QExpr. Each question is preceded by translation instructions and examples. A fine-tuned model may perform better in terms of accuracy or cost, but it is not implemented yet.

### Model selection
Each model was asked the following question:
<blockquote>
big cap with vwap above 10 day average vwap and high volume today?
</blockquote> 
and answers were:

- text-ada-001 \
  {"Date":"today", "Expr": "vwap(t=daily)>100&l(t=day)<l(t=day,n=20,s=min)"}
- text-babbage-001 \
  {"Date":"2023-02-01", "Expr": "vwap(t=day)>10&qlmt(t=day)>qlmt(t=day,n=10,s=max)"}
- text-curie-001 \
  {"Date":"today", "Expr": "marketcap(t=daily)>20000&vwap(t=day)>10"}
- gpt-3.5-turbo \
  {"Date":"today", "Expr": "marketcap(t=daily)>8200&vw(t=day)>vw(t=day,n=10,s=mean)&qlmt(t=day)>qlmt(t=day,n=5,s=max)"}

The results show that all previous models failed the translation task, while gpt-3.5-turbo is able to translate the question to a valid QExpr.

### Cost
Each question requires roughly 800 OpenAI tokens and costs around 0.16 cents, based on $0.002 per 1K tokens.

