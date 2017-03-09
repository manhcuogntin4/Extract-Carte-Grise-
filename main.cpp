#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <sstream>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <dirent.h> // for linux systems
#include <sys/stat.h> // for linux systems
using namespace cv; 
using namespace std;

/* Returns a list of files in a directory (except the ones that begin with a dot) */

void readFilenames(std::vector<string> &filenames, const string &directory)
{
#ifdef WINDOWS
    HANDLE dir;
    WIN32_FIND_DATA file_data;

    if ((dir = FindFirstFile((directory + "/*").c_str(), &file_data)) == INVALID_HANDLE_VALUE)
        return; /* No files found */

    do {
        const string file_name = file_data.cFileName;
        const string full_file_name = directory + "/" + file_name;
        const bool is_directory = (file_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0;

        if (file_name[0] == '.')
            continue;

        if (is_directory)
            continue;

        filenames.push_back(full_file_name);
    } while (FindNextFile(dir, &file_data));

    FindClose(dir);
#else
    DIR *dir;
    class dirent *ent;
    class stat st;

    dir = opendir(directory.c_str());
    while ((ent = readdir(dir)) != NULL) {
        const string file_name = ent->d_name;
        const string full_file_name = directory + "/" + file_name;

        if (file_name[0] == '.')
            continue;

        if (stat(full_file_name.c_str(), &st) == -1)
            continue;

        const bool is_directory = (st.st_mode & S_IFDIR) != 0;

        if (is_directory)
            continue;

//        filenames.push_back(full_file_name); // returns full path
        filenames.push_back(file_name); // returns just filename
    }
    closedir(dir);
#endif
} // GetFilesInDirectory

std::vector<cv::Rect> detectLetters(cv::Mat img)
{
    std::vector<cv::Rect> boundRect;
    cv::Mat img_gray, img_sobel, img_threshold, element;
    if(img.channels()>=3){
    cvtColor(img, img_gray, CV_BGR2GRAY);
    }
    else 
    img_gray=img;
    //cvtColor(img, img_gray, CV_BGR2GRAY);
    cv::Sobel(img_gray, img_sobel, CV_8U, 1, 0, 3, 1, 0, cv::BORDER_DEFAULT);
    cv::threshold(img_sobel, img_threshold, 0, 255, CV_THRESH_OTSU+CV_THRESH_BINARY);
    element = getStructuringElement(cv::MORPH_RECT, cv::Size(17, 3) );
    cv::morphologyEx(img_threshold, img_threshold, CV_MOP_CLOSE, element); //Does the trick
    std::vector< std::vector< cv::Point> > contours;
    cv::findContours(img_threshold, contours, 0, 1); 
    std::vector<std::vector<cv::Point> > contours_poly( contours.size() );
    for( int i = 0; i < contours.size(); i++ )
        if (contours[i].size()>100)
        { 
            cv::approxPolyDP( cv::Mat(contours[i]), contours_poly[i], 3, true );
            cv::Rect appRect( boundingRect( cv::Mat(contours_poly[i]) ));
            if (appRect.width>appRect.height) 
                boundRect.push_back(appRect);
        }
    return boundRect;
}
int main(int argc, char* argv[])
{
//Begin version Binary
   char *outText;

    //tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    //if (api->Init(NULL, "fra")) {
     //   fprintf(stderr, "Could not initialize tesseract.\n");
     //   exit(1);
    //}

    // Open input image with leptonica library
    //Pix *image = pixRead(argv[1]);
    std::string input_path = argv[1];
	string folder = input_path;
    vector<string> filenames;
    cout<<"File size "<< filenames.size()<<endl;
    readFilenames(filenames, folder);
     for(size_t i = 0; i < filenames.size(); ++i)
    {

    cv::Mat im = cv::imread(folder+filenames[i], 0);
    if(im.channels()>=3){
    cvtColor(im, im, CV_BGR2GRAY);
    }
   //imshow("Gray", im);

   //imwrite("out-gray"+input_path, im);
   //cv::waitKey(0);  
   Size size(im.cols*4, im.rows*4);
  int height=60;
 //int widthMax=300;
 size.height=height;
 size.width=(int)(height*im.cols/im.rows);
  cv::resize(im, im, size);       
Mat bw;
threshold(im, bw, 0, 255, CV_THRESH_BINARY | CV_THRESH_OTSU);
//cout<<"Step 1"<<endl;
//imshow("Test", bw);
//std::string outfile="out"+filenames[i];
std::string outfile=filenames[i];
imwrite(folder+outfile, bw );

//End-of-version-binary-resize




/*Begin version color resize
   char *outText;

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    if (api->Init(NULL, "fra")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    // Open input image with leptonica library
    //Pix *image = pixRead(argv[1]);
    std::string input_path = argv[1];
	string folder = input_path;
    vector<string> filenames;

    readFilenames(filenames, folder);
     for(size_t i = 0; i < filenames.size(); ++i)
    {

    cv::Mat im = cv::imread(folder+filenames[i], 0);
      
   Size size(im.cols*4, im.rows*4);
  int height=100;
 int widthMax=300;
 size.height=height;
 size.width=(int)(height*im.cols/im.rows);
  cv::resize(im, im, size);       
//cout<<"Step 1"<<endl;
//imshow("Test", bw);
std::string outfile="out"+filenames[i];
		imwrite(folder+outfile, im );
*/
//End-of-version-binary-resize




//imwrite("out-binary"+input_path, bw);
//cv::waitKey(0);
// take the distance transform
}
cout<<"Finish"<<endl;
    return 0;
}


