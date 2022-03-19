#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include "Vertex.h"
#include "edge.h"
#include "graph.h"
#include "shortestpath.h"
#include "draw.h"

using namespace std;

int main() {
    Graph g("Datasets/Routes.txt", "Datasets/Airports.txt");
    
    int src;
    cout << "Please enter a source aiport ID from 'Datasets/Airports.txt': ";
    cin >> src;
    while (g.m.find(src) == g.m.end()) {
         cout << "Please enter a valid source airport ID: ";
         cin >> src;
    }
    cout << "Source Airport: " << g.m[src].nameOfAirport << endl;
    int dest;
    cout << "Please enter a destination airport ID from 'Datasets/Airports.txt': ";
    cin >> dest;
    while (g.m.find(dest) == g.m.end() || src == dest) {
         cout << "Please enter a valid destination airport ID: ";
         cin >> dest;
    }
    cout << "Destination Airport: " << g.m[dest].nameOfAirport << endl;
    std::cout <<std::endl;
    
    ShortestPath sp(g.m[src], g.m[dest]);
    vector<Edge> pathes = sp.BFS(g);
    vector<Edge> pathes2 = sp.Dijkstra(g);
    
    std::cout << std::endl;
    
    Draw D(pathes);
    D.convert();
    D.draw("world_map.png", "first.png", true);

    Draw D2(pathes2);
    D2.convert();
    D2.draw("first.png", "output.png", false);

    std::cout << "Please check out output.png for the graphical output - green (Dijkstra), purple (BFS)" << std::endl;
    
    return 0;
};
