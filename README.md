# CNB Exchange Rates API

Exchange rates API is a free service for current foreign exchange rates [published by the Czech National Bank](https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/).

[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m779426128-6b6e81ed8dc987db17d4cad2.svg)](https://stats.uptimerobot.com/q20jpuoRv)
[![Build Status](https://travis-ci.org/QuarKUS7/converter.svg?branch=master)](https://travis-ci.org/QuarKUS7/converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage

### API Endpoint

http://cnbrates.pgc.sk/

#### Latest rates
Get the latest foreign exchange rates.

```http
GET http://cnbrates.pgc.sk/latest
```
Rates are quoted against the Czech koruna (CZK) by default. For quotation against a different currency, set the base parameter in your request.

```http
GET http://cnbrates.pgc.sk/latest?base=EUR
```

Request specific exchange rates by setting the rates parameter.

```http
GET http://cnbrates.pgc.sk/latest?symbols=USD,GBP
```

API supports currency symbols

```http
GET http://cnbrates.pgc.sk/latest?base=$
```

```http
GET http://cnbrates.pgc.sk/latest?base=EUR&rates=Kč,¥,CN¥,£,R,TL,฿,AU$,R$,S$,NZ$,MX$,CA$,HK$,₪,Dkr,kn,Skr,₱,zł,₩,Ft,Rp,Rs,Ikr,RM,Nkr
```
#### Currency converter
Convert from currency to another using CNB rates.

```http
GET http://cnbrates.pgc.sk/currency_converter?amount=99.99&input_currency=$&output_currency=EUR
```
Covnert from one currency to all known currencies.

```http
GET http://cnbrates.pgc.sk/currency_converter?amount=99.99&input_currency=RUB
```

#### Rates history
TBA

#### Client side usage

The primary use case is client side. For instance, with [money.js](https://openexchangerates.github.io/money.js/) in the browser

```js
let demo = () => {
  let rate = fx(1).from("GBP").to("USD")
  alert("£1 = $" + rate.toFixed(4))
}

fetch('http://cnbrates.pgc.sk/latest')
  .then((resp) => resp.json())
  .then((data) => fx.rates = data.rates)
  .then(demo)
```

## API wrapper
* TBA

## Stack

Exchange rates API is built upon Flask_RESTful to enforce REST principles. Gunicorn serves as a WSGI Server. Nginx is used as a reverse proxy. Redis is used for caching. Everything is dockerized.

#### Libraries used
* [Flask](https://github.com/pallets/flask)
* [Flask-RESTful](https://github.com/flask-restful/flask-restful)
* [requests](https://github.com/requests/requests)
* [gunicorn](https://github.com/benoitc/gunicorn)
* [redis-py](https://github.com/andymccurdy/redis-py)


## Deployment
#### Docker
Clone this repo and in root directory run docker-compose.

```shell
docker-compose up
```

## Contributing
Thanks for your interest in the project! All pull requests are welcome from developers of all skill levels. To get started, simply fork the master branch on GitHub to your personal account and then clone the fork into your development environment.

Peter Pagáč (quarkus7 on Github) is the original creator of the CNB Exchange Rates API framework.

## License
MIT
