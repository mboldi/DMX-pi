var express = require('express');
var app = express();
var fs = require("fs");

var uidata;
var lampdata;

app.get('/init', function(req, res){
     fs.readFile(__dirname + "/data.json", 'utf8', function(err, data){
          if(err) throw err;
          uidata = JSON.parse(data);
     });

     fs.readFile(__dirname + "/lamps.json", 'utf8', function(err, data){
          if (err) throw err;
          lampdata = JSON.parse(data);
     });

     res.end("loaded")
})
/*
app.get('/varGet', function(req, res){
     res.end(JSON.stringify(uidata));
})*/

app.get('/uidata', function (req, res) {
   /*fs.readFile( __dirname + "/" + "data.json", 'utf8', function (err, data) {


          //console.log("Teljes adatlekeres");
          res.end( data );
   });*/

   res.end(JSON.stringify(uidata));
})

app.get('/lampdata', function (req, res) {
   /*fs.readFile( __dirname + "/" + "lamps.json", 'utf8', function (err, data) {
          //console.log("Teljes adatlekeres");
          res.end( data );
   });*/

   res.end(JSON.stringify(lampdata));
})

app.get('/lampdata/:id', function(req, res) {
     res.end(JSON.stringify(lampdata["lamp" + req.params.id]));
})

app.get('/dataelem/:id', function(req, res) {
     /*fs.readFile( __dirname + "/" + "data.json", 'utf8', function (err, data) {
          //console.log(req.params.id);
          adatok = JSON.parse(data);
          var adat = adatok["pot: " + req.params.id] 
          //console.log( adat );
          res.end( JSON.stringify(adat));
     });*/
     var adat = uidata["pot" + req.params.id];
     res.end(JSON.stringify(adat));
})

app.get('/updatePot/:id/:level', function(req, res) {
     /*fs.readFile(__dirname + "/" + "data.json", 'utf8', function(err, data) {
          adat = JSON.parse(data);
          var pot = adat["pot" + req.params.id];

          var level = req.params.level;
          //console.log("id: " + adat["pot" + req.params.id]["color"] + " level: " + level);

          pot["level"] = parseInt(level);
          adat["pot" + req.params.id] = pot;
          fs.writeFile(__dirname + "/" + "data.json", JSON.stringify(adat), 'utf8', function(err) {
               if (err) throw err;
          });

          res.end(JSON.stringify(adat["pot" + req.params.id]));
     });*/

     var pot = uidata["pot" + req.params.id];
     pot["level"] = parseInt(req.params.level);

     uidata["pot" + req.params.id] = pot;

     fs.writeFile(__dirname + "/" + "data.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     //console.log(JSON.stringify(pot));

     res.end(JSON.stringify(pot));
})

app.get('/updateSel/:id', function(req, res) {
     /*fs.readFile(__dirname + "/" + "data.json", 'utf8', function(err, data) {
          adat = JSON.parse(data);
          var lamSel = adat["lamSel"];
          var butState = lamSel["State" + req.params.id];

          if (butState == 0){
               butState = 1;
          }else{
               butState = 0;
          }

          adat["lamSel"]["State" + req.params.id] = butState;

          //console.log("State" + req.params.id + ": " + butState);

          fs.writeFile(__dirname + "/" + "data.json", JSON.stringify(adat), 'utf8', function(err) {
               if (err) throw err;
          });

          res.end(JSON.stringify(adat["lamSel"]["State" + req.params.id]));
     });*/

     var butState = uidata["lamSel"]["State" + req.params.id];

     if (butState == 0){
               butState = 1;
          }else{
               butState = 0;
          }

     uidata["lamSel"]["State" + req.params.id] = parseInt(butState);

     fs.writeFile(__dirname + "/" + "data.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     //console.log(butState);

     res.end(JSON.stringify(butState));
})

app.get('/updateLamp/:id/:r/:g/:b/:l', function(req, res) {
     /*fs.readFile(__dirname + "/lamps.json", "utf8", function(err, data) {
          adat = JSON.parse(data);
          var lamp = adat["lamp" + req.params.id];
          lamp["r"] = req.params.r;
          lamp["g"] = req.params.g;
          lamp["b"] = req.params.b;
          lamp["l"] = req.params.l;

          adat["lamp" + req.params.id] = lamp;

          fs.writeFile(__dirname + "/lamps.json", JSON.stringify(adat), 'utf8', function(err) {
               if (err) throw err;
          });
          res.end(JSON.stringify(lamp))
     });*/

     var lamp = lampdata["lamp" + req.params.id];
     lamp["r"] = parseInt(req.params.r);
     lamp["g"] = parseInt(req.params.g);
     lamp["b"] = parseInt(req.params.b);
     lamp["l"] = parseInt(req.params.l);

     lampdata["lamp" + req.params.id] = lamp;
     fs.writeFile(__dirname + "/lamps.json", JSON.stringify(lampdata), 'utf8', function(err) {
          if (err) throw err;
     });

     res.end(JSON.stringify(lampdata));
})

var server = app.listen(8081, function () {
     var host = server.address().address
     var port = server.address().port

     //console.log("Example app listening at http://%s:%s", host, port)
})