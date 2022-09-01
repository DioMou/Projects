-- the following code selected flight having flight frequency within certain range in December at ORD
select airline, origin_Airport, destination_airport
from "mp9_flight"."transformedflight"
where scheduled_departure>=800 and scheduled_departure<1200 and day=25 and month=12 and origin_airport='ORD'
;
-- The following code selected flight having delay time at transfer station within certain range between origin airport and destination airport
select f1.airline as Airline, f1.origin_airport as Origin_Airport, f1.destination_airport as Stopover_Airport, f2.destination_airport as Destination_Airport, f1.departure_delay as Origin_Departure_Delay, f1.arrival_delay as Stopover_Arrival_Delay, f2.departure_delay as Stopover_Departure_Delay, f2.arrival_delay as Destination_Arrival_Delay
from "mp9_flight"."transformedflight" f1, "mp9_flight"."transformedflight" f2
where f1.origin_airport='SFO' and f1.destination_airport= f2.origin_airport and f2.destination_airport= 'JFK' and f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + ((f1.scheduled_arrival / 100)*60 + (f1.scheduled_arrival % 100) - ((f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.scheduled_time)%(24*60)))>=60 and f2.day*24*60 + (f2.scheduled_departure / 100)*60 + (f2.scheduled_departure % 100) + f2.departure_delay - (f1.day*24*60 + (f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.departure_delay + f1.elapsed_time + ((f1.scheduled_arrival / 100)*60 + (f1.scheduled_arrival % 100) - ((f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.scheduled_time)%(24*60)))<=180 and f1.airline=f2.airline and f1.cancelled=0 and f2.cancelled=0
;