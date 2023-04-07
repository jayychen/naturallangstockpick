cmake_minimum_required(VERSION 3.17.2)
project(Utility)

add_library(util Init.cpp)
target_include_directories(util PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
