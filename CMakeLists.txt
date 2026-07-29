cmake_minimum_required(VERSION 3.16)
project(Chess_Engine CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake_modules)

# SDL2 and SDL2_image come from the MSYS2 UCRT64 packages:
#   pacman -S mingw-w64-ucrt-x86_64-SDL2 mingw-w64-ucrt-x86_64-SDL2_image
# cmake_modules/FindSDL2.cmake is kept for a hand-downloaded SDL2 instead, but
# it has no companion module for SDL2_image, which the piece PNGs need.
find_package(PkgConfig REQUIRED)
pkg_check_modules(SDL2 REQUIRED sdl2)
pkg_check_modules(SDL2_IMAGE REQUIRED SDL2_image)

add_executable(Chess_Engine
    ChessMain.cpp
    ChessEngine.cpp
)

target_include_directories(Chess_Engine PRIVATE
    ${SDL2_INCLUDE_DIRS}
    ${SDL2_IMAGE_INCLUDE_DIRS}
)

# Deliberately using *_INCLUDE_DIRS / *_LIBRARIES rather than the full pkg-config
# flag sets: SDL2's pkg-config file adds -Dmain=SDL_main and -mwindows, which
# would rename main() and strip the console the move list is printed to.
target_link_directories(Chess_Engine PRIVATE
    ${SDL2_LIBRARY_DIRS}
    ${SDL2_IMAGE_LIBRARY_DIRS}
)

target_link_libraries(Chess_Engine PRIVATE
    ${SDL2_IMAGE_LIBRARIES}
    ${SDL2_LIBRARIES}
)

target_compile_options(Chess_Engine PRIVATE -Wall -Wextra)

add_custom_command(TARGET Chess_Engine POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_CURRENT_SOURCE_DIR}/images
        $<TARGET_FILE_DIR:Chess_Engine>/images
    COMMENT "Copying piece images next to the executable"
)
