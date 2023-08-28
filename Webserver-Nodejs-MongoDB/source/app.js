// app.js
const express = require('express');
const session = require('express-session');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const port = 3001;

// MongoDB connection
mongoose.connect('mongodb://database-mongodb:27017/ecom_eric', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Set up EJS as the view engine
app.set('view engine', 'ejs');

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
    secret: 'your-secret-key', // Replace 'your-secret-key' with your own secret key
    resave: false,
    saveUninitialized: true
}));

// Define MongoDB schema and models
const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  isAdmin: Boolean,
});

const productSchema = new mongoose.Schema({
    name: String,
    brand: String,
    price: Number,
    imageUrl: String, // Add imageUrl field for storing the image URL
  });
  
const cartSchema = new mongoose.Schema({
    user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }, // Reference to the User model
    products: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product' }], // Reference to the Product model
});

const User = mongoose.model('User', userSchema);
const Product = mongoose.model('Product', productSchema);
const Cart = mongoose.model('Cart', cartSchema);

// Routes

app.get('/create-user', (req, res) => {
    res.render('create-user');
  });

// Route 1: Create User
app.post('/create-user', async (req, res) => {
  // You should implement proper validation and security measures here
  try {
    const { username, password, isAdmin } = req.body;
    const adminUser = isAdmin === 'on' ? true : false;
    const existingUser = await User.findOne({ username });

    if (existingUser) {
      // If the user already exists, redirect to the login page with a message
      res.redirect('/login?message=User already exists. Please login.');
      return;
    }

    await User.create({ username, password, isAdmin :adminUser});
    res.redirect('/login?message=User created successfully!');
  } catch (error) {
    console.log(error)
    res.status(500).send('An error occurred while creating the user.');
  }
});

// Route 2: Login Page (assuming you have a login form in your EJS template)
app.get('/login', (req, res) => {
    const message = req.query.message;
    res.render('login', { message });
});

app.post('/login', async (req, res) => {
    // You should implement proper validation and security measures here
    try {
      const { username, password } = req.body;
  
      // Assuming you have the User model defined earlier
      const user = await User.findOne({ username, password });
  
      if (user) {
        // Successful login
        // For a real-world scenario, you would use sessions or JWT for authentication
        req.session.isLoggedIn = true;
        req.session.username = username; 
        res.redirect('/products');
        return;
      } else {
        // Invalid credentials
        res.redirect('/login?message=Invalid User name or password!');
      }
    } catch (error) {
      res.status(500).send('An error occurred while logging in.');
    }
  });

// Middleware to check if the user is logged in
const checkLogin = (req, res, next) => {
    if (req.session.isLoggedIn) {
        // If the user is logged in, allow them to proceed to the next middleware/route
        next();
      } else {
        // If the user is not logged in, redirect them to the login page
        res.redirect('/login?message=Please login to access the products page.');
      }
};

const checkAdmin = async (req, res, next) => {
    try {
      // For a real-world scenario, you would use sessions or JWT for authentication
      // Here, we'll assume the username is stored in the session when the user logs in
      const username = req.session.username;
  
      // Assuming you have the User model defined earlier
      const user = await User.findOne({ username });
  
      if (user && user.isAdmin) {
        // If the user is an admin, allow them to proceed to the next middleware/route
        next();
      } else {
        // If the user is not an admin, redirect them to the products page or show an error page
        res.redirect('/products'); // Redirect to the products page or '/error' or other suitable route
      }
    } catch (error) {
      res.status(500).send('An error occurred while checking admin privileges.');
    }
  };

// Routes accessible after login

// Route 3: View all products with pagination
app.get('/products', checkLogin, async (req, res) => {
  // Implement pagination logic here
  const products = await Product.find({});
  res.render('products', { products });
});

// Route 4: View one product and add to cart
app.get('/products/:id', checkLogin, async (req, res) => {
  const productId = req.params.id;
  const product = await Product.findById(productId);
  res.render('product', { product });
});

// app.js

// ... (previous code)

app.post('/add-to-cart/:productId', checkLogin, async (req, res) => {
    try {
      const productId = req.params.productId;
      const userId = req.session.username; // Assuming you have stored the user's ID in the session
  
      // Assuming you have the Cart, User, and Product models defined earlier
      // Find the cart entry for the user in the cart collection
      const user = await User.findOne({ username: userId });
      console.log(user)
      let userCart = await Cart.findOne({ user: user._id });
  
      if (!userCart) {
        // If the cart entry for the user is not found, create a new cart entry
        userCart = new Cart({ user: user._id  });
      }
  
      // Find the product by its ID
      const product = await Product.findById(productId);
  
      // Add the product to the cart
      userCart.products.push(product._id);
      await userCart.save();
  
      // Redirect back to the 'my-products' page after adding the product to the cart
      res.redirect('/my-products');
    } catch (error) {
    console.log(error)
      res.status(500).send('An error occurred while adding the product to the cart.');
    }
  });
  
  
  // ... (previous code)
  

// app.js

// ... (previous code)

// Route to view the user's cart (GET request)
app.get('/view-cart', checkLogin, async (req, res) => {
    try {
      const userId = req.session.username; // Assuming you have stored the user's ID in the session
      const user = await User.findOne({ username: userId });
      // Assuming you have the Cart, User, and Product models defined earlier
      // Find the user's cart by their ID and populate the 'products' field with product details
      const userCart = await Cart.findOne({ user: user }).populate('products');
  
      res.render('view-cart', { cart: userCart });
    } catch (error) {
      res.status(500).send('An error occurred while fetching the cart items.');
    }
  });
  
  // ... (previous code)
  
  

app.get('/my-products', checkLogin,checkAdmin, async (req, res) => {
    try {
      // For a real-world scenario, you would use sessions or JWT for authentication
      // Here, we'll assume the username is stored in the session when the user logs in
      const username = req.session.username;
  
      // Assuming 'seller' is the field in the Product model that stores the seller's username
      const products = await Product.find({ brand: username });
  
      res.render('my-products', { products });
    } catch (error) {
      res.status(500).send('An error occurred while fetching the products.');
    }
  });

app.get('/add-product', checkLogin, checkAdmin, (req, res) => {
    // Render the add product page here
    res.render('add-product'); // Replace 'add-product' with the actual EJS template for adding a product
  });



// Route to delete a product (POST request)
app.post('/delete-product/:productId', async (req, res) => {
    try {
      const productId = req.params.productId;
  
      // Assuming you have the Product model defined earlier
      // Find the product by its _id and delete it from the database
      await Product.findByIdAndDelete(productId);
  
      // Redirect back to the 'my-products' page after successful deletion
      res.redirect('/my-products');
    } catch (error) {
      res.status(500).send('An error occurred while deleting the product.');
    }
  });
  

  
// Route 6: Admin user can add products under their brand
app.post('/add-product', checkLogin,checkAdmin, async (req, res) => {
  // Implement proper validation and security measures here
  try {
    const { name, price, imageUrl } = req.body; // Include imageUrl here
    const brand = req.session.username; 
    await Product.create({ name, brand, price, imageUrl });
    res.send('Product added successfully!');
  } catch (error) {
    res.status(500).send('An error occurred while adding the product.');
  }
});

app.get('/logout', (req, res) => {
    // Destroy the session to log the user out
    req.session.destroy((err) => {
      if (err) {
        console.error('Error destroying session:', err);
      }
  
      // Redirect to the login page after logging out
      res.redirect('/login?message=You have been logged out.');
    });
  });

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
