# Inrix-API-Ingestion
An API that stores INRIX data as csv files on your hard drive.

## Setup
After cloning this repo, create an .env file in the same directory as this with these variables
```
TOKEN_API =
DSD_API =
```
Obtain your INRIX API URLs(through the INRIX website), and place them in the respective variables

Note: the DSD API URL should look something like the one below with brackets where the access token would go

'https://dsd.api.inrix.com/v2/DangerousSlowdowns?GeoID=208&units=0&accesstoken={}'
