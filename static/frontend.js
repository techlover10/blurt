// A ton of code I ripped just for balloons
// Source: https://codepen.io/Jemimaabu/pen/vYEYdOy
function random(num) {
  return Math.floor(Math.random() * num);
}

function getRandomStyles() {
  var r = random(255);
  var g = random(255);
  var b = random(255);
  var mt = random(200);
  var ml = random(1000);
  var dur = random(5) + 5;
  return `
  background-color: rgba(${r},${g},${b},0.7);
  color: rgba(${r},${g},${b},0.7); 
  box-shadow: inset -7px -3px 10px rgba(${r - 10},${g - 10},${b - 10},0.7);
  margin: ${mt}px 0 0 ${ml}px;
  animation: float ${dur}s ease-in infinite
  `;
}

function createBalloons(num) {
  var balloonContainer = document.getElementById("correct");
  for (var i = num; i > 0; i--) {
    var balloon = document.createElement("div");
    balloon.className = "balloon";
    balloon.style.cssText = getRandomStyles();
    balloonContainer.append(balloon);
  }
}

// Actual view model
var GameViewModel = function() {

    // states: "init", "ingame", "waiting", "turnended"
    this.gameState = ko.observable("init")
    this.userCanSkip = ko.observable(true);
    this.currentClue = ko.observable("");
    this.currentPointVal = ko.observable("");
    this.currentAnswer = ko.observable("");
    this.waitingForUserConfirm = ko.observable(true);
    this.showWinnerDiv = ko.observable(false);

    this.scoresList = ko.observableArray([]);
    this.guessesList = ko.observableArray([]);


    this.login = function(){}

    this.proceedToWait = function()
    {
        this.gameState("waiting");
    }

    this.wonPoint = function()
    {
        this.showWinnerDiv(true);
        createBalloons(50);
    }

    this.startRound = function()
    {
        this.showWinnerDiv(false);
        this.gameState("ingame");
        this.userCanSkip(true);
        this.currentAnswer("");
    }

    this.terminateRound = function(ans)
    {
        this.gameState("turnended");
        this.currentAnswer(ans);
    }

    this.skipQuestion = function()
    {
        this.userCanSkip(false);
    }

    this.setClue = function(clue, points)
    {
        this.guessesList.removeAll();
        this.currentClue(clue);
        this.currentPointVal(points);
    }

    this.showSkipButton = function()
    {
        return (this.gameState() == "ingame" && this.userCanSkip());
    }

    this.updateScores = function(scoresArr)
    {
        this.scoresList.removeAll();
        for (let s of scoresArr)
        {
            this.scoresList.push({
                name: s.name,
                score: s.score,
                userDidSkip: false
            });
        }
    }

    this.setUserSkipped = function(username)
    {
        var targetUser = ko.utils.arrayFirst(this.scoresList(), function(player){ return player.name == username; });
        if (targetUser)
        {
            this.scoresList.replace(targetUser, {name: targetUser.name, score: targetUser.score, userDidSkip: true})
        }
    }


    
}

var thisViewModel = new GameViewModel();


window.onload = function(){
    loadit();
    ko.applyBindings(thisViewModel);
createBalloons(50);
}


