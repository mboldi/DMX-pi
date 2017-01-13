var express = require('express');
var app = express();
var fs = require("fs");

app.get('/dataelem', function (req, res) {
   fs.readFile( __dirname + "/" + "data.json", 'utf8', function (err, data) {
          console.log( data );
          res.end( data );
   });
})

app.get('/dataelem/:id', function(req, res) {
	fs.readFile( __dirname + "/" + "data.json", 'utf8', function (err, data) {
          console.log(req.params.id);
          adatok = JSON.parse(data);
          var adat = adatok["pot: " + req.params.id] 
          console.log( adat );
          res.end( JSON.stringify(adat));
   });
})

app.get('/updatePot/:id/:level', function(req, res) {
     fs.readFile(__dirname + "/" + "data.json", 'utf8', function(err, data) {
          adat = JSON.parse(data);
          var pot = adat["pot" + req.params.id];

          var level = req.params.level;/*
          if (req.params.level <= 255 && req.params.level >= 0){
               level = req.params.level;
          }else if(req.params.level < 0){
               level = 0;
          }else{
               level = 255;
          }*/
          console.log("id: " + adat["pot" + req.params.id]["color"] + " level: " + level);

          pot["level"] = level;
          adat["pot" + req.params.id] = pot;
          fs.writeFile("data.json", JSON.stringify(adat), 'utf8', function(err) {
               if (err) throw err;
          });

          res.end(JSON.stringify(adat["pot" + req.params.id]));
     });
})

app.get('/updateSel/:id', function(req, res) {
     fs.readFile(__dirname + "/" + "data.json", 'utf8', function(err, data) {
          adat = JSON.parse(data);
          var lamSel = adat["lamSel"];
          var butState = lamSel["State" + req.params.id];

          if (butState == 0){
               butState = 1;
          }else{
               butState = 0;
          }

          adat["lamSel"]["State" + req.params.id] = butState;

          fs.writeFile("data.json", JSON.stringify(adat), 'utf8', function(err) {
               if (err) throw err;
          });

          res.end(JSON.stringify(adat["lamSel"]["State" + req.params.id]));
     });
})

var server = app.listen(8081, function () {
     var host = server.address().address
     var port = server.address().port

     console.log("Example app listening at http://%s:%s", host, port)
})