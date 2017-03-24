var express = require('express');
var app = express();
var fs = require("fs");

var nonDelData;
var uidata;

app.get('/init', function(req, res){
     fs.readFile(__dirname + "/data.json", 'utf8', function(err, data){
          if(err) throw err;
          //console.log("string: " + data);
          nonDelData = JSON.parse(data);
     });

     //console.log("json: " +  JSON.stringify(nonDelData));

     fs.readFile(__dirname + "/uidata.json", 'utf8', function(err, data){
          if (err) throw err;
          uidata = JSON.parse(data);
     });

     res.end("loaded")
})

app.get('/bankdata', function (req, res) {
   res.end(JSON.stringify(nonDelData));
})

app.get('/getbank/:id', function(req, res){
     res.end(JSON.stringify(nonDelData["bank" + req.params.id]))
})

app.get('/uidata', function (req, res) {
   res.end(JSON.stringify(uidata));
})

app.get('/lampdata/:id', function(req, res) {
     res.end(JSON.stringify(uidata["lamp" + req.params.id]));
})

app.get('/pot/:id', function(req, res) {
     var adat = uidata["pot"][parseInt(req.params.id)];
     res.end(JSON.stringify(adat));
})

app.get('/updatePot/:id/:level', function(req, res) {
     uidata["pot"][parseInt(req.params.id)] = parseInt(req.params.level);

     fs.writeFile(__dirname + "/" + "uidata.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     res.end(JSON.stringify(uidata["pot"][parseInt(req.params.id)]));
})

app.get('/updateSel/:id', function(req, res) {
     var butState = uidata["lamSel"][parseInt(req.params.id)];

     if (butState == 0){
               butState = 1;
          }else{
               butState = 0;
          }

     uidata["lamSel"][parseInt(req.params.id)] = parseInt(butState);

     fs.writeFile(__dirname + "/" + "uidata.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     res.end(JSON.stringify(uidata["lamSel"][parseInt(req.params.id)]));
})

app.get('/updateLamp/:id/:r/:g/:b/:l', function(req, res) {
     var lamp = uidata["lamp" + req.params.id];
     lamp["r"] = parseInt(req.params.r);
     lamp["g"] = parseInt(req.params.g);
     lamp["b"] = parseInt(req.params.b);
     lamp["l"] = parseInt(req.params.l);

     uidata["lamp" + req.params.id] = lamp;
     fs.writeFile(__dirname + "/uidata.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     res.end(JSON.stringify(uidata["lamp" + req.params.id]));
})

app.get('/updateDmxCh/:id/:level', function(req, res){
     uidata["dmxCh"][parseInt(req.params.id)] = parseInt(req.params.level);

     fs.writeFile(__dirname + "/uidata.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     res.end(JSON.stringify(uidata["dmxCh"][parseInt(req.params.id)]));
})

app.get('/dmxch/:id', function(req, res){
     res.end(JSON.stringify(uidata["dmxCh"][parseInt(req.params.id)-1]));
})

app.get('/getLamp/:id', function(req, res){
     res.end(JSON.stringify(uidata["lamp" + req.params.id]));
})

app.get('/updateBank/:bank', function(req, res){
     uidata["bank"] = parseInt(req.params.bank);

     fs.writeFile(__dirname + "/uidata.json", JSON.stringify(uidata), 'utf8', function(err) {
          if (err) throw err;
     });

     res.end(JSON.stringify(uidata["bank"]));
})

var server = app.listen(8081, function () {
     var host = server.address().address
     var port = server.address().port

     //console.log("Example app listening at http://%s:%s", host, port)
})