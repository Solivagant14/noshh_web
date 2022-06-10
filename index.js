const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
const path = require('path')
var fs = require('fs');
var exec = require('child_process').exec;

app.use(express.static(path.join(__dirname, 'web/public')));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/web/index.html');
});

app.get('/progress', (req, res) => {
    exec("env/bin/python noshh.py " + req.query.link, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });

    res.sendFile(__dirname + '/web/progress.html');

    var previous = null;
    var current = null;
    var dataFile = null;
    var process = null

    io.on('connection', (socket) => {
        operation = () => {
            try {
                dataFile = JSON.parse(fs.readFileSync('./progress/progress.json'));
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

app.get("/video", function(req, res) {
    res.sendFile(__dirname + "/web/video.html");
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
    const videoPath = "noshh_vids/video.webm";
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