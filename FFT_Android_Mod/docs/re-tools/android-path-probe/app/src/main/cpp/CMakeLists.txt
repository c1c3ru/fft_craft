cmake_minimum_required(VERSION 3.18.1)
project(a04_android_path_probe C)

# The only builder linked here is the bounded independent reconstruction;
# the original game ELF and its unsafe strcpy are never linked or executed.
add_library(a04_android_path_probe SHARED
    a04_android_path_probe.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../../../../c-models/a04_rootpath_safe.c
)
set_property(TARGET a04_android_path_probe PROPERTY C_STANDARD 11)
