const mongoose = require('mongoose')
const uuid = require('node-uuid');

module.exports = mongoose.model('Controller', new mongoose.Schema(
    {
        _id: { type: String, default: () => uuid.v1() },
        brightness: Number,
        last_motion_detected: Number,
    },
    { timestamps: true }
))