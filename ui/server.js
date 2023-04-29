const fs = require('fs');
const pythonShell = require('python-shell')
const path = require('path')
const fullPath = path.join(__dirname, '../data')
const express = require('express');
const app = express();
const port = 3000 // Change this to whatever port number you prefer

app.use(express.static(path.join(__dirname, '/public'))); // Serve up the public folder as static files

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html'); // Send the index.html file when someone visits '/'
});

app.get('/datasets', (req, res) => {
    fs.readdir(fullPath, (error, files) => {
        if (error) console.log(error)
        // fileNames = files.toString()
        console.log('Filenames: ' + files);
        // files.forEach(file => {
        //     console.log(file)

        // })
        res.send(files.toString())
    })
});

app.get('/results/:file', (req, res) => {
    let fileName = req.params['file']
    let options = {args: [fileName]}
    console.log('Running');
    pythonShell.PythonShell.run(__dirname + '/../code/modified_apriori.py', options).then(messages => {
        console.log(messages);
        // let result = JSON.parse(messages[0])
        res.send(messages[0])
    })
    pythonShell.PythonShell.run(__dirname + '/../code/compare_results.py', options).then(messages => {
        console.log(messages);
        // let result = JSON.parse(messages[0])
        res.send(messages[0])
    })
});

app.listen(port, () => {
    console.log(`Server listening on port ${ port }`);
});
