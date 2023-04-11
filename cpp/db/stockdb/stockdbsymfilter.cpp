// util
#include "system/ArgParse.h"
//
#include "StockDB.h"

int main(int argc, char *argv[]) {
  auto pars =
      ArgParse(argc, argv,
               {{"Date", "today"},
                {"Expr", R"(qlmt(t=day)/qlmt(t=day,n=5,s=mean)>5&marketcap(t=daily)>20000"})"}});
  if (pars.empty()) return 1;
  std::string dat = pars.at("Date");
  auto expr = pars.at("Expr");
  // filter
  StockDB sdb;
  if (dat == "today") dat = sdb.LastDate();
  auto symbols = sdb.SymbolFilter(expr, dat);
  for (const auto &sym : symbols) printf("%s\n", sym.c_str());
}