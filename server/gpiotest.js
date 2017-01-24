var gpio = require('rpi-gpio');
var MCP3008 = require('mcp3008.js'), 
	adc = new MCP3008(),
	channel = 0;
var MCP23017 = require('node-mcp23017'),
	mcp = new MCP23017({
		address: 0x20,
		device: '/dev/i2c-1',
		debug: false
	});

var state = 0;
var pot = 0;
var lastValue = 0;

gpio.setup(29, gpio.DIR_OUT);


function map(value, imin, imax, jmin, jmax){
	return parseInt((value - imin) * (jmax - jmin) / (imax - imin) + jmin)
};

adc.poll(0, 1000/24, function(value){
	value = map(value, 0, 1023, 0, 255)
	if(value != pot){
		pot = value;
		console.log('New value is: ' + pot);
	}
});

gpio.on('change', function(channel, value){
	if(value == true){
		state = !state;
		gpio.write(29, state);
		console.log('channel: ' + channel + ' value is now: ' + state);
	}
});
gpio.setup(7, gpio.DIR_IN, gpio.EDGE_BOTH);

function read(){
	console.log("read");
	mcp.digitalRead(0, function (err, value){
		console.log("read")
		if (err) throw err;
		console.log("past err throw");

		if(value != lastValue){
			lastValue = value;
			console.log("New value is: " + value);
		}
	});
}

setInterval(read, 1000/24);