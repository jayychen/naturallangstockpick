#ifndef D392B8CA_FAA7_4B29_8CC7_7D42DA49CB6D
#define D392B8CA_FAA7_4B29_8CC7_7D42DA49CB6D

//util
#include "string/Init.h"
#include "RunTimeAssert.h"

using Par = std::vector<std::pair<std::string, std::string>>;

/* check if return empty
 * can handle named variable in format --par=val, notice named variable should positioned later than
 all positional variable
 * eg.
        auto pars=ArgParse(argc, argv, {{"csv_fname", "AAPL.csv"}, {"db_fname", "AAPL.db"},
 {"table_name", "daily"}}, {{"date_key", "Date"}}); if (pars.empty()) return 1;
 */
inline StringMap ArgParse(int argc, char *argv[], const Par &pars, const Par &pars_opt = {},
                          const StringVec &notes = {}) {
  int n_par_min = pars.size();
  int n_par = pars.size() + pars_opt.size();
  if (argc < n_par_min + 1 || argc > n_par + 1 || (argc == 2 && strcmp(argv[1], "help") == 0)) {
    // notes
    printf("Brief: \n");
    for (const auto &note : notes) printf("\t%s\n", note.c_str());
    // args
    printf("Arguments: \n");
    int i = 1;
    for (const auto &item : pars) printf("\t%d. %s\n", i++, item.first.c_str());
    for (const auto &item : pars_opt)
      printf("\t%d. %s (opt. %s)\n", i++, item.first.c_str(), item.second.c_str());
    // Examples
    printf("Examples: \n");
    printf("\t%s", argv[0]);
    for (const auto &item : pars) printf(" %s", item.second.c_str());
    printf("\n");
    if (!pars_opt.empty()) { // with optional param
      printf("\t%s", argv[0]);
      for (const auto &item : pars) printf(" %s", item.second.c_str());
      for (const auto &item : pars_opt) printf(" %s", item.second.c_str());
      printf("\n");
    }
    printf("\n");
    // return
    return StringMap();
  } else {
    StringMap res;
    int idx = 1;
    auto is_positional = [&]() { return (idx < argc && strncmp(argv[idx], "--", 2) != 0); };
    auto is_named = [&]() { return (idx < argc && strncmp(argv[idx], "--", 2) == 0); };
    // handle positional
    for (const auto &item : pars)
      res.emplace(item.first, is_positional() ? (argv[idx++]) : item.second);
    for (const auto &item : pars_opt)
      res.emplace(item.first, is_positional() ? (argv[idx++]) : item.second);
    // handle named
    while (is_named()) {
      std::string named = argv[idx] + 2;
      auto svec = split(named, '=');
      RunTimeAssert(svec.size() != 2, "wrong format for named variable, %s", argv[idx]);
      res[svec[0]] = svec[1]; // over-write
      idx++;
    }
    return res;
  }
}

#endif /* D392B8CA_FAA7_4B29_8CC7_7D42DA49CB6D */
