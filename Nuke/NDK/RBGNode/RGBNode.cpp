#include<iostream>
#include<DDImage/PlanarIop.h>
#include<DDImage/Row.h>
#include<DDImage/Knobs.h>
#include<DDImage/NukeWrapper.h>

using namespace DD::Image;

const char* CLASS = "RGBNode";
const char* HELP = " ";


class RGBNode : public PlanarIop
{
	int value[3];

public:
	RGBNode(Node* node) : PlanarIop(node)
	{
		value[0] = value[1] = value[2] = 0;
	}
	void _validate(bool);
	void _request(int x, int y, int r, int t, ChannelMask channels, int count);
	void renderStripe(ImagePlane& outputPlane);
	bool useStripes() { return true; };

	const char* Class() const { return d.name; };
	const char* node_help() const { return HELP; };

	virtual void knobs(Knob_Callback);
	static const Iop::Description d;
};

void RGBNode::_validate(bool for_real)
{
	copy_info();
}

void RGBNode::_request (int x, int y, int r, int t, ChannelMask channels, int count)
{
	input(0)->request(x, y, r, t, channels, count);
}

void RGBNode::renderStripe(ImagePlane& outputPlane)
{
	input(0)->fetchPlane(outputPlane);

	outputPlane.makeUnique();
	outputPlane.makeWritable();

	Box bounds = outputPlane.bounds();

	for (Box::iterator it = bounds.begin(); it != bounds.end(); it++)
	{
		outputPlane.writableAt(it.x, it.y, 0) = value[0];
		outputPlane.writableAt(it.x, it.y, 1) = value[1];
		outputPlane.writableAt(it.x, it.y, 2) = value[2];
	}
};

void RGBNode::knobs(Knob_Callback f)
{
	MultiInt_knob(f, value, 3, "value");
}

static Iop* build(Node* node)
{
	return new NukeWrapper(new RGBNode(node));
}

const Iop::Description RGBNode::d("RGBNode", "RGBNode", build);