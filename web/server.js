const express = require('express');
const cors = require('cors');
const fileUpload = require('express-fileupload');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const uuid = require('uuid');
const fs = require('fs');
const http = require('http');
require('dotenv').config();
const app = express();
const superagent = require('superagent');

const SESSION_SECRET = uuid.v4();

app.use(express.static('public'));
app.use(cors({
    origin: true,
    credentials: true
}));
app.use(fileUpload());
app.use(cookieParser(SESSION_SECRET));
app.use(session({
    secret: SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 60*60*1000 }
}));

const getFolderPath = req => `${__dirname}/public/session_${req.sessionID}`;

app.get('/chart/:chartId', (req, res) => {
    const { chartId } = req.params;
    if (chartId) {
        const filePath = `${getFolderPath(req)}/data/${chartId}.html`;
        if (fs.existsSync(filePath)) {
            return res.sendFile(filePath);
        }
    }
    return res.sendFile(`${__dirname}/public/404.html`);
});

app.post('/upload', (req, res) => {

    console.log('dir path:',`${__dirname}`)

    if (!req.files) {
        return res.status(404).send({ error: ".CSV File not found in the request body" });
    }

    const file = req.files.file;
    const columns = JSON.parse(req.body.data);

    if (columns && file) {
        const chartId = uuid.v4();
        const sessionPath = getFolderPath(req);
        const dataPath = `${sessionPath}/data`;
        const folderPath = `/opt/web/public/session_${req.sessionID}/data`
        const fileName = `${chartId}.csv`

        if (!fs.existsSync(sessionPath)) {
            fs.mkdirSync(sessionPath);
        }

        if (!fs.existsSync(dataPath)) {
            fs.mkdirSync(dataPath);
        }

        fs.writeFile(`${dataPath}/${chartId}.csv`, file.data, (err) => {
            if (err) {
                return res.status(500).send({ error: 'Error writing CSV file to disk' });
            }

            const data = { folderPath, fileName, columns, chartId };

            console.log('data ', data);

            superagent
                .post('http://0.0.0.0:8080/api/process')
                .send(data)
                .set('accept', 'application/json')
                .set('Content-Type', 'application/json')
                .end((err, result) => {
                    if (err) {
                        console.log('Server Error',err);
                        return res.status(500).send({ err, error: 'Error processing CSV file' });
                    }
                    return res.status(200).send({ id: chartId, path: `/chart/${chartId}` });
                });
        });

        return;
    }

    return res.status(404).send({ error: 'Column data not found in the request body' });
});


app.listen(4500, () => {
    console.log('server is running at port 4500');
})