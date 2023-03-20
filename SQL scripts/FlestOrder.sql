USE IHM_indiv;

-- Visar kunder som har flest ordrar under de senaste året.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName, COUNT(*) AS OrderCount
FROM orders
INNER JOIN customers ON orders.CustomerId = customers.CustomerNumber
WHERE orders.OrderDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY customers.CustomerNumber
ORDER BY OrderCount DESC;


-- Visar kunder som har flest ordrar under de senaste två åren.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName, COUNT(*) AS OrderCount
FROM orders
INNER JOIN customers ON orders.CustomerId = customers.CustomerNumber
WHERE orders.OrderDate >= DATE_SUB(NOW(), INTERVAL 2 YEAR)
GROUP BY customers.CustomerNumber
ORDER BY OrderCount DESC;


-- Visar kunder som har flest ordrar under de senaste fyra åren.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName, COUNT(*) AS OrderCount
FROM orders
INNER JOIN customers ON orders.CustomerId = customers.CustomerNumber
WHERE orders.OrderDate >= DATE_SUB(NOW(), INTERVAL 4 YEAR)
GROUP BY customers.CustomerNumber
ORDER BY OrderCount DESC;


-- Visar kunder som har flest ordrar över all tid.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName, COUNT(*) AS OrderCount
FROM orders
INNER JOIN customers ON orders.CustomerId = customers.CustomerNumber
GROUP BY customers.CustomerNumber
ORDER BY OrderCount DESC;