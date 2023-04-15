var GameViewModel = function() {

    // states: "init", "ingame", "wonpoint", "waiting", "turnended"
    this.gameState = ko.observable("init")
    this.userCanSkip = ko.observable(true);
    this.currentClue = ko.observable("");
    this.currentPointVal = ko.observable("");
    this.currentAnswer = ko.observable("");
    this.waitingForUserConfirm = ko.observable(true);

    this.scoresList = ko.observableArray([]);
    this.guessesList = ko.observableArray([]);

    this.login = function(){}

    this.proceedToWait = function()
    {
        this.gameState("waiting");
    }

    this.wonPoint = function()
    {
        this.gameState("wonpoint");
    }

    this.startRound = function()
    {
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
            targetUser.userDidSkip = true;
        }
    }


    
}

var thisViewModel = new GameViewModel();


window.onload = function(){
    loadit();
    ko.applyBindings(thisViewModel);
}
