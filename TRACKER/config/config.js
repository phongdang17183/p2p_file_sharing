const mongoose = require("mongoose")

const connectDB = async ()=>{
    try {
        await mongoose.connect("mongodb+srv://tranchinhbach:tranchinhbach@co3001.qkb5z.mongodb.net/?retryWrites=true&w=majority&appName=CO3001/tracker")
        console.log("MongoDB connected");
    } catch (error) {
        console.log("db connect err: ", error)
    }
}

module.exports = connectDB;