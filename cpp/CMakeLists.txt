cmake_minimum_required(VERSION 3.17.2)
project(NLSP)

# libs
# set(Boost_USE_STATIC_LIBS OFF) 
# find_package(Boost 1.73.0 REQUIRED COMPONENTS iostreams)
# find_package(ZLIB)
# set(LIB_DIR xxx)

# flag
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(EXTERNAL_LIB_LIB_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../external_libs)
set(CMAKE_CXX_FLAGS "-Wall -Wfatal-errors")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g3")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# build type
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

IF(CMAKE_BUILD_TYPE MATCHES Release)
  set(BUILDEXE True)
  set(BUILDUNITTEST True)
  set(RPKGRELEASE True)
ENDIF(CMAKE_BUILD_TYPE MATCHES Release)

IF(CMAKE_BUILD_TYPE MATCHES Debug)
  set(BUILDEXE True)
  set(BUILDUNITTEST True)
  option(BUILD_SHARED_LIBS "Build using shared libraries" OFF)
ENDIF(CMAKE_BUILD_TYPE MATCHES Debug)

# base
add_subdirectory(util)
add_subdirectory(db)
# add_subdirectory(../rpkg ${CMAKE_CURRENT_BINARY_DIR}/rpkg)

# graphviz
# add_custom_target(graphviz ALL
# COMMAND "${CMAKE_COMMAND}" "--graphviz=graph/graph.dot" .
# COMMAND dot graph/graph.dot -Tsvg -o graph.svg
# WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")