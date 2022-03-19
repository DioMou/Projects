#pragma once
#include "Vertex.h"
#include "graph.h"
#include "edge.h"
#include <iostream>
#include <queue>
#include <map>
#include <tuple>

class ShortestPath {
    public:
        // user defined constructor
        ShortestPath(Vertex _source, Vertex _destination);

        // Dijkstra's algorithm implementation
        std::vector<Edge> Dijkstra(Graph G);

        // BFS implementation
        std::vector<Edge> BFS(Graph G);

        // return the shortest distance from source airport to destination airport
        long double getShortestDistance();

    private:
        // the shortest distance from source to destination
        long double shortestDistance;

        // source and destination Vertexs
        Vertex source;
        Vertex destination;
        map<int, tuple<long double, Vertex, bool>> mm;
};

// the class used to set up the min heap or priority queue in Dijkstra's algorithm
class TypeComparator {
    public:
        bool operator() (const pair<int, long double>& V1, pair<int, long double>& V2) {
            return V1.second > V2.second;
        }
};