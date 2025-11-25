# 📦 Storify – Smart E-Commerce Platform  
A smart, secure, and scalable e-commerce web application connecting **Customers**, **Sellers**, and **Admins** in one integrated platform.

---

## 📘 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [User Roles](#user-roles)
- [Tech Stack](#tech-stack)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Use Cases](#use-cases)
- [Database Entities](#database-entities)
- [Team Members](#team-members)

---

## 📝 Overview
Storify is a smart e-commerce system designed to streamline the online shopping experience while providing sellers with efficient product management tools and admins with complete platform oversight.

The platform includes:
- Product browsing, filtering, and purchasing for customers.
- Full product and order management for sellers.
- User and system monitoring for administrators.

---

## ✨ Features

### 👤 **Customer**
- Register/Login securely  
- Browse and filter products  
- Add to cart & checkout  
- Secure online payment  
- Track orders  
- Rate and review purchased products  
- Contact customer support  

### 🛍️ **Seller**
- Create/verify store profile  
- Add, edit, delete products  
- Manage stock  
- View customer orders  
- Receive system alerts (low stock, feedback)  
- Reply to customer queries  

### 🛠️ **Admin**
- Manage customer & seller accounts  
- Approve products and stores  
- Monitor system activity  
- View reports & handle complaints  
- Manage notifications  

---

## 🧱 System Architecture
Storify follows a modular architecture consisting of:

- **Authentication Module** – registration, login, verification  
- **Product Management Module**  
- **Order & Payment Module**  
- **Notification Module**  
- **Checker Module (Automated Stock Monitor)**  
- **Admin Module**  
- **Customer Support Module**

---

## 👥 User Roles
| Role | Description |
|------|-------------|
| **Customer** | Browses and buys products |
| **Seller** | Manages store products & orders |
| **Admin** | Controls system operations and verifies users/products |

---

## 🧰 Tech Stack
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python (Flask)  
**Database:** MySQL  
**External Services:** Payment Gateway (PayPal/Stripe)  
**Protocols:** HTTPS, SMTP (Notifications)

---

## ✅ Functional Requirements

### **Customers**
- Secure login/logout  
- Search/filter products  
- Add to cart & checkout  
- Online payments  
- View order history  
- Review products  

### **Sellers**
- Manage store profile  
- Add/update/remove products  
- Manage orders  
- Receive notifications  

### **Admin**
- Approve products and sellers  
- Manage all system users  
- Handle reports and complaints  

### **System**
- Automatic notifications  
- Stock monitoring checker  
- Secure data transactions  

---

## 🔐 Non-Functional Requirements
- **Performance**: Supports 200 concurrent users  
- **Security**: Encrypted passwords, HTTPS  
- **Usability**: Simple & responsive UI  
- **Reliability**: 99% uptime, daily backups  
- **Scalability**: Handles growth in users/products  
- **Maintainability**: Modular code structure  

---

## 🧩 Use Cases
### 📌 Main Actors:
- Customer  
- Seller  
- Admin  

### Includes:
- Login/Authentication  
- Product Management  
- Order & Payment Workflow  
- Notification Handling  

---

## 🗂️ Database Entities
| Table | Attributes |
|-------|------------|
| **User** | UserID, Name, Email, Password, Role |
| **Product** | ProductID, Name, Description, Price, Stock, SellerID |
| **Order** | OrderID, CustomerID, TotalAmount, PaymentID, Date |
| **Payment** | PaymentID, Method, Status, Amount |
| **Notification** | NotificationID, UserID, Message, Date |

---

## 👥 Team Members (Team #28)
- **Ahmed Tamer** — ID: 202401457  
- **Omar Ahmed** — ID: 202400354  
- **Samaa Khaled** — ID: 202401280  

---

## 📄 License
This project is part of **CSAI203 – Introduction to Software Engineering** coursework.

---

## 📧 Contact
For any inquiries regarding the Storify project, please contact:
Omar Elgazar – omarelgazar715@gmail.com
