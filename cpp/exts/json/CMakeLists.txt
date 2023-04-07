cmake_minimum_required(VERSION 3.17.2)
project(JSON)

add_library(json INTERFACE)
target_include_directories(json INTERFACE ${EXTERNAL_LIB_DIR}/include/json/single_include/ ${CMAKE_CURRENT_SOURCE_DIR} )
target_link_libraries(json INTERFACE util)


#bin---------------------------------------------------------
if(DEFINED BUILDEXE)
	#ut_json
	add_executable(ut_json ut_json.cpp)
	target_link_libraries(ut_json PUBLIC json)	
endif()
