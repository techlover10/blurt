

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
                document.getElementById('skip').hidden = false;
                document.getElementById('ready').hidden = true;
                document.getElementById('ans').hidden = true;
                document.getElementById('guessr').hidden = false;
                document.getElementById('guesses').hidden = false;
                document.getElementById('guesses').replaceChildren();
                console.log('clue handling part, ', dat);
                // note that ping is supposed to happen here too...
                let o = {'pong': 1, user: self.name};
                self.sock.send(JSON.stringify(o));
                let elt = document.getElementById('clue');
                elt.innerHTML  = '<div class="point-value">Points: '+ dat['value'] + '</div>' + '<div class="clue-text">' + dat['clue'] + '</div>';
            }
            else if(t == 'end') {
                document.getElementById('skip').hidden = true;
                document.getElementById('ready').hidden = false;
                document.getElementById('guessr').hidden = true;
                let ans = dat['answer'];
                document.getElementById('ans').innerHTML = '<div class="answer-banner">Answer:</div><div class="answer-text">' + ans + '</div>';
                document.getElementById('ans').hidden = false;
                //document.getElementById('guesses').hidden = true;
                console.log('end of round, ', dat);
                let sc = dat['scores'];
                let elt = document.getElementById('scores');
                elt.replaceChildren();
                for(let s of sc) {
                    let d = document.createElement('div');
                    d.classList.add("score-entry");
                    d.innerHTML = '<div class="username">' + s['name'] + '</div><div class="user-score">' + s['score'] + '</div>';
                    elt.appendChild(d);
                }
            }
            else if(t == 'reg') {
                console.log('hihi')
                // hide/show relevant divs
                document.getElementById('nd').hidden = true;
                document.getElementById('pp').hidden = false;
                document.getElementById('clue').hidden = false;
                document.getElementById('scores').hidden = false;
                document.getElementById('guesses').hidden = false;
            }
						else if(t == 'right') {
								document.getElementById('correct').hidden = false;
						}
            else if(t == 'scores') {
                //console.log(dat)
                let sc = dat['scores'];
                let elt = document.getElementById('scores');
                elt.replaceChildren();
                for(let s of sc) {
                    let d = document.createElement('div');
                    d.classList.add("score-entry");
                    d.innerHTML = '<div class="username">' + s['name'] + '</div><div class="user-score">' + s['score'] + '</div>';
                    elt.appendChild(d);
                }
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
                let gs = document.getElementById('guesses');
                let d = document.createElement('div');
                d.innerHTML = '<div class="guess-entry"><div class="guesser">' + dat['name'] + ' guessed...</div><div class="guess">' + dat['guess'] + '</div></div>';
                gs.appendChild(d);
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
        let gs = document.getElementById('guesses');
				let righto = document.getElementById('correct');
				righto.hidden = true;
        gs.replaceChildren();
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
    }
    sbox.onclick = e => {
        gm.skip();
    }
}


window.onload = loadit;
