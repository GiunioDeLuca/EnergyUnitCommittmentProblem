# powerplant-coding-challenge proposed API solution

This is a RestFul API developed with Flask 
for the powerplant-coding-challenge for 
the [GEM](https://gems.engie.com/) team of [ENGIE](https://www.engie.com/) group.

The directory 'app' contains all the files required for the deployement.
The directory example_payloads contains 
the example payloads supplied for the challenge 
and to use for tests or debugging.

## Installation

The API requires python version 3.6.

To run the API in on the local machine:

```bash
cd ENGIECHALLENGE                      # place in the root project folder
pip install -r ./app/requirements.txt  # install python packages
python ./app/app.py                    # run the API
```

If using docker:
```bash
cd ENGIECHALLENGE
docker build -t pw-challenge ./app/     # build the image
docker run -ti --rm -p 8888:8888 pw-challenge  # run container
```

## Usage
The API will be exposed on the port:8888 as essential condition for the challenge.

## Methods
### Get the production plan with POST method
#### Request
```bash
curl --location --request POST 'http://127.0.0.1:8888/productionplan' \
--header 'Content-Type: application/json' \
--data-binary '@./example_payloads/payload1.json'
```
#### Response
````json
[
  {
    "name": "gasfiredbig1",
    "p": 254
  },
  {
    "name": "gasfiredbig2",
    "p": 449
  },
  {
    "name": "gasfiredsomewhatsmaller",
    "p": 0
  },
  {
    "name": "tj1",
    "p": 0
  },
  {
    "name": "windpark1",
    "p": 146
  },
  {
    "name": "windpark2",
    "p": 33
  }
]
````

### Connect to the websocket server
#### Directly write into the browser:
```
http://localhost:8888/websocket-server
```

#### Return the http page connected to test the websocket:
```html
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>powerplants engie challenge</title>

	<script src="//code.jquery.com/jquery-1.12.4.min.js" integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ="
		crossorigin="anonymous"></script>
	<script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js"
		integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
	<script type="text/javascript">
		$(document).ready(function(){
            // namespace for the physical channel
            namespace = '/test';

            // Conncect to the Socket.IO server
            var socket = io(namespace);

            socket.on('event', function(data){
                $('#input').html(JSON.stringify(data.inp))
                $('#response').html(JSON.stringify(data.sol))
            })

        })

	</script>


</head>

<body>
	<h1>TEST WEBSOCKET Page</h1>
	<h2>Input</h2>
	<div id="input"></div>

	<h2>Response</h2>
	<div id="response"></div>
</body>

</html>
```


## Technical details
The API integrates a dynamic programming algorithm 
for a simplified modeling of the unit commitment problem.
The approach is roughly similar to 
a priority dynamic programming approach
(see [Singhal, Sharma 2011](https://ieeexplore.ieee.org/abstract/document/6075161)).
By the way, a detailed description of the algorithm and 
a sensitivity study of the parameters involved
can be directly asked to the [author](giuniodl@live.it).

The total production cost takes into account the emission allowance
by considering the emission of CO2 only for the gasfired plants
and not for the turbojet (as specified by the challenge).

The websocket is implemented by using Socket.IO. 
This allow to run the API on every browser, 
even for those ws protocol is not supported. 
However, the websocket cannot be tested with
ws based address testing modes (such as Websocket Test Client from Chrome).

For more details or questions contact directly the [author](giuniodl@live.it) 

## Author
Giunio De Luca

email: 
[giuniodl@live.it](giuniodl@live.it)

tel: +33 684 00 09 99


## License
This project is free license and 
it has been developed with the only purpose of 
advertising consulting or recruitment 
of the [author](giuniodl@live.it).

## Last Update
Paris, 22/05/2020