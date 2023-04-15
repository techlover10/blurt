

HOST = 'ws://localhost:8765'


var gm = null;

class GameManager {
    constructor() {
        this.sock = new WebSocket(HOST);
        this.sock.addEventListener('message', this.handlermaker())
    }
    reload() {
        this.sock = new WebSocket(HOST);
        this.sock.addEventListener('message', this.handlermaker())
    }
    handlermaker() {
        let self = this; // this shit again
        function cb(e) {
            let dat = JSON.parse(e.data);
            console.log(dat);
            let t = dat['type'];
            if(t == 'clue') {
                thisViewModel.startRound();
                console.log('clue handling part, ', dat);
                // note that ping is supposed to happen here too...
                let o = {'pong': 1, user: self.name};
                self.sock.send(JSON.stringify(o));
                thisViewModel.setClue(dat.clue, dat.value);
            }
            else if(t == 'end') {
                thisViewModel.terminateRound(dat.answer);
                thisViewModel.waitingForUserConfirm(true);
                console.log('end of round, ', dat);
                thisViewModel.updateScores(dat.scores);
            }
            else if(t == 'reg') {
                thisViewModel.proceedToWait();
            }
            else if(t == 'right') {
                thisViewModel.wonPoint();
            }
            else if(t == 'scores') {
                thisViewModel.updateScores(dat.scores);
            }
            else if(t == 'skip') {
                console.log('skippa')
                let namedivs = document.querySelectorAll(".username")
                for(let d of namedivs) {
                    if(d.textContent == dat['name']) {
                        d.textContent = dat['name'] + "*";
                    }
                }
            }
            else if(t == 'guess') {
                thisViewModel.guessesList.push({
                    name: dat.name,
                    guess: dat.guess
                });
            }
            else {
                console.log('unhandled, ', dat)
            }
        }
        return cb;
    }
    join(name) {
        let obj = {join: name}
        this.name = name;
        this.sock.send(JSON.stringify(obj));
    }
    skip() {
        let obj = {skip: 1, user: this.name};
        this.sock.send(JSON.stringify(obj));
    }
    ready() {
        let righto = document.getElementById('correct');
        righto.hidden = true;
        let obj = {ready: 1, user: this.name};
        this.sock.send(JSON.stringify(obj));
    }
    guess(word) {
        let obj = {guess: word, user: this.name};
        this.sock.send(JSON.stringify(obj));
    }
    clear() {
        // DO NOT USE
        let obj = {clear: 1, user: this.name};
        this.sock.send(JSON.stringify(obj));
    }
}


function loadit() {
    // loads everything, sets stuff up etc
    gm = new GameManager()
    let nform = document.getElementById('namer');
    let nbox = document.getElementById('name');
    let rbox = document.getElementById('ready');
    let sbox = document.getElementById('skip');
    let gform = document.getElementById('guessr')
    let gbox = document.getElementById('guess');
    let gs = document.getElementById('guesses');
    nform.onsubmit = e => {
        e.preventDefault();
        let name = nbox.value;
        gm.join(name);
    }
    gform.onsubmit = e => {
        e.preventDefault();
        let name = gbox.value;
        gbox.value = ""
        gm.guess(name);
    }
    rbox.onclick = e => {
        gm.ready();
        thisViewModel.waitingForUserConfirm(false);
    }
    sbox.onclick = e => {
        gm.skip();
    }
}


