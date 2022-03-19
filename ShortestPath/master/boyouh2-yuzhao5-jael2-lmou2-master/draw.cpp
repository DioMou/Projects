#include "draw.h"
#include <stdio.h>
#include <math.h>


Draw::Draw(std::vector<Edge> edges) {
    edges_ = edges;
}

float Draw::slope(coor a, coor b) {
    return (b.second - a.second) / (b.first - a.first);
}

float Draw::intercept(coor point, float slope) {
    if (isnan(slope)) {
        // vertical line
        return point.first;
    }

    return point.second - slope * point.first;
}

void Draw::draw(std::string inputFile, std::string outputFile, bool ifBFS) {
    PNG wMap;
    wMap.readFromFile(inputFile);
    double hue = (ifBFS) ? 315 : 95;
    
    for (size_t i = 0; i < coors.size()-1; i++) {
        coor A = coors[i][0];
        coor B = coors[i+1][0];
        // select the pixel point with shorter distance to draw
        if (coors[i + 1].size() > 1) {
            if (abs(A.first - coors[i+1][0].first) > abs(A.first - coors[i+1][1].first)) {
                B = coors[i + 1][1];
                // to make sure the coor A in next iteration correct
                coors[i + 1][0] = coors[i + 1][1];
            }
        }
        

        if (A.first != B.first && A.second != B.second) {

            float m = slope(A, B);
            float b = intercept(A, m);

            // Draws line between points A and B
            // TODO: line is too small, make it larger
            for (float x = min(A.first, B.first); x <= max(A.first, B.first); x++) {
                int y = int(m * x + b);
                int preY=int(m * (x-1) + b);
                if (y-preY >=1 || y-preY <=-1) {x=x+6;}
                if (x < (int)wMap.width() && y < (int)wMap.height() ) {
                    HSLAPixel &pixel = wMap.getPixel(x, y);
                    for(int i = x-1; i < x+2; i++){
                        for(int j = y-1; j < y+2; j++){
                            if (i < (int)wMap.width() && j < (int) wMap.height()) {
                                HSLAPixel &pixelAll=wMap.getPixel(i,j);
                                pixelAll.h = hue; pixelAll.s = 1;pixelAll.l = 0.5;pixelAll.a = 1;
                            }
                        }
                    }
                }
            }
        }
    }
    wMap.writeToFile(outputFile);
}

void Draw::convert() {
    
    for (Edge e : edges_) {
        vector<coor> temp;

        // in the eastern semisphere
        if (e.source.longitude >= 0) {
            coor c = convert(e.source.latitude, e.source.longitude);
            temp.push_back(c);
        } else {
            // in the western semisphere
            coor c1 = convert(e.source.latitude, e.source.longitude);
            coor c2 = {c1.first  + sphereWidth, c1.second};
            temp.push_back(c1);
            temp.push_back(c2);
        }

        coors.push_back(temp);
        temp.clear();

        // in the eastern semisphere
        if (e.destination.longitude >= 0) {
            coor c = convert(e.destination.latitude, e.destination.longitude);
            temp.push_back(c);
        } else {
            // in the western semisphere
            coor c1 = convert(e.destination.latitude, e.destination.longitude);
            coor c2 = {c1.first + sphereWidth, c1.second};
            temp.push_back(c1);
            temp.push_back(c2);
        }

        coors.push_back(temp);
    }
    
}

coor Draw::convert(long double latitude, long double longitude) {
    float x = ((longitude + 180) * sphereWidth) / 360;
    float y = ((90 - latitude) * mapHeight) / 180;
    return {x, y};
}
