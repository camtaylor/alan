//Lets require/import the HTTP module
var http = require('http');

//Lets define a port we want to listen to
const PORT=8080; 

//We need a function which handles requests and send response
function handleRequest(request, response){
    response.end('It Works!! Path Hit: ' + request.url);
    console.log(":notify:Someone connected to the server");
}

//Create a server
var server = http.createServer(handleRequest);

//Lets start our server
server.listen(PORT, "0.0.0.0");

//Callback triggered when server is successfully listening. Hurray!
console.log(":speak:Server listening on: http://localhost:%s", PORT);
console.log(":release:");

