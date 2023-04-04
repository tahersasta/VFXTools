#include "DDImage/PlanarIop.h"
#include <opencv2/opencv.hpp>

using namespace DD::Image;

void IOPtoCVMat(Iop& inputIOP, cv::Mat& ouputMat);
void CVMatToImagePlane(cv::Mat& inputMat, ImagePlane& outputPlane);


