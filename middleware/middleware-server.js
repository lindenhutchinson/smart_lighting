const express = require('express');
const axios = require('axios');
const mqtt = require('mqtt');

const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());

const MAIN_SERVER_URL = 'http://localhost:5000';

const options = {
    host: 'broker.emqx.io',
    port: 1883,
    username: 'emqx',
    password: 'public'
}

// initialize the MQTT client
const client = mqtt.connect(options);


client.subscribe('/lighting/driver/controllerUpdated');
client.on('message', async (topic, payload) => {
    console.log(topic)
    console.log(payload.toString());
    axios.post(`${MAIN_SERVER_URL}/ctrl/updated`, payload.toString(), {
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((res) => {
            console.log('RESPONSE', res.status);
        }).catch((err) => {
            console.log('ERROR', err);
        });
})


app.post('/mqtt/create', (req, res) => {
    const json_string = JSON.stringify({
        id: req.body.id,
    })
    console.log('create controller', json_string)
    client.publish('/lighting/driver/createController', json_string)
    res.sendStatus(201);
});

app.post('/mqtt/update', (req, res) => {
    const json_string = JSON.stringify({
        id: req.body.id,
    })
    console.log('toggle on controller', json_string)
    client.publish('/lighting/driver/updateController', json_string)
    res.sendStatus(201);

})

app.post('/mqtt/load', (req, res) => {
    const json_string = JSON.stringify(req.body.data);
    console.log('load controllers', json_string)
    client.publish('/lighting/driver/loadControllers', json_string)
    res.sendStatus(200);
})

app.listen(6000, () => {
    console.log('Middleware server listening on port 6000!')
});