cmake_minimum_required(VERSION 3.18.1)
project(a04_android_path_probe C)
add_library(a04_android_path_probe SHARED a04_android_path_probe.c)
set_property(TARGET a04_android_path_probe PROPERTY C_STANDARD 11)
