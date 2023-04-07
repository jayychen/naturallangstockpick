cmake_minimum_required(VERSION 3.17.2)
project(StockDB)

#external 
add_library(stockdblib SHARED IMPORTED)
set_target_properties(stockdblib PROPERTIES
    IMPORTED_LOCATION ${EXTERNAL_LIB_DIR}/lib/libstockdb.so
)

# interface for database query
add_library(stockdb INTERFACE)
target_link_libraries(stockdb INTERFACE stockdblib util)
target_include_directories(stockdb INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})

# bin---------------------------------------------------------
if(DEFINED BUILDEXE)
  # stockdbsymfilter
  add_executable(stockdbsymfilter stockdbsymfilter.cpp)
  target_link_libraries(stockdbsymfilter stockdb json)
endif()

if(DEFINED BUILDUNITTEST)
  # ut_stockdb
  add_executable(ut_stockdb ut_stockdb.cpp)
  target_link_libraries(ut_stockdb stockdb)
endif()