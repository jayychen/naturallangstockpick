#ifndef DE3AF9D4_DE16_4EC2_9D1B_D4D9018AC5B6
#define DE3AF9D4_DE16_4EC2_9D1B_D4D9018AC5B6

#include <string>
#include <vector>

/**
 * @brief For query stock data from database
 *        Data is read from database on-demand, and cached in memory
 *
 */
class StockDB {
public:
  /**
   * @brief For expression calculation
   * @param expr expression is composed of token in following format:
   *             {column_name}(n={day},t={table_name},s={summary_function})
   *        where
   *            table_name, column_name:
   *                position in the database
   *            n: (optional, default 0)
   *                0 for current day;
   *                positive num for history;
   *                positive num start with 0 for history including today;
   *                negative num for future;
   *                negative num start with 0 for future including today;
   *            summary_function: (optional, default mean)
   *                only used when n!=0, for summarizing vector of data into a single number
   *        and common operators of tokens are supported.
   *        example:
   *            marketcap(t=daily,n=3,s=max)
   *                returns max of market cap of last 3 days
   *            log10(marketcap(t=daily,n=3,s=max))>2
   *                returns 0.0 or 1.0, indicating whether max market cap of last 3 days larger than
   *                10 million
   *            c(t=day)>c(t=day,n=20,s=high)
   *                returns 0.0 or 1.0, indicating whether today's close is highest price of last 20
   *                days
   *            todo add more examples
   *
   * @param dat date, in format of YYYY-MM-DD
   * @param sym symbol, eg. AAPL
   * @return double
   */
  double ExprCalc(std::string expr, std::string dat, std::string sym) const;

  /**
   * @brief For filtering symbols where expr is not zero
   *
   * @param expr
   * @param dat
   * @return all eligible symbols
   * @example
   *     SymbolFilter("log10(marketcap(t=daily,n=3,s=max))>2", "2023-04-01")
   *         returns all symbols whose max market cap of last 3 days larger than 10 million
   */
  std::vector<std::string> SymbolFilter(std::string expr, std::string dat) const;

  /**
   * @brief For retrieving vector of float
   *
   * @param expr in format of {column_name}(t={table_name})
   * @param dat date, in format of YYYY-MM-DD
   * @param sym symbol, eg. AAPL
   * @example
   *     GetFltVec("sym(t=cor)", "2023-04-01", "AAPL")
   *         returns vector of correlation of AAPL with best correlated symbols
   */
  const std::vector<float> &GetFltVec(std::string expr, std::string dat, std::string sym) const;

  /**
   * @brief Same as GetFltVec, but for string vector
   * @example
   *    GetStrVec("sym(t=cor)", "2023-04-01", "AAPL")
   *        returns vector of symbols that are best correlated with AAPL
   */
  const std::vector<std::string> &GetStrVec(std::string expr, std::string dat,
                                            std::string sym) const;

public:
  StockDB() = default; // do nothing
  ~StockDB();          // delete impl_
private:
  void *impl_{nullptr}; // for implentation
};

#endif /* DE3AF9D4_DE16_4EC2_9D1B_D4D9018AC5B6 */
