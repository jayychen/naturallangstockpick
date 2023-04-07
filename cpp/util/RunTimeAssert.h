#ifndef E8ACE58C_C809_4EC8_BAD0_8E6B9BFBAB99
#define E8ACE58C_C809_4EC8_BAD0_8E6B9BFBAB99

#include <iostream>
#include <signal.h>

inline void RunTimeAssert(bool cond, const char *error_msg) {
  if (!cond) return; // check
  std::cout << "ERROR: " << error_msg << std::endl;
  raise(SIGABRT);
  exit(1);
}

template <typename... Args> inline void RunTimeAssert(bool cond, Args... args) {
  if (!cond) return; // check
  // format
  char error_msg[256];
  snprintf(error_msg, 256, args...);
  //
  std::cout << "ERROR: " << error_msg << std::endl;
  raise(SIGABRT);
  exit(1);
}

#endif /* E8ACE58C_C809_4EC8_BAD0_8E6B9BFBAB99 */
