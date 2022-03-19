# boyouh2-yuzhao5-jael2-lmou2

## Team Members: Yu (William) Zhao, Jae Lee, Boyou Han, Lingxiao Mou

### Final Presentation
Check out our final presentation here: https://drive.google.com/file/d/1poYTXSCDcKFgcMo-urg71MroKVYweaE_/view?usp=sharing

### Dataset
We are using the OpenFlights dataset (https://openflights.org/data.html) for our project. The users can input the airport ID based on “Datasets/Airport.txt” and “Datasets/Routes.txt” for their source and destination. 

*Below is a sample line from airport.txt :*

507,"London Heathrow Airport","London","United Kingdom","LHR","EGLL",51.4706,-0.461941,83,0,"E","Europe/London","airport","OurAirports"

(Airport ID,Name,City,Country,IATA,ICAO,Latitude,Longitude,Altitude,Timezone,DSTTz database time zone,Type,Source)


*Below is a sample line from routes.txt :*

BA,1355,SIN,3316,LHR,507,,0,744 777

(Airline,AirlineID,Source airport,Source airportID, destination airport,destination airportID,Codeshare,Stops,Equipment)


### Running Our Project
To run our project, please run the following commands.

`make -j$(nproc)`

`./final`

After running the final command, our program will ask you for the source and destination airport IDs which can be found in “Datasets/Airport.txt”. Upon receiving input, our program would generate a graph with airports as Vertex and Edges as routes between the airports. Then, it is going to select the shortest path (Dijkstra’s Algorithm) between the chosen source and destination and project the route to a PNG image called “output.png. This png file gives the user an overview of the path they want to take. The exact detail, including all visited airports, can be found in the output prints.

*Sample Output*

`Please enter a valid source airport ID: 3320`

`Source Airport: "Brisbane International Airport"`

`Please enter a destination airport ID from 'Datasets/Airports.txt': 1212`

`Destination Airport: "Alicante International Airport"`

`Shortest Distance: 17293.5 KM`

![alt text](https://github-dev.cs.illinois.edu/cs225-fa20/boyouh2-yuzhao5-jael2-lmou2/blob/master/sample.png?raw=true)


## Running Test Cases
To run our test cases, please run the following commands:

`make test -j$(nproc)`

`./test`

This will run the catch-based test cases implemented in “tests/test.cpp”. 
