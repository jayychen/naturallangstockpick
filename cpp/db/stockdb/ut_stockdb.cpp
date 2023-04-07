#include <functional>
using namespace std::placeholders;
// util
#include "system/ArgParse.h"
//
#include "StockDB.h"

int main(int argc, char *argv[]) {
  auto pars = ArgParse(argc, argv, {{"Date", "2023-04-06"}});
  if (pars.empty()) return 1;
  auto dat = pars.at("Date");
  //
  StockDB sdb;
  // filter
  auto symbols = sdb.SymbolFilter("log10(marketcap(t=daily,n=3,s=max))>6", dat);
  printf("Filtered trillion dollar symbols using log10(marketcap(t=daily,n=3,s=max))>6:\n");
  for (const auto &sym : symbols) printf("%s\n", sym.c_str());
  // cor
  auto symvec = sdb.GetStrVec("sym(t=cor)", dat, "GME");
  auto corvec = sdb.GetFltVec("cor(t=cor)", dat, "GME");
  printf("Correlated symbol of GME:\n");
  int i = 0;
  for (const auto &sym : symvec) printf("%s: %g\n", sym.c_str(), corvec.at(i++));
}