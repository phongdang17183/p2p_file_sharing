const mongoose = require("mongoose");

const ListPeerSchema = new mongoose.Schema({
    magnetText: { type: String, required: true },
    list_peer:[{
        peerIp: {type: String, required: true},
        peerPort: {type: Number, required: true}
    }]
});


module.exports = mongoose.model("listpeer", ListPeerSchema);
