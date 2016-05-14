//Lets require/import the HTTP module
var http = require('http');
var url = require('url') ;

//Lets define a port we want to listen to
const PORT=8080; 

//We need a function which handles requests and send response
function handleRequest(request, response){
    // Get sentence from url
    var sentence = url.parse(request.url,true).query['sentence'];
    sentence = sentence.toLowerCase();
    //console.log(sentence);
    // Pass the sentence to alan to think.
    console.log(":think:" + sentence);
    var readline = require('readline');
    var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
    });

    rl.on('line', function(line){
        var alanResponse = {
            "response" : line
        }
        response.end(JSON.stringify(alanResponse));
        console.log(":speak:" + line + "\n");
        rl.close();
    })
}

//Create a server
var server = http.createServer(handleRequest);

//Lets start our server
server.listen(PORT, "0.0.0.0");

//Callback triggered when server is successfully listening. Hurray!
console.log(":speak:Server listening on: http://localhost:%s", PORT);
// console.log(":release:");

