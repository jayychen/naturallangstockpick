# Query to JSON converter
This Module converts natural language into JSON format string, which can be used for sql query.

### Model Test
Q: big cap with vwap above 10 day average vwap and high volume today?

A:
- text-ada-001 \
  {"Date":"today", "expr": "vwap(t=daily)>100&l(t=day)<l(t=day,n=20,s=min)"}
- text-babbage-001 \
  {"Date":"2023-02-01", "expr": "vwap(t=day)>10&qlmt(t=day)>qlmt(t=day,n=10,s=max)"}
- text-curie-001 \
  {"Date":"today", "expr": "marketcap(t=daily)>20000&vwap(t=day)>10"}
- gpt-3.5-turbo \
  {"Date":"today", "expr": "marketcap(t=daily)>8200&vw(t=day)>vw(t=day,n=10,s=mean)&qlmt(t=day)>qlmt(t=day,n=5,s=max)"}

### Test results with gpt-3.5-turbo
- volume increse 5 folds today \
  I'm sorry, but your request is incomplete. Please provide more information or a specific question for me to translate into the JSON format.
- volume increse 5 folds today vs previous 5 days \
  {"Date":"today", "expr": "qlmt(t=day)/qlmt(t=day,n=5,s=mean)>5"}
- volume increse 5 folds today vs previous 5 days and market cap > 20000 \
  {"Date":"today", "expr": "qlmt(t=day)/qlmt(t=day,n=5,s=mean)>5&marketcap(t=daily)>20000"}

### Notes
- each call cost ~0.13 cents; 100 calls daily -> $3.9 monthly
- future: fine tune model