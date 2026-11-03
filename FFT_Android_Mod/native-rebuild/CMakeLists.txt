cmake_minimum_required(VERSION 3.18)
project(fftcraft_native_stage LANGUAGES C CXX)

# An independent reconstruction STAGING target, not a replacement libgl2jni.so.
# Never link a shipped game ELF or publish it as a reconstructed Android engine.
include(CTest)
add_library(fftcraft_stage_models STATIC
  ../docs/re-tools/c-models/b01_named_cpp_methods.cpp
  ../docs/re-tools/c-models/t14_boot_framemove.c
  ../docs/re-tools/c-models/t19_evt_flag_high_low.c
  ../docs/re-tools/c-models/t19_evt_flagset.c
  ../docs/re-tools/c-models/t22_ios_resumegetdata.c
)
target_compile_features(fftcraft_stage_models PUBLIC c_std_11 cxx_std_17)
set_target_properties(fftcraft_stage_models PROPERTIES
  C_STANDARD 11 C_STANDARD_REQUIRED YES
  CXX_STANDARD 17 CXX_STANDARD_REQUIRED YES
  POSITION_INDEPENDENT_CODE YES
)
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(fftcraft_stage_models PRIVATE -Wall -Wextra -Werror -Wpedantic)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(fftcraft_stage_models PRIVATE $<$<COMPILE_LANGUAGE:CXX>:-Wall;-Wextra;-Werror;-Wpedantic>)
endif()

if(BUILD_TESTING AND NOT CMAKE_CROSSCOMPILING)
  add_executable(fftcraft_stage_smoke tests/stage_smoke.cpp)
  target_link_libraries(fftcraft_stage_smoke PRIVATE fftcraft_stage_models)
  target_compile_features(fftcraft_stage_smoke PRIVATE cxx_std_17)
  add_test(NAME fftcraft_stage_cpp_contract_smoke COMMAND fftcraft_stage_smoke)
endif()
