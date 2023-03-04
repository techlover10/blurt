
// not really rain...

var sock = null;



function load() {
		sock = new WebSocket('ws://localhost:8765');
		sock.addEventListener('message', e=>console.log("recvd: ", e.data));
}
