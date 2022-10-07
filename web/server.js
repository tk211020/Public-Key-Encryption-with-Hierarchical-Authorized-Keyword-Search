let http = require("http")
let myApp = http.createServer(function (req,res) {
    res.end("welcome")
 });
 myApp.listen(3000)