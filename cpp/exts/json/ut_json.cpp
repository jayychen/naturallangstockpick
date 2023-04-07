#include <functional>
using namespace std::placeholders;
// util
#include "system/ArgParse.h"
//
#include <nlohmann/json.hpp>
using json = nlohmann::json;

int main(int argc, char *argv[]) {
  auto pars = ArgParse(
      argc, argv, {},
      {{"js",
        R"({"Date":"today", "Expr": "qlmt(t=day)/qlmt(t=day,n=5,s=mean)>5&marketcap(t=daily)>20000"})"}});
  if (pars.empty()) return 1;
  auto js = pars.at("js");
  auto jsp = json::parse(js);
  printf("Date: %s\n", jsp["Date"].get<std::string>().c_str());
  printf("Expr: %s\n", jsp["Expr"].get<std::string>().c_str());
}