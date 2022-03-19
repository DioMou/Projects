#include "graph.h"
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <string>
#include <algorithm>
#include <stdio.h>
#include <math.h>
using namespace std;

Graph::Graph(const string& routes, const string& airports)
{
    string a = file_to_string(airports);
    string r = file_to_string(routes);
    vector<vector<string>> rawA;
    vector<vector<string>> rawR;

    vector<string> result = doSegment(a);
    for (size_t i = 0; i < result.size(); i++) {
        rawA.push_back(toVector(result[i]));
    }

    vector<string> result2 = doSegment(r);
    for (size_t i = 0; i < result2.size(); i++) {
        rawR.push_back(toVector(result2[i]));
    }
    // -----------------------------------------------------
    
    for (size_t i = 0; i < rawA.size(); i++)
    {
        Vertex insert;
        stringstream airportID(rawA[i][0]);
        stringstream latitude(rawA[i][6]);
        stringstream longitude(rawA[i][7]);
        airportID >> insert.airportID;
        latitude >> insert.latitude;
        longitude >> insert.longitude;
        insert.nameOfAirport = rawA[i][1];
        
        insertVertex(insert);
        m[insert.airportID] = insert;
        vertices.push_back(insert);
    }

    for(size_t j = 0; j<rawR.size();j++){
        //set edge
        stringstream sourceID(rawR[j][3]);
        stringstream destID(rawR[j][5]);
        string airline = rawR[j][2];
        int sID = 0;
        int dID = 0;
        sourceID >> sID;
        destID >> dID;
        
        if (m[sID].airportID != 0 && m[dID].airportID != 0) {
            insertEdge(m[sID], m[dID], airline);
        }
        
        //set weight
        Edge sameEdge = setEdgeWeight(m[sID], m[dID], distanceCalculate(m[sID], m[dID]));
        edges.push_back(sameEdge);
    }
}

string Graph::file_to_string(const std::string & filename) {
    ifstream tex(filename);

    stringstream strStream;
    if (tex.is_open()) {
        strStream << tex.rdbuf();
    }

    return strStream.str();
}

vector<string> Graph::toVector(string s) {
    vector<string> v;
    string str;
    for(size_t i = 0; i <= s.size(); i++) {
        if (i == s.size() || s[i] == ','){
            v.push_back(str);
            str.clear();
        } else{
            str +=string(1,s[i]);
        }
    }
    return v;
}

vector<string> Graph::doSegment(string sentence) {
    std::stringstream ss(sentence);
    std::string to;
    vector<string> result;
  
    while(std::getline(ss,to,'\n')){
        result.push_back(to);
    }

    return result;
}

void Graph::insertVertex(Vertex v)
{
    adjacency_list[v] = unordered_map<Vertex, Edge, MyHashFunction>();
}

vector<Vertex> Graph::getVertices() const
{
    vector<Vertex> ret;

    for(auto it = adjacency_list.begin(); it != adjacency_list.end(); it++)
    {
        if (it->first.airportID != 0) {
            ret.push_back(it->first);
        }
        
    }

    return ret;
}

// Referenced from https://www.geeksforgeeks.org/program-distance-two-points-earth/
long double Graph::toRadians(const long double degree) 
{ 
    // cmath library in C++  
    // defines the constant 
    // M_PI as the value of 
    // pi accurate to 1e-30 
    long double one_deg = (M_PI) / 180.0; 
    return (one_deg * degree); 
}

// Reference from https://www.geeksforgeeks.org/program-distance-two-points-earth/
long double Graph::distanceCalculate(Vertex source, Vertex destination) {
    source.latitude = toRadians(source.latitude); 
    source.longitude = toRadians(source.longitude); 
    destination.latitude = toRadians(destination.latitude); 
    destination.longitude = toRadians(destination.longitude); 

    // Haversine Formula 
    long double dlong = destination.longitude - source.longitude; 
    long double dlat = destination.latitude - source.latitude; 
  
    long double ans = pow(sin(dlat / 2), 2) +  
                          cos(source.latitude) * cos(destination.latitude) *  
                          pow(sin(dlong / 2), 2); 
  
    ans = 2 * asin(sqrt(ans)); 
  
    // Radius of Earth in  
    // Kilometers, R = 6371 
    // Use R = 3956 for miles 
    long double R = 6371; 
      
    // Calculate the result 
    ans = ans * R; 
    return ans; 
}

void Graph::insertEdge(Vertex source, Vertex destination, string airline) {
    if (source.airportID == 0 || destination.airportID == 0) {
        return;
    }

    if(adjacency_list.find(source)!= adjacency_list.end() 
    && adjacency_list[source].find(destination)!= adjacency_list[source].end())
    {
        //edge already exit
        return;
    }
    
    if(adjacency_list.find(source)==adjacency_list.end())
    {
        adjacency_list[source] = unordered_map<Vertex, Edge, MyHashFunction>();
    }
    adjacency_list[source][destination] = Edge(source, destination, airline);
}

vector<Vertex> Graph::getAdjacent(Vertex source) const 
{
    auto lookup = adjacency_list.find(source);

    if(lookup == adjacency_list.end()) {
        return vector<Vertex>();
    }
        

    else
    {
        vector<Vertex> vertex_list;
        unordered_map <Vertex, Edge, MyHashFunction> & map = adjacency_list[source];
        for (auto it = map.begin(); it != map.end(); it++)
        {
            vertex_list.push_back(it->first);
        }
        return vertex_list;
    }
}

Edge Graph::getEdge(Vertex source , Vertex destination) const
{
    Edge ret = adjacency_list[source][destination];
    return ret;
}

long double Graph::getEdgeWeight(Vertex source, Vertex destination) const
{
    return adjacency_list[source][destination].getWeight();
}

Edge Graph::setEdgeWeight(Vertex source, Vertex destination, long double weight)
{
    Edge e = adjacency_list[source][destination];
    Edge new_edge(source, destination, weight, e.getAirline());
    adjacency_list[source][destination] = new_edge;
    return new_edge;
}

vector<Edge> Graph::getEdges() const
{
    if (adjacency_list.empty())
        return vector<Edge>();

    vector<Edge> ret;
    set<pair<Vertex, Vertex>> seen;

    for (auto it = adjacency_list.begin(); it != adjacency_list.end(); it++)
    {
        Vertex source = it->first;
        for (auto its = adjacency_list[source].begin(); its != adjacency_list[source].end(); its++)
        {
            Vertex destination = its->first;
            if(seen.find(make_pair(source, destination)) == seen.end())
            {
                //this pair is never added to seen
                ret.push_back(its->second);
                seen.insert(make_pair(source,destination));
            }
        }
    }

    return ret;
}
