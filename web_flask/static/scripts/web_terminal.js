const term = new Terminal({
    cursorBlink: true,
    macOptionIsMeta: true,
});

// Load fit Addon
const fit = new FitAddon.FitAddon();
term.loadAddon(fit);
term.loadAddon(new WebLinksAddon.WebLinksAddon());
term.loadAddon(new SearchAddon.SearchAddon());

// Open the terminal in #terminal-container
term.open(document.getElementById("terminal"));
fit.fit();
term.resize(15, 45);
// console.log(`size: ${term.cols} columns, ${term.rows} rows`);
fit.fit();

term.writeln("Welcome to hbnb web CLI!");
term.writeln("https://github.com/iChigozirim/holbertonbnb");
term.onData((data) => {
  // console.log("key pressed in browser:", data);
  socket.emit("console-input", { input: data });
});

// const socket = io.connect("wss://www.miniairbnb.gq/socket.io");
// const socket = io.connect("wss://miniairbnb.gq/socket.io", {transports: ["websocket"]});
// {transports: ["websocket"], rejectUnauthorized: false }
const socket = io.connect("wss://www.miniairbnb.gq:5005", {transports: ["websocket"]});
const status = document.getElementById("status");

socket.on("console-output", function (data) {
  // new output received from server
  // console.log("new output received from server:", data.output);
  term.write(data.output);
});

socket.on("connect", () => {
  fitToscreen();
  status.innerHTML =
    '<span style="background-color: lightgreen;">connected</span>';
});

socket.on("end", () => {
  socket.disconnect()
})

socket.on("disconnect", (reason) => {
  console.log("DISCONNECTING CLIENT SIDE: " + reason)
  status.innerHTML =
    '<span style="background-color: #ff8383;">disconnected</span>';
});

function fitToscreen() {
  fit.fit();
  const dims = { cols: term.cols, rows: term.rows };
  // console.log("sending new dimensions to server's console", dims);
  socket.emit("resize", dims);
}

function debounce(func, wait_ms) {
  let timeout;
  return function (...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait_ms);
  };
}

// Fit the terminal to screen when the window or it's div is resized
const wait_ms = 50;
window.onresize = debounce(fitToscreen, wait_ms);

const terminal = document.querySelector('.terminal-content')

const obs = new ResizeObserver(entries => {
  debounce(fitToscreen(), wait_ms);
})

obs.observe(terminal)
