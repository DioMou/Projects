#pragma once

#include <string>
#include <limits.h>
#include "Vertex.h"

using std::string;

using namespace std;
// typedef string Vertex;
/**
 * Represents an edge in a graph; used by the Graph class.
 */
class Edge
{
  public:
    Vertex source; /**< The source of the edge **/
    Vertex destination; /**< The destination of the edge **/
    bool visited;
    long double weight;/**the distance between two Vertex(airport)*/
    string airline;/**the airline name*/



    /**
     * Parameter constructor for weighted graphs.
     * @param s - one vertex the edge is connected to
     * @param d - the other vertex it is connected to
     * @param w - the weight of the edge
     * @param arli - the edge label
     */
    Edge(Vertex s, Vertex d, long double w, string arli)
        : source(s), destination(d) ,visited(false), weight(w), airline(arli)
    { /* nothing */
    }

    /**
     * Default constructor.
     */
    Edge() : source(Vertex()), destination(Vertex()), visited(false),weight(-1), airline("")
    { /* nothing */
    }

    /** * Parameter constructor for unweighted graphs. * @param s - one vertex the edge is connected to * @param d - the other vertex it is connected to * @param arli - the edge label */ 
    Edge(Vertex s, Vertex d, string arli) : source(s), destination(d), visited(false), weight(-1) ,airline(arli) {  } 

    /**
     * Compares two Edges.
     * operator< is defined so Edges can be sorted with std::sort.
     * @param other - the edge to compare with
     * @return whether the current edge is less than the parameter
     */
    bool operator<(const Edge& other) const
    {
        return weight < other.weight;
    }

    /**
     * Gets edge label.
     */
    string getAirline() const
    {
        return this->airline;
    }

    /**
     * Gets edge weight.
     */
    long double getWeight() const
    {
        return this->weight;
    }

    bool operator==(const Edge& other) const
    {
        if (this->source.airportID == other.source.airportID 
            && this->destination.airportID == other.destination.airportID)
            return true;

        return false;
    }
};
