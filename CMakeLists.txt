cmake_minimum_required(VERSION 2.8)
project (extract)

# Include CMake modules
INCLUDE(FindPkgConfig)
INCLUDE(CheckIncludeFiles)

# Set C++ flag to use functionalities of C++11
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

###################################################
#                    MODULES
###################################################
set (PO_MODULES "extract")
###################################################
#                EXTERNAL LIBRARIES
###################################################

pkg_check_modules(OPENCV REQUIRED opencv)
pkg_check_modules(ARGTABLE REQUIRED argtable2)
pkg_check_modules(TESSERACT REQUIRED tesseract)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)


if(UNIX AND NOT APPLE)
        find_path(OPENBLAS_INCLUDE_DIRS NAMES cblas.h HINTS "/usr/include" "/usr/local/include" )
        find_library(OPENBLAS_LIBRARIES NAMES openblas HINTS "/usr/lib" "/usr/local/lib" "/usr/lib/x86_64-linux-gnu")
else(UNIX AND NOT APPLE)
        find_path(OPENBLAS_INCLUDE_DIRS NAMES cblas.h HINTS "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework/Frameworks/vecLib.framework/Headers" "/usr/local/Cellar/openblas/0.2.18_2/include/")

        find_library(OPENBLAS_LIBRARIES NAMES openblas HINTS "/usr/lib" "/usr/local/lib")
        find_library(OPENBLAS_LIBRARIES vecLib)
endif(UNIX AND NOT APPLE)

###################################################
#                     HEADERS
###################################################
set(INCLUDE_DIRS "")

foreach (_moduleName ${PO_MODULES})
    list(APPEND INCLUDE_DIRS "${_moduleName}/include")	
endforeach()

include_directories(${INCLUDE_DIRS})
include_directories(${OPENCV_INCLUDE_DIRS} ${TESSERACT_INCLUDE_DIRS} ${ARGTABLE_INCLUDE_DIRS} ${GFLAGS_INCLUDE_DIRS} ${GLOG_INCLUDE_DIRS} ${PROTOBUF_INCLUDE_DIRS} ${HDF5_INCLUDE_DIRS} ${LMDB_INCLUDE_DIRS} ${LEVELDB_INCLUDE_DIRS} ${SNAPPY_INCLUDE_DIRS} ${OPENBLAS_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${CAFFE_INCLUDE_DIRS})

###################################################
#               LIBRARIES SEARCH PATH
###################################################
link_directories("/usr/local/lib" "/usr/lib" ${OPENCV_LINK_DIRECTORIES} ${TESSERACT_LINK_DIRECTORIES} ${ARGTABLE_LINK_DIRECTORIES} ${GFLAGS_LINK_DIRECTORIES} ${GLOG_LINK_DIRECTORIES} ${PROTOBUF_LINK_DIRECTORIES} ${Boost_LINK_DIRECTORIES})

###################################################
#             PROJECT EXECUTABLE OUTPUT
###################################################
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
foreach (_moduleName ${PO_MODULES})
    file(GLOB_RECURSE _module_sources "${_moduleName}/*.cpp")
    add_executable(${_moduleName} ${_module_sources})
    TARGET_LINK_LIBRARIES(${_moduleName} ${ARGTABLE_LIBRARIES} ${TESSERACT_LIBRARIES} ${OPENCV_LIBRARIES} pthread tiff)
endforeach()


