# IP2LOC

A tiny web server for ipv4 to geo location conversion

## System Prerequisites

- [SQLite](https://www.sqlite.org/index.html) is available 
(SQLite is included by default in [these systems](https://en.wikipedia.org/wiki/SQLite#Operating_systems).)
- Only Python3 supported, `>= 3.6` is preferred.

## Quick Start

### Installation & Start

```bash
pip install --user ip2loc-server
ip2loc
```

Now you have already started the server. 
Try

```bash
curl localhost:8080/ip2loc?ip=216.58.221.228
# {"ip": "216.58.221.228", "country_code": "NL", "country_name": "Netherlands", "region_name": "Noord-Holland", "city_name": "Amsterdam", "latitude": 52.37403, "longitude": 4.88969}
curl localhost:8080/url2loc?url=www.google.com
# {"ip": "216.58.221.228", "country_code": "NL", "country_name": "Netherlands", "region_name": "Noord-Holland", "city_name": "Amsterdam", "latitude": 52.37403, "longitude": 4.88969}
curl localhost:8080/url2loc?url=https://www.google.com
# {"ip": "216.58.221.228", "country_code": "NL", "country_name": "Netherlands", "region_name": "Noord-Holland", "city_name": "Amsterdam", "latitude": 52.37403, "longitude": 4.88969}
```

to test the server is working well ^_^. 

By default the server listens to port `8080`, you could ONLY modify this in the configure file. 
(Arguments specified listened ports are not supported)

To find paths info, run

```bash
ip2loc --showpath
```

Run `ip2loc -h` for help.

## Track the Latest Data

All the data used in this project is from 
[https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude](https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude).

For the reason that the data on this site updated monthly, you need track the latest data manually.

- Download "IPV4CSV" and remember the current version of data
![IP2LocationSiteSnapshot](docs/images/IP2LocationLite.png)

- Run `ip2loc --loaddata --dataver="current version" --datapath="CSV/DATA/PATH/NAME.ZIP"`


## How it Works

Shortly: binary search of ordered data

See [https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude](https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude) 
for details of data structure.

## Contact Me

zhenninglang@163.com