USE IHM_indiv;

-- Hur många kunder är från Stockholmsregionen?
SELECT COUNT(*) AS CustomerCount
FROM customers
WHERE LEFT(customers.Zip, 2) = "11"; -- Postnummer för Stockholmsregione börjar på 11.


-- Vilket län har flest kunder?
SELECT LEFT(customers.Zip, 2) AS Län, COUNT(*) AS CustomerCount
FROM customers
GROUP BY Län
ORDER BY CustomerCount DESC
LIMIT 1;


-- Visa kunder som har handlat i flera år (3 år):
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
INNER JOIN orders ON orders.CustomerId = customers.CustomerNumber
GROUP BY customers.CustomerNumber
HAVING COUNT(DISTINCT YEAR(orders.OrderDate)) >= 3;


-- Visa kunder som har handlat innan, men har slutat på senaste år.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
LEFT JOIN orders ON orders.CustomerId = customers.CustomerNumber AND orders.OrderDate >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
WHERE orders.OrderId IS NULL;

-- Visa kunder som har handlat över flera år och är aktiva kunder.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
INNER JOIN orders ON orders.CustomerId = customers.CustomerNumber
WHERE YEAR(orders.OrderDate) >= YEAR(NOW()) - 3
GROUP BY customers.CustomerNumber
HAVING COUNT(DISTINCT YEAR(orders.OrderDate)) >= 3;


-- Visa kunder som har aldrig handlat.
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
LEFT JOIN orders ON orders.CustomerId = customers.CustomerNumber
WHERE orders.OrderId IS NULL;


-- Visa kunder som handlar helst varumärkeprodukter (minst 10% mer än egna-märken-produkter).
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
INNER JOIN orders ON orders.CustomerId = customers.CustomerNumber
INNER JOIN orderRows ON orderRows.OrderId = orders.OrderId
INNER JOIN products ON products.ProductId = orderRows.ProductId
WHERE products.PriceClass = 'brands'
GROUP BY customers.CustomerNumber
HAVING SUM(CASE WHEN products.PriceClass = 'brands' THEN 1 ELSE 0 END) >= 
    1.1 * SUM(CASE WHEN products.PriceClass = 'private_label' THEN 1 ELSE 0 END);

-- Visa kunder som handlar helst egna-märken-produkter (minst 10% mer än varumärkeprodukterr). 
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
INNER JOIN orders ON orders.CustomerId = customers.CustomerNumber
INNER JOIN orderRows ON orderRows.OrderId = orders.OrderId
INNER JOIN products ON products.ProductId = orderRows.ProductId
WHERE products.PriceClass = 'private_label'
GROUP BY customers.CustomerNumber
HAVING SUM(CASE WHEN products.PriceClass = 'private_label' THEN 1 ELSE 0 END) >= 
    1.1 * SUM(CASE WHEN products.PriceClass = 'brands' THEN 1 ELSE 0 END);

-- Visa kunder som handlar båda typer av produkter ungefär lika mycket (inte mer eller mindre än 10% från båda hållen).
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
INNER JOIN orders ON orders.CustomerId = customers.CustomerNumber
INNER JOIN orderRows ON orderRows.OrderId = orders.OrderId
INNER JOIN products ON products.ProductId = orderRows.ProductId
GROUP BY customers.CustomerNumber
HAVING 
    ABS(
        SUM(CASE WHEN products.PriceClass = 'brands' THEN 1 ELSE 0 END) 
        - SUM(CASE WHEN products.PriceClass = 'private_label' THEN 1 ELSE 0 END)
    ) 
    <= 0.1 * ( 
        SUM(CASE WHEN products.PriceClass = 'brands' THEN 1 ELSE 0 END) 
        + SUM(CASE WHEN products.PriceClass = 'private_label' THEN 1 ELSE 0 END)
    );

-- Visa kunder där det inte går avgöra vilken preferens de har (för att de har aldrig handlat).
SELECT customers.CustomerNumber, customers.FirstName, customers.LastName
FROM customers
LEFT JOIN orders ON orders.CustomerId = customers.CustomerNumber
WHERE orders.OrderId IS NULL;
