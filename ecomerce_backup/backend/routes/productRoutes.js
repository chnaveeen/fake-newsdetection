const express = require("express");
const router = express.Router();
const Product = require("../models/Product");


// GET all products
router.get("/products", async (req, res) => {

  try {
    const products = await Product.find();
    res.json(products);
  } catch (error) {
    res.status(500).json({message: error.message});
  }

});


// ADD product
router.post("/products", async (req, res) => {

  try {

    const product = new Product({
      name: req.body.name,
      price: req.body.price,
      description: req.body.description,
      image: req.body.image
    });

    const savedProduct = await product.save();

    res.json(savedProduct);

  } catch (error) {

    res.status(500).json({message: error.message});

  }

});

module.exports = router;