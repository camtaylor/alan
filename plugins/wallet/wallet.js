var Web3 = require('web3');
var web3 = new Web3();
var reader = require("readline");
var fs = require('fs');
var path = require('path');
var prompt = require('prompt');

web3.setProvider(new web3.providers.HttpProvider("http://localhost:8545"));
// Load wallet and addresses from json files
var wallet = JSON.parse(fs.readFileSync(path.join(__dirname, 'wallet.json'), 'utf8'));
var addresses = JSON.parse(fs.readFileSync(path.join(__dirname,'addresses.json'), 'utf8'));
//Unlock account
web3.personal.unlockAccount(wallet["address"], wallet["password"], 10000);

process.stdout.write(":speak: My ethereum wallet is open.\n");

function getRecipient() {
  process.stdout.write(":speak:Who do you want me to pay?\n");
  process.stdout.write(":listen:\n");
  prompt.get(['recipient'], function(err, result) {
    process.stdout.write("\n");
    process.stdout.write(result.recipient + "\n");
    if(addresses[result.recipient] != null) {
      getAmount(result.recipient);
    }
    else{
      process.stdout.write(":speak:I could not find an address for " + result.recipient + "\n");
      process.stdin.resume();
    }
  });

}

function getAmount(recipient){
  process.stdout.write(":speak:How many ether should I pay " + recipient + "?\n");
  process.stdout.write(":listen:\n");
  prompt.get(['amount'], function(err, result) {
    process.stdout.write("\n");
    process.stdout.write(result.amount + "\n");
    var amount = parseFloat(result.amount);
    if(amount != NaN) {
      send(recipient, amount);
    }
    else{
      process.stdout.write(":speak:I can't send " + result.amount + "\n");
      process.stdin.resume();
    }
  });
}

function send(address, amount){
  process.stdout.write(":speak:Are you sure I should pay " + address + " " + amount + " ether?\n");
  process.stdout.write(":listen:\n");
  prompt.get(['confirmation'], function(err, result) {
    if (result.confirmation.toLowerCase() == "yes") {
      var transaction = web3.eth.sendTransaction({from: wallet["address"], to: addresses[address], value: amount});
      process.stdout.write(transaction + "\n");
      process.stdout.write("Sent " + amount + " to " + address + "\n");
      process.stdin.resume();
    }
    else {
      process.stdout.write("Cancelling transaction \n");
      process.stdin.resume();
    }
  });
}

function balance(){
  process.stdout.write(":speak: My wallet balance is: \n");
  process.stdout.write(":speak:" + web3.eth.getBalance(wallet["address"]) + " wei\n");
}

process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', function(data) {
  data = data.trim();
  switch(data){
    case "send":
      getRecipient();
      break;
    case "balance":
      balance();
      break;
    case "request":
      break;
    case "exit":
      process.stdout.write(":speak:Closing my wallet.");
      process.exit();
      break;

  }
});