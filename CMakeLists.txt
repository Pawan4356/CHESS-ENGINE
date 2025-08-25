cmake_minimum_required(VERSION 4.0)
project(Chess_Engine CXX)

set(CMAKE_C_STANDARD 17)
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake_modules)
set(SDL2_PATH "C:/Users/HP/Downloads/SDL2-devel-2.0.5-mingw/SDL2-2.0.5/x86_64-w64-mingw32")
find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIR})

add_executable(Chess_Engine ChessMain.cpp)

target_link_libraries(${PROJECT_NAME} ${SDL2_LIBRARY})