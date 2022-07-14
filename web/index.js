const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
const path = require('path')
var fs = require('fs');

app.set('view engine', 'ejs');

function uid(link){
    return link.slice(-11)
}

app.use(express.static(path.join(__dirname, 'pages/public')));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/pages/index.html');
});

app.get('/progress', (req, res) => {
    async function doAsyncTask() {
        const url = (
          'http://127.0.0.1:5000/?' +
          new URLSearchParams({ 'url' :  req.query.link}).toString()
        );
      
        const result = await fetch(url)
          .then(response => response.json());
      
        console.log('Fetched from: ' + url);
        console.log(result);
      }
      
      doAsyncTask();

    video = uid(req.query.link)

    res.render('progress', {video:video});

    var previous = null;
    var current = null;
    var dataFile = null;
    var process = null

    io.on('connection', (socket) => {
        operation = () => {
            try {
                dataFile = JSON.parse(fs.readFileSync(`./progress/${video}_progress.json`));
                current = JSON.stringify(dataFile);
            } catch (err) {}

            if (previous && current && previous !== current) {
                process = dataFile["process"]
                if (process == 'Done') {
                    clearInterval(operation_instance)
                    io.emit('progress', { process: process, percentage: "100" });
                }
                if (process && process !== 'Done') {
                    io.emit('progress', { process: process, percentage: dataFile[process] });
                }
            }
            previous = current;
        }
        operation_instance = setInterval(operation, 100);
    });
});

app.get("/watch", function(req, res) {
    res.render('video', {video:req.query.v});
});

app.get("/videostream", function(req, res) {
    // Ensure there is a range given for the video
    const range = req.headers.range;
    console.log(req)
    if (!range) {
        res.status(400).send("Requires Range header");
        console.log("Requires Range header")
    }

    // get video stats (about 61MB)
    const videoPath = `noshh_vids/${req.query.v}.webm`;
    const videoSize = fs.statSync(videoPath).size;

    // Parse Range
    // Example: "bytes=32324-"
    const CHUNK_SIZE = 10 ** 6; // 1MB
    const start = Number(range.replace(/\D/g, ""));
    const end = Math.min(start + CHUNK_SIZE, videoSize - 1);

    // Create headers
    const contentLength = end - start + 1;
    const headers = {
        "Content-Range": `bytes ${start}-${end}/${videoSize}`,
        "Accept-Ranges": "bytes",
        "Content-Length": contentLength,
        "Content-Type": "video/mp4",
    };

    // HTTP Status 206 for Partial Content
    res.writeHead(206, headers);

    // create video read stream for this particular chunk
    const videoStream = fs.createReadStream(videoPath, { start, end });

    // Stream the video chunk to the client
    videoStream.pipe(res);
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});