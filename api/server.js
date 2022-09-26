require('dotenv').config()
const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();

app.use(bodyParser.json());
app.use(cors());

const MIDDLEWARE_API = 'http://localhost:6000'
const mongoose = require('mongoose');
const Controller = require('./models/controller');
const MONGO_URL = `mongodb+srv://admin:${process.env.MONGO_PASSWORD}@cluster0.vmekeyd.mongodb.net/?retryWrites=true&w=majority`

mongoose.connect(MONGO_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.info('INFO: API is connected to database');
})
    .catch((err) => {
        console.error(`ERROR: ${err}`);
    })


app.get('/', async (req, res) => {
    // console.log(req.body);
    const controllers = await Controller.find().sort({ updatedAt: -1 });
    const controller_ids = controllers.map((ctrl) => ctrl._id);

    axios.post(`${MIDDLEWARE_API}/mqtt/load`, { data: controller_ids}, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return res.status(200).send(controllers);
});
// app.get('/', async (req, res) => {
//     // console.log(req.body);
//     const ctrl = {
//         _id: req.body._id,
//         brightness: req.body.brightness,
//         last_motion_detected: req.body.last_motion_detected
//     };

//     Controller.findOneAndUpdate({ _id: req.body._id }, ctrl, { upsert: true }, (err, doc) => {
//         console.log('error', err)
//         console.log('doc', doc)
//     })

//     res.sendStatus(201);
// });

app.post('/ctrl/create', async (req, res) => {
    const ctrl = new Controller({
        brightness: 100,
        last_motion_detected: Math.floor(Date.now() / 1000) // get unix timestamp
    });
    await ctrl.save();

    console.log('posted to middleware API to create controller', ctrl);
    axios.post(`${MIDDLEWARE_API}/mqtt/create`, { id: ctrl._id }, {
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return res.status(201).send(ctrl);
});

app.post('/ctrl/update', async (req, res) => {
    const ctrl = await Controller.findById(req.body.id);
    if (ctrl) {
        console.log('posted to middleware API to update controller', ctrl);
        axios.post(`${MIDDLEWARE_API}/mqtt/update`, { id: ctrl._id }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        return res.status(201).send(ctrl);
    }
    res.sendStatus(404);
})

app.post('/ctrl/updated', async (req, res) => {
    const ctrl = {
        _id: req.body.id,
        brightness: req.body.brightness,
        last_motion_detected: req.body.last_motion_detected
    };

    Controller.findOneAndUpdate({ _id: req.body.id }, ctrl, { upsert: true }, (err, doc) => {
        console.log('error', err)
        console.log('doc', doc)
    });

    res.sendStatus(201);
});



app.listen(5000, () => {
    console.log('Main server listening on port 5000!')
});