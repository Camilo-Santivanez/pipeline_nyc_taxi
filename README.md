# pipeline_nyc_taxi
Homework 1 - DataTalks Data Enginerring Zoomcamp 2026

# Questions

1. For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile? 
```
  SELECT COUNT(*) 
  FROM public.green_taxi_data
  WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
  AND trip_distance <= 1;
```
- *ANSWER*: **8007**

2. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors). *Use the pick up time for your calculations.*

```
SELECT lpep_pickup_datetime 
FROM public.green_taxi_data
WHERE trip_distance = (
	SELECT MAX(trip_distance)
	FROM public.green_taxi_data
	WHERE trip_distance <100
);
```
- *ANSWER*: **2025-11-14**

3.Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

```
WITH C1 AS (
	SELECT "PULocationID", SUM(total_amount) as total
	FROM public.green_taxi_data
	WHERE lpep_pickup_datetime >= '2025-11-18 00:00:00' 
  		AND lpep_pickup_datetime <  '2025-11-19 00:00:00'
	GROUP BY "PULocationID"
)
SELECT "Zone"
FROM public.taxi_zones
JOIN C1 ON "LocationID" = "PULocationID" 
AND total = (
	SELECT MAX(total)
	FROM C1
);
```
- *ANSWER*: **East Harlem North**

