/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   outil.h
 * Author: cuong_nguyen
 *
 * Created on October 18, 2016, 3:56 PM
 */
#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <sstream>
#include <tesseract/baseapi.h>
using namespace cv;
#ifndef OUTIL_H
#define OUTIL_H

class outil {
public:
    outil();
    outil(const outil& orig);
    virtual ~outil();
    char* getTextFromRectangle(tesseract::TessBaseAPI *api, Rect r, cv::Mat src_img);
private:
    

};

#endif /* OUTIL_H */

