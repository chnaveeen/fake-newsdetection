const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

const productRoutes = require("./routes/productRoutes");
const userRoutes = require("./routes/userRoutes");

app.use("/api", productRoutes);
app.use("/api", userRoutes);

/* MongoDB Connection */
console.log("Attempting to connect to MongoDB...");
mongoose.connect("mongodb://localhost:27017/projectDB")
.then(() => {
    console.log("✅ MongoDB Connected Successfully");
})
.catch((err) => {
    console.log("❌ Connection Error:", err);
});

// Health check endpoint
console.log("Registering /health route");
app.get("/health", (req, res) => {
    console.log("Health endpoint called at", new Date().toISOString());
    res.status(200).json({
        status: "OK",
        timestamp: new Date().toISOString(),
        mongodb: mongoose.connection.readyState === 1 ? "Connected" : "Disconnected"
    });
});

// Test route
app.get("/test", (req, res) => {
    console.log("Test endpoint called");
    res.send("Test route working");
});

// 404 handler - ABSOLUTELY LAST
app.use((req, res) => {
    console.log("404 handler called for:", req.path);
    res.status(404).json({ error: "Endpoint not found" });
});

// Global error handler - AFTER 404 handler
app.use((err, req, res, next) => {
    console.error("Unhandled error:", err);
    res.status(500).json({
        error: "Internal server error",
        details: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

/* Server */
app.listen(5000, () => {
    console.log("Server running on port 5000");
});