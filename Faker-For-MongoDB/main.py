from faker import Faker
from pymongo import MongoClient
from bson import ObjectId
import random

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']

# Create a Faker object
fake = Faker()

# Function to generate fake users
def generate_fake_users(num_users):
    users = []
    for _ in range(num_users):
        user = {
            "_id": ObjectId(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "isAdmin": random.choice([True, False])
        }
        users.append(user)
    return users

# Function to generate fake products
def generate_fake_products(num_products, num_brands):
    products = []
    for _ in range(num_products):
        product = {
            "_id": ObjectId(),
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "price": random.uniform(10.0, 1000.0),
            "brand": random.choice(range(1, num_brands + 1)),
            "category": fake.word(),
            "imageUrl": fake.image_url()
        }
        products.append(product)
        # Function to generate fake brands
def generate_fake_brands(num_brands):
    brands = []
    for i in range(num_brands):
        brand = {
            "_id": i + 1,
            "name": fake.company(),
            "description": fake.text(max_nb_chars=100),
            "logoUrl": fake.image_url(),
            "website": fake.url()
        }
        brands.append(brand)
    return brands

# Function to generate fake payments
def generate_fake_payments(num_payments, users):
    payments = []
    for _ in range(num_payments):
        payment = {
            "_id": ObjectId(),
            "user_id": random.choice(users)["_id"],
            "amount": random.uniform(10.0, 1000.0),
            "paymentDate": fake.date_time_this_year(),
            "paymentMethod": random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
            # Additional payment details
        }
        payments.append(payment)
    return payments

# Function to generate fake activities
def generate_fake_activities(num_activities, users, products):
    activities = []
    activity_types = ["view_product", "click", "purchase", "add_to_cart", "search"]

    for _ in range(num_activities):
        activity = {
            "_id": ObjectId(),
            "user_id": str(random.choice(users)["_id"]),
            "activityType": random.choice(activity_types),
            "productId": str(random.choice(products)["_id"]),
            "timestamp": fake.date_time_this_year(),
            # Additional details about the activity
        }
        activities.append(activity)
    return activities

if __name__ == "__main__":
    # Number of fake users, products, brands, payments, and activities to generate
    num_fake_users = 5234
    num_fake_products = 1034
    num_fake_brands = 345
    num_fake_payments = 12543
    num_fake_activities = 1234343

    # Create collections if they do not exist
    db.create_collection('users')
    db.create_collection('products')
    db.create_collection('brands')
    db.create_collection('payments')
    db.create_collection('activities')

    # Generate fake data
    fake_users = generate_fake_users(num_fake_users)
    fake_products = generate_fake_products(num_fake_products, num_fake_brands)
    fake_brands = generate_fake_brands(num_fake_brands)
    fake_payments = generate_fake_payments(num_fake_payments, fake_users)
    fake_activities = generate_fake_activities(num_fake_activities, fake_users, fake_products)

    # Insert data into MongoDB collections
    user_collection = db['users']
    user_collection.insert_many(fake_users)
    product_collection = db['products']
    product_collection.insert_many(fake_products)

    brand_collection = db['brands']
    brand_collection.insert_many(fake_brands)

    payment_collection = db['payments']
    payment_collection.insert_many(fake_payments)

    activity_collection = db['activities']
    activity_collection.insert_many(fake_activities)

    print("Fake data has been generated and inserted into the MongoDB collections.")