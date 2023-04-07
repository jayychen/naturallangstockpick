#ifndef EADC6BBA_0DBF_4A38_9FFE_371054C9673F
#define EADC6BBA_0DBF_4A38_9FFE_371054C9673F

#include <cmath> //NAN
#include <set>
#include <sstream>
//
#include "Base.h"

inline StringVec split(const std::string &s, char delim) {
  StringVec ret;
  std::stringstream ss(s);
  std::string item;
  while (std::getline(ss, item, delim)) ret.push_back(item);
  return ret;
}

#endif /* EADC6BBA_0DBF_4A38_9FFE_371054C9673F */
