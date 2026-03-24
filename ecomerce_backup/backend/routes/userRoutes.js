const express = require("express");
const router = express.Router();
const User = require("../models/User");

/* API */
router.post("/addUser", async (req, res) => {
    try {
        // Input validation
        if (!req.body.name || !req.body.email) {
            return res.status(400).json({ error: "Name and email are required" });
        }

        // Check if user already exists
        const existingUser = await User.findOne({ email: req.body.email });
        if (existingUser) {
            return res.status(409).json({ error: "User with this email already exists" });
        }

        const user = new User({
            name: req.body.name,
            email: req.body.email
        });

        await user.save();
        res.status(201).json({
            message: "User Added Successfully",
            user: {
                id: user._id,
                name: user.name,
                email: user.email
            }
        });
    } catch (error) {
        console.error("Error adding user:", error);
        res.status(500).json({
            error: "Failed to add user",
            details: process.env.NODE_ENV === 'development' ? error.message : 'Internal server error'
        });
    }
});

router.get("/users", async (req, res) => {
    try {
        const data = await User.find();
        res.status(200).json({
            users: data,
            count: data.length,
            success: true
        });
    } catch (error) {
        console.error("Error fetching users:", error);
        res.status(500).json({
            error: "Failed to fetch users",
            details: process.env.NODE_ENV === 'development' ? error.message : 'Internal server error'
        });
    }
});

module.exports = router;