# pipeline_nyc_taxi
Homework 1 - DataTalks Data Enginerring Zoomcamp 2026

# Questions

1. For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?
- Query:
  SELECT COUNT(*) 
  FROM public.green_taxi_data
  WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
  AND trip_distance <= 1;
*ANSWER*: **8007**
