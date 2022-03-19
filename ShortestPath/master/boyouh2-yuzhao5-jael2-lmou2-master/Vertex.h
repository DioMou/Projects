#pragma once

#include <string>
#include <limits.h>
#include <float.h>

using std::string;
using namespace std;

class Vertex{
public:
    int airportID;
    long double longitude;
    long double latitude;
    string nameOfAirport;

    // default
    Vertex() : airportID(0), longitude(0.0), latitude(0.0), nameOfAirport("") { }

    Vertex(int airID, long double longti, long double lati, string airport) : 
        airportID(airID), longitude(longti), latitude(lati), nameOfAirport(airport) { }

    /**
     * Compares two Vertex' airportID, longitude and latitude.
     * @param other - the Vertex to compare with
     */
    bool operator==(const Vertex& other) const {
        if(this->airportID != other.airportID){return false;}
        return true;
    }

    bool operator!=(Vertex& other) const {
        return this->airportID != other.airportID;
    }

    void operator=(const Vertex& other) {
        this->airportID = other.airportID;
        this->latitude = other.latitude;
        this->longitude = other.longitude;
        this->nameOfAirport = other.nameOfAirport;
    }

    bool operator<(const Vertex& other) const {
        return this->airportID < other.airportID;
    }

};

class MyHashFunction { 
public: 
  
    // Use sum of lengths of first and last names 
    // as hash function. 
    size_t operator()(const Vertex& p) const { 
        return p.airportID;
    } 
};
