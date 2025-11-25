📦 Storify – Smart E-Commerce Platform

A smart, secure, and scalable e-commerce web application connecting Customers, Sellers, and Admins in one integrated platform.

📘 Table of Contents

Overview

Features

System Architecture

User Roles

Tech Stack

Functional Requirements

Non-Functional Requirements

Use Cases

Database Entities

Team Members

License

Contact

📝 Overview

Storify is a smart e-commerce platform designed to streamline online shopping for customers, provide efficient product management tools for sellers, and offer comprehensive monitoring and control for administrators.

Key capabilities include:

Product browsing, filtering, and purchasing for customers.

Full product and order management for sellers.

User and system monitoring for administrators.

✨ Features
👤 Customer

Secure registration and login

Browse and filter products

Add to cart & checkout

Secure online payment

Track orders

Rate and review purchased products

Contact customer support

🛍️ Seller

Create and verify store profile

Add, edit, and delete products

Manage stock and inventory

View customer orders

Receive system alerts (low stock, feedback)

Respond to customer queries

🛠️ Admin

Manage customer and seller accounts

Approve products and stores

Monitor system activity

View reports and handle complaints

Manage notifications

🧱 System Architecture

Storify uses a modular architecture with the following components:

Authentication Module – Handles registration, login, and verification

Product Management Module – Manages product listings and updates

Order & Payment Module – Handles order processing and payment workflows

Notification Module – Sends alerts and updates to users

Checker Module – Monitors stock and system status automatically

Admin Module – Manages platform oversight and approvals

Customer Support Module – Handles inquiries and complaints

👥 User Roles
Role	Description
Customer	Browses and purchases products
Seller	Manages store products & orders
Admin	Oversees system operations & users
🧰 Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Database: MySQL

External Services: Payment Gateway (PayPal/Stripe)

Protocols: HTTPS, SMTP for notifications

✅ Functional Requirements

Customer

Secure login/logout

Search and filter products

Add to cart & checkout

Online payments

View order history

Review products

Seller

Manage store profile

Add/update/remove products

Manage orders

Receive notifications

Admin

Approve products and sellers

Manage all system users

Handle reports and complaints

System

Automatic notifications

Stock monitoring

Secure data transactions

🔐 Non-Functional Requirements

Performance: Supports up to 200 concurrent users

Security: Encrypted passwords, HTTPS secure connections

Usability: Simple, responsive, and intuitive UI

Reliability: 99% uptime, daily backups

Scalability: Handles increasing users and products

Maintainability: Modular, organized code structure

🧩 Use Cases

Actors: Customer, Seller, Admin

Key Workflows:

Login and Authentication

Product Management

Order and Payment Workflow

Notifications and Alerts

🗂️ Database Entities
Table	Attributes
User	UserID, Name, Email, Password, Role
Product	ProductID, Name, Description, Price, Stock, SellerID
Order	OrderID, CustomerID, TotalAmount, PaymentID, Date
Payment	PaymentID, Method, Status, Amount
Notification	NotificationID, UserID, Message, Date
👥 Team Members (Team #28)

Ahmed Tamer — ID: 202401457

Omar Ahmed — ID: 202400354

Samaa Khaled — ID: 202401280

📄 License

This project is part of CSAI203 – Introduction to Software Engineering coursework.

📧 Contact

For any inquiries regarding the Storify project, please contact:
Omar Elgazar – omarelgazar715@gmail.com
