#ifndef D841A048_0278_4025_B5BE_345B1EA86F5E
#define D841A048_0278_4025_B5BE_345B1EA86F5E

#include <chrono>
#include <iomanip>
#include <iostream>
#include <sstream>

std::string getCurrentDate() {
  auto now = std::chrono::system_clock::now();
  auto timePoint = std::chrono::system_clock::to_time_t(now);
  std::tm currentTime{};
  localtime_r(&timePoint, &currentTime);

  std::ostringstream oss;
  oss << std::put_time(&currentTime, "%Y-%m-%d");
  return oss.str();
}

#endif /* D841A048_0278_4025_B5BE_345B1EA86F5E */
