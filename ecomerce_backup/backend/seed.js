const mongoose = require("mongoose");
const Product = require("./models/Product");

mongoose.connect("mongodb://localhost:27017/projectDB")
    .then(async () => {
        console.log("Connected to MongoDB");

        // Check if products exist
        const count = await Product.countDocuments();
        if (count === 0) {
            console.log("No products found, seeding database...");
            const products = [
                {
                    name: "Premium Wireless Headphones",
                    price: 249.99,
                    description: "High-fidelity audio with active noise cancellation and 30-hour battery life. Experience sound like never before.",
                    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
                },
                {
                    name: "Smart Watch Elite",
                    price: 199.50,
                    description: "Advanced health monitoring, GPS tracking, and a stunning OLED display wrapped in an aerospace-grade aluminum body.",
                    image: "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&q=80"
                },
                {
                    name: "Mechanical Keyboard Pro",
                    price: 129.00,
                    description: "Tactile switches, customizable RGB backlighting, and a premium aluminum frame for the ultimate typing experience.",
                    image: "https://images.unsplash.com/photo-1595225476474-87563907a212?w=500&q=80"
                },
                {
                    name: "Minimalist Desk Lamp",
                    price: 89.99,
                    description: "Adjustable color temperature, wireless charging base, and sleek modern design to elevate any workspace.",
                    image: "https://images.unsplash.com/photo-1517705008128-361805f42e86?w=500&q=80"
                },
                {
                    name: "Smart Watch",
                    price: 335,
                    description: "minimalist smartwatch product photo, clean white background, sleek modern smartwatch with fitness display, soft shadows, studio lighting, ultra realistic, 8k product photography",
                    image: "c:\Users\chnav\Downloads\smartwatch.jpg"
                }
            ];

            await Product.insertMany(products);
            console.log("Seeded products successfully");
        } else {
            console.log(`Found ${count} products, skipping seed.`);
        }

        process.exit(0);
    })
    .catch(err => {
        console.error("Error:", err);
        process.exit(1);
    });
