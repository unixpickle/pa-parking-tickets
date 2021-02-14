# pa-parking-tickets

Scraping [Philadelphia's Parking Portal](https://onlineserviceshub.com/ParkingPortal/Philadelphia) for unpaid parking ticket data. This website lets you search unpaid tickets by license plate.

I have so far dumped data from [over 70K parking tickets](data). In the following section, I describe some high-level results. Detailed results and plots can be viewed in the Jupyter notebook [analysis.ipynb](analysis.ipynb).

# Summary

Stats from the current dump:

```
total tickets: 76,352
unique plates: 15,804
  total fines: $6,036,978.58
```

Top 10 violations, with number of tickets:

```
20725 METER EXPIRED
10120 STOPPING PROHIBITED
 8059 PARKING PROHIBITED
 4626 OVER TIME LIMIT
 3503 FIRE HYDRANT
 3319 SIDEWALK
 3254 METER EXPIRED CC
 2660 BUS ONLY ZONE
 2473 EXPIRED INSPECTION
 2263 PHOTO RED LIGHT
```

Top 10 vehical makes with number of tickets:

```
9371 FORD
7293 CHRY
6172 CHEV
5423 DODG
5251 NISS
3945 
3867 PLYM
2606 TOYT
2539 BENZ
2357 MERC
```
