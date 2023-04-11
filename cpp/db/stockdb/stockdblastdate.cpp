#include <iostream>
//
#include "StockDB.h"

int main(int argc, char *argv[]) {
  StockDB sdb;
  std::cout << sdb.LastDate() << std::endl;
}