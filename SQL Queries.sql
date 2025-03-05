# 1. Check Availability of eBooks vs Physical Books
SELECT 
    COUNT(CASE WHEN is_Ebook = 1 THEN 1 END) AS ebooks,
    COUNT(CASE WHEN is_Ebook = 0 THEN 1 END) AS physical_books
FROM dance_book_data;
-- ------------------------------------------------------

# 2. Find the Publisher with the Most Books Published
SELECT publisher, count(*) AS top_publisher
FROM dance_book_data
group by publisher
order by top_publisher desc
limit 1;
-- ------------------------------------------------------

# 3. Identify the Publisher with the Highest Average Rating
select publisher, avg(average_Rating) as Avg_Rating
from dance_book_data
group by publisher
order by Avg_Rating desc
limit 1;
-- ------------------------------------------------------

# 4. Get the Top 5 Most Expensive Books by Retail Price
select book_title, amount_retailPrice
from dance_book_data
order by amount_retailPrice desc
limit 5;
-- ------------------------------------------------------

# 5. Find Books Published After 2010 with at Least 500 Pages
select book_title, year, page_Count
from dance_book_data
where year > 2010 and page_Count >= 500
order by year asc;
-- ------------------------------------------------------

# 6. List Books with Discounts Greater than 20%
select book_title, 
       ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 as discount_above_20_percentage
from dance_book_data
where amount_listPrice > 0 and ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 > 20
order by discount_above_20_percentage asc;
-- ------------------------------------------------------

# 7. Find the Average Page Count for eBooks vs Physical Books
SELECT is_Ebook, AVG(page_Count) AS Average_Page_Count
FROM dance_book_data
GROUP BY is_Ebook;
   
     # 0 - true
     # 1 - false
-- ------------------------------------------------------

# 8. Find the Top 3 Authors with the Most Books
select book_authors, count(*) as total_books
from dance_book_data
group by book_authors
order by total_books desc
limit 3;
-- ------------------------------------------------------

# 9. List Publishers with More than 10 Books
select publisher, count(*) as total_books
from dance_book_data
group by publisher
having total_books > 10
order by total_books desc;
-- ------------------------------------------------------

# 10. Find the Average Page Count for Each Category
select categories, avg(page_Count) as avg_page_count
from dance_book_data
group by categories
order by avg_page_count desc;
-- ------------------------------------------------------

# 11. Retrieve Books with More than 3 Authors
SELECT book_title, book_authors
FROM dance_book_data
WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) >= 3;
-- ------------------------------------------------------

# 12. Books with Ratings Count Greater Than the Average
SELECT book_title, ratings_Count
FROM dance_book_data
WHERE ratings_Count > (SELECT AVG(ratings_Count) FROM dance_book_data)
order by ratings_Count desc;
-- ------------------------------------------------------

# 13. Books with the Same Author Published in the Same Year
SELECT book_authors, year, COUNT(*) AS books_published
FROM dance_book_data
GROUP BY book_authors, year
HAVING books_published > 1
order by year asc;
-- ------------------------------------------------------

# 14. Books with a Specific Keyword in the Title
SELECT book_title
FROM dance_book_data
WHERE book_title LIKE '%dance%';
-- ------------------------------------------------------

# 15. Year with the Highest Average Book Price
SELECT year, AVG(amount_retailPrice) AS avg_price
FROM dance_book_data
GROUP BY year
ORDER BY avg_price DESC
LIMIT 1;
-- ------------------------------------------------------

# 16. Count Authors Who Published 3 Consecutive Years
SELECT 
    book_authors, 
    COUNT(DISTINCT year) AS consecutive_years
FROM dance_book_data
GROUP BY book_authors
HAVING MAX(year) - MIN(year) >= 2
order by consecutive_years desc;

-- ------------------------------------------------------

# 17. Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year.
SELECT 
    book_authors, 
    year, 
    COUNT(DISTINCT publisher) AS publisher_count
FROM dance_book_data
GROUP BY book_authors, year
HAVING COUNT(DISTINCT publisher) > 1
order by year asc;

-- ------------------------------------------------------

# 18. Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries.
SELECT 
    AVG(CASE WHEN is_Ebook = 1 THEN amount_retailPrice END) AS avg_ebook_price,
    AVG(CASE WHEN is_Ebook = 0 THEN amount_retailPrice END) AS avg_physical_price
FROM dance_book_data;

-- ------------------------------------------------------

# 19. Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers.
WITH stats AS (
    SELECT 
        AVG(average_Rating) AS avg_rating, 
        STDDEV(average_Rating) AS std_dev
    FROM dance_book_data
)
SELECT 
    book_title, 
    average_Rating, 
    ratings_Count
FROM dance_book_data, stats
WHERE average_Rating > (stats.avg_rating + 2 * stats.std_dev)
   OR average_Rating < (stats.avg_rating - 2 * stats.std_dev);
-- ------------------------------------------------------

# 20. Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published.
SELECT publisher, AVG(average_Rating) AS avg_rating, COUNT(*) AS total_books
FROM dance_book_data
GROUP BY publisher
HAVING total_books > 10
ORDER BY avg_rating DESC
LIMIT 1;
