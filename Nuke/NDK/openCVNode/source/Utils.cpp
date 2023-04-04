#include "DDImage/PlanarIop.h"
#include <opencv2/opencv.hpp>
#include "Utils.h"


using namespace DD::Image;


void CVMatToImagePlane(cv::Mat& inputMat, ImagePlane& outputPlane)
{
	outputPlane.makeUnique();
	outputPlane.makeWritable();

	Box box = outputPlane.bounds();
	cv::Vec3b pixel_color;

	if (!inputMat.empty())
	{
		ChannelMask channels = outputPlane.channels();

		Channel r_ch = channels.first();
		Channel g_ch = channels.next(r_ch);
		Channel b_ch = channels.next(g_ch);


		for (Box::iterator it = box.begin(); it != box.end(); it++)
		{
			pixel_color = inputMat.at<cv::Vec3b>(cv::Point(it.x, it.y));
			outputPlane.writableAt(it.x, it.y, outputPlane.chanNo(r_ch)) = pixel_color[2] / 255.0;
			outputPlane.writableAt(it.x, it.y, outputPlane.chanNo(g_ch)) = pixel_color[1] / 255.0;
			outputPlane.writableAt(it.x, it.y, outputPlane.chanNo(b_ch)) = pixel_color[0] / 255.0;

		}
	}
}

void IOPtoCVMat(Iop& inputIOP, cv::Mat& outputMat)
{
	ChannelMask channels = inputIOP.channels();
	
	Channel r_ch = channels.first();
	Channel g_ch = channels.next(r_ch);
	Channel b_ch = channels.next(g_ch);

	outputMat = cv::Mat::zeros(inputIOP.h(), inputIOP.w(), CV_8UC3);

	for (int i = 0; i < outputMat.rows; i++)
	{
		for (int j = 0; j < outputMat.cols; j++)
		{
			(outputMat.at<cv::Vec3b>(i, j).val[0] = inputIOP.at(j, i, b_ch)) * 255;
			(outputMat.at<cv::Vec3b>(i, j).val[0] = inputIOP.at(j, i, g_ch)) * 255;
			(outputMat.at<cv::Vec3b>(i, j).val[0] = inputIOP.at(j, i, r_ch)) * 255;
		}
	}
}