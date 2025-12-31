# 📃 Models

### 1️⃣ Category & Product
- 1 category can have Multiple Product
- 1 Product can have 1 Category
- **Category & Product == 1 to Many**

----------------------------

### 2️⃣ Rating & Product
- 1 Product can have Multiple Rating
- Each Rating is for only 1 Product
- **Product & Rating  == 1 to Many**

----------------------------

### 3️⃣ Rating & User
- 1 User can create many Ratings
- Each Rating belongs to only 1 User
- **User & Rating  == 1 to Many** 

------------------------------------

### 4️⃣ Cart & User
- 1 User can create 1 Cart
- Each Cart belongs to only 1 User
- **User & Cart  == 1 to 1** 


------------------------------------


### 5️⃣ Cart & Cart Item
- 1 Cart can have multiple Cart Item
- Each Cart Item must belongs to only 1 Cart
- **Cart & Cart Item  == 1 to Many**


-----------------------------


### 6️⃣ Cart Item & Product
- 1 Cart Item can have multiple Product
- Each Product Item must belongs to only 1 Cart Item
- **Cart Item & Product  == 1 to Many**


-----------------------------


### 7️⃣ Order & User
- 1 User can have multiple Order
- Each Order Item must belongs to 1 user
- **User & Order  == 1 to Many**


-----------------------------


### 8️⃣ Order & Oder Item
- 1 Order can have multiple Order Items
- Each Order Item must belongs to 1 Order
- **Order & Oder Item  == 1 to Many**


