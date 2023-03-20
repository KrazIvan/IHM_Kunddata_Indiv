USE IHM_individual;

CREATE TABLE customers (
  CustomerNumber INT PRIMARY KEY,
  Email VARCHAR(255),
  FirstName VARCHAR(255),
  LastName VARCHAR(255),
  Country VARCHAR(255),
  Zip VARCHAR(255),
  Street VARCHAR(255)
);

CREATE TABLE products (
  ProductId INT PRIMARY KEY,
  ProductName VARCHAR(255),
  ProductPrice DECIMAL(10, 2),
  ProductCategory VARCHAR(255),
  PriceClass VARCHAR(255)
);


CREATE TABLE orders (
  OrderId INT PRIMARY KEY,
  CustomerId INT,
  OrderDate DATETIME,
  FOREIGN KEY (CustomerId) REFERENCES customers(CustomerNumber)
);

CREATE TABLE orderRows(
  OrderId INT,
  ProductId INT,
  FOREIGN KEY (OrderId) REFERENCES orders(OrderId),
  FOREIGN KEY (ProductId) REFERENCES products(ProductId)
);