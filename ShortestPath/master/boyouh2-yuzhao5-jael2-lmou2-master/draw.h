#pragma once
#include "Vertex.h"
#include "edge.h"
#include "cs225/PNG.h"
#include "cs225/HSLAPixel.h"
#include <vector>

using cs225::HSLAPixel;
using cs225::PNG;

// declare the coordinate of pixels to  be a pair of unsigned int
typedef pair<float, float> coor;

class Draw {
public:
    Draw(vector<Edge> edges);
    float slope(coor a, coor b);
    float intercept(coor point, float slope);
    void draw(std::string inputFile, std::string outputFile, bool ifBFS);

    // convert the data iedges to pixel positions in coors
    void convert();

    // helper function used to convert latitude and longitude to pixel coordinate (x, y) on the world map
    coor convert(long double latitude, long double longitude);

    // used to store coordinates in the shortest path in order
    // if there are two coordinates in the inner vector,
    // then it means you need to choose one pixel from the two pixels in different positions for the same airport
    vector<vector<coor>> coors;

private:
    vector<Edge> edges_;
    // int mapWidth = 3071;
    int mapHeight = 1025;
    int sphereWidth = 2048;
};


