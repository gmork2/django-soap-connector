# django-soap-connector

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gmork2/django-soap-connector.svg?branch=master)](https://travis-ci.com/gmork2/django-soap-connector)

Django project to connect to an existing SOAP web service and transform it into a REST API.

## Getting Started

This application constitutes a proof of concept and is totally experimental, use it at your own risk! 
You can test the application using the VIES validation service.

What is *VIES* (VAT Information Exchange System)?

> It is an electronic mean of validating VAT-identification numbers of economic operators registered in 
> the European Union for cross border transactions on goods or services. 

https://ec.europa.eu/taxation_customs/vies/

### Prerequisites
It is not recommended to use memcached with this project.

### Installation
Inside the downloaded repository folder, create a virtual environment and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage
Run the django web server and explore the browserable api: 
```bash
python manage.py runserver 8000
```
Initialize client and it will automatically retrieve the WSDL file passed in the post request:
```bash
curl --location --request POST 'http://127.0.0.1:8000/api/client/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "wsdl": "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
}'
```
Finds out what services, ports and operations are available to this client:
```bash
curl --location --request GET 'http://127.0.0.1:8000/api/client/1/service/'
```
Verify the validity of a VAT number:
```bash
curl --location --request POST 'http://127.0.0.1:8000/api/client/1/service/checkvatservice/checkvatport/checkvat' \
--header 'Content-Type: application/json' \
--data-raw '{
    "countryCode": "ES",
    "vatNumber": "12345678"
}'
```

## Authors
**Fernando M** - https://bitbucket.org/gmork2/

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE
Version 3 - see the [LICENSE](LICENSE) file for details.
