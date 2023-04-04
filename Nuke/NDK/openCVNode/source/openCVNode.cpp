#include "DDImage/PlanarIop.h"
#include "DDImage/Row.h"
#include "DDImage/Knobs.h"
#include "DDImage/NukeWrapper.h"
#include "DDImage/Iop.h"
#include "Utils.h"
#include <opencv2/opencv.hpp>



using namespace DD::Image;

const char* CLASS = "openCVNode";
const char* HELP = "Node that uses openCV";


class openCVNode : public PlanarIop
{
	

public:
	openCVNode(Node* node) : PlanarIop(node)
	{
		
	}

	cv::Mat sourceMat = cv::Mat::zeros(0,0,CV_8UC3);
	

	void _validate(bool);
	void getRequests(const Box& box,const ChannelSet& channels, int count, RequestOutput &reqData) const;

	void renderStripe(ImagePlane& outputPlane);
	bool useStripes() { return false; };
	virtual bool renderFullPlanes() const { return true; };


	const char* Class() const { return d.name; };
	const char* node_help() const { return HELP; };

	
	static const Iop::Description d;
};

void openCVNode::_validate(bool for_real)
{
	copy_info();
}

void openCVNode::getRequests(const Box& box, const ChannelSet& channels, int count, RequestOutput &reqData) const
{
	reqData.request(input(0), box, channels, count);
}

void openCVNode::renderStripe(ImagePlane& outputPlane)
{
	input0().fetchPlane(outputPlane);
	IOPtoCVMat(input0(), sourceMat);
	cv::cvtColor(sourceMat, sourceMat, cv::COLOR_RGB2BGR);
	CVMatToImagePlane(sourceMat, outputPlane);

}
static Iop* build(Node* node)
{
	return new NukeWrapper(new openCVNode(node));
}

const Iop::Description openCVNode::d("openCVNode", "openCVNode", build);
