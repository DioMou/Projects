#include "../cs225/catch/catch.hpp"

#include "../cs225/PNG.h"
#include "../cs225/HSLAPixel.h"

#include "../graph.h"
#include "../shortestpath.h"
#include "../draw.h"

using namespace cs225;


TEST_CASE("test graph constructor with small dataset", "[weight=1][valgrind]") {
    Graph small = Graph("tests/test_dataset_constructor_routes.txt", "tests/test_dataset_constructor_airports.txt");
    REQUIRE(small.getVertices().size() == 9);
    REQUIRE(small.getEdges().size() == 5);
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex PEK = Vertex(3364, 116.58499908447266, 40.080101013183594, "Beijing Capital International Airport");
    Edge route = Edge(ORD, PEK, "HU");
    REQUIRE(small.getEdge(ORD, PEK) == route);
    REQUIRE(small.getAdjacent(ORD).size() == 1);
    REQUIRE(std::find(small.getAdjacent(ORD).begin(), small.getAdjacent(ORD).end(), PEK) != small.getAdjacent(ORD).end());
}

TEST_CASE("test graph constructor with large dataset", "[weight=1][valgrind]") {
    Graph large = Graph("Datasets/Routes.txt", "Datasets/Airports.txt");
    REQUIRE(large.getVertices().size() == 7698);
    REQUIRE(large.getEdges().size() == 37336);
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex PEK = Vertex(3364, 116.58499908447266, 40.080101013183594, "Beijing Capital International Airport");
    Vertex CMI = Vertex(4049, -88.27809906, 40.03919983, "University of Illinois Willard Airport");
    Edge route = Edge(ORD, PEK, "HU");
    REQUIRE(large.getEdge(ORD, PEK) == route);
    REQUIRE(large.getAdjacent(CMI).size() == 2);
    REQUIRE(std::find(large.getAdjacent(ORD).begin(), large.getAdjacent(ORD).end(), PEK) != large.getAdjacent(ORD).end());
}

TEST_CASE("test BFS with small dataset", "[weight=1][valgrind]") {
    Graph small = Graph("tests/test_dataset_shortestpath_routes.txt", "tests/test_dataset_shortestpath_airports.txt");
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex PEK = Vertex(3364, 116.58499908447266, 40.080101013183594, "Beijing Capital International Airport");
    Vertex SZX = Vertex(3374, 113.81099700927734, 22.639299392700195, "Shenzhen Bao'an International Airport");
    Edge route1 = Edge(PEK, ORD, "HU");
    Edge route2 = Edge(SZX, PEK, "HU");

    ShortestPath direct(PEK, ORD);
    std::vector<Edge> directPath = direct.BFS(small);
    REQUIRE(directPath.size() == 1);
    REQUIRE(directPath[0] == route1);
}

TEST_CASE("test shortest distance algorithm with small dataset", "[weight=1][valgrind]") {
    Graph small = Graph("tests/test_dataset_shortestpath_routes.txt", "tests/test_dataset_shortestpath_airports.txt");
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex PEK = Vertex(3364, 116.58499908447266, 40.080101013183594, "Beijing Capital International Airport");
    Vertex SZX = Vertex(3374, 113.81099700927734, 22.639299392700195, "Shenzhen Bao'an International Airport");
    Edge route1 = Edge(PEK, ORD, "HU");
    Edge route2 = Edge(SZX, PEK, "HU");

    ShortestPath direct(PEK, ORD);
    std::vector<Edge> directPath = direct.Dijkstra(small);
    REQUIRE(directPath.size() == 1);
    REQUIRE(directPath[0] == route1);

    ShortestPath transfer(SZX, ORD);
    std::vector<Edge> transferPath = transfer.Dijkstra(small);
    REQUIRE(transferPath.size() == 2);
    REQUIRE(transferPath[0] == route2);
    REQUIRE(transferPath[1] == route1);

}

TEST_CASE("test shortest distance algorithm with large dataset", "[weight=1][valgrind]") {
    Graph large = Graph("Datasets/Routes.txt", "Datasets/Airports.txt");
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex PEK = Vertex(3364, 116.58499908447266, 40.080101013183594, "Beijing Capital International Airport");
    Vertex SZX = Vertex(3374, 113.81099700927734, 22.639299392700195, "Shenzhen Bao'an International Airport");
    Edge route1 = Edge(PEK, ORD, "HU");
    Edge route2 = Edge(SZX, PEK, "HU");
    
    ShortestPath direct(PEK, ORD);
    std::vector<Edge> directPath = direct.Dijkstra(large);
    REQUIRE(directPath.size() == 1);
    REQUIRE(directPath[0] == route1);

    ShortestPath transfer(SZX, ORD);
    std::vector<Edge> transferPath = transfer.Dijkstra(large);
    REQUIRE(transferPath.size() == 2);
    REQUIRE(transferPath[0] == route2);
    REQUIRE(transferPath[1] == route1);
}

TEST_CASE("test graphical output with small dataset", "[weight=1][valgrind]") {
    Graph small = Graph("tests/test_dataset_shortestpath_routes.txt", "tests/test_dataset_shortestpath_airports.txt");
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex SZX = Vertex(3374, 113.81099700927734, 22.639299392700195, "Shenzhen Bao'an International Airport");
    ShortestPath path(SZX, ORD);
    std::vector<Edge> edges = path.Dijkstra(small);
    Draw D(edges);
    D.convert();    
    D.draw("./world_map.png", "test_output1.png", false);
    cs225::PNG i; i.readFromFile("test_output1.png");
    cs225::PNG ans; ans.readFromFile("./tests/test_soln.png");
    REQUIRE(i == ans);
}

TEST_CASE("test graphical output with large dataset", "[weight=1][valgrind]") {
    Graph large = Graph("Datasets/Routes.txt", "Datasets/Airports.txt");
    Vertex ORD = Vertex(3830, -87.9048, 41.9786, "Chicago O'Hare International Airport");
    Vertex SZX = Vertex(3374, 113.81099700927734, 22.639299392700195, "Shenzhen Bao'an International Airport");
    ShortestPath path(SZX, ORD);
    std::vector<Edge> edges = path.Dijkstra(large);
    Draw D(edges);
    D.convert();    
    D.draw("./world_map.png", "test_output2.png", false);
    cs225::PNG i; i.readFromFile("test_output2.png");
    cs225::PNG ans; ans.readFromFile("./tests/test_soln.png");
    REQUIRE(i == ans);
}

