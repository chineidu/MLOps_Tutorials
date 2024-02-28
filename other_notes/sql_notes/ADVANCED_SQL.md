# SQL

## Table of Content

- [SQL](#sql)
  - [Table of Content](#table-of-content)
  - [Database Design](#database-design)
    - [Intro](#intro)
    - [Free Hosted Postgres DB](#free-hosted-postgres-db)
      - [CREATE A Table](#create-a-table)
      - [INSERT Statement](#insert-statement)
      - [SELECT Statement](#select-statement)
    - [Filtering](#filtering)
      - [WHERE CLAUSE](#where-clause)
      - [UPDATE Statement](#update-statement)
      - [DELETE Statement](#delete-statement)
    - [Database For A Photo-Sharing App](#database-for-a-photo-sharing-app)
    - [Relationships](#relationships)
      - [One-to-Many And Many-to-One Relationships](#one-to-many-and-many-to-one-relationships)
      - [One-to-One And Many-to-Many Relationships](#one-to-one-and-many-to-many-relationships)
      - [Primary Key](#primary-key)
      - [Foreign Key](#foreign-key)
    - [Relating Records With Joins](#relating-records-with-joins)
      - [Inner Join](#inner-join)
      - [Left Outer Join](#left-outer-join)
      - [Right Outer Join](#right-outer-join)
      - [Full Join](#full-join)
    - [Aggregations](#aggregations)
      - [Grouping](#grouping)
      - [Aggregates](#aggregates)
    - [HAVING Clause](#having-clause)

## Database Design

### Intro

- Design Process

[![image.png](https://i.postimg.cc/50FnNS6w/image.png)](https://postimg.cc/CBSjcDC1)

- A simple table in a database

[![image.png](https://i.postimg.cc/DzVwW2zR/image.png)](https://postimg.cc/LJTpwFLV)

### Free Hosted Postgres DB

- [pq-sql.com]([pq-sql.com](https://pg-sql.com/))

#### CREATE A Table

```sql
CREATE TABLE [IF NOT EXISTS] table_name (
    column_name_1 datatype,
    column_name_2 datatype,
    column_name_3 datatype,
    ...
    column_name_N datatype
);

-- e.g. SQLite
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    country VARCHAR(100),
    population INTEGER,
    area INTEGER
);

-- e.g. Postgres
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY, -- autoincrement
    name VARCHAR(100),
    country VARCHAR(100),
    population INTEGER,
    area INTEGER
);
```

#### INSERT Statement

```sql
INSERT INTO table_name (column_1, column_2, ..., column_n)
  VALUES (value_1, value_2, ..., value_n);

-- e.g.
INSERT INTO cities (name, country, population, area)
VALUES
  ("Tokyo", "Japan", 37400068, 8223),
  ("Delhi", "India", 28514000, 2240),
  ("Shanghai", "China", 25528000, 4015);

```

#### SELECT Statement

```sql
SELECT * FROM table_name;

-- e.g.
SELECT * FROM cities;
SELECT name, population FROM cities;

-- Alias
SELECT name, country, (population / area) AS "population_density" FROM cities;
-- OR
SELECT name, country, (population / area) "population_density" FROM cities;
```

### Filtering

#### WHERE CLAUSE

- It is used to filter a condition.
- The order of execution is shown below:

[![image.png](https://i.postimg.cc/cHdhSgVm/image.png)](https://postimg.cc/1gYw0tRn)

```sql
SELECT * FROM table_name
WHERE condition(s);

-- e.g.
SELECT name, population, area FROM cities
  WHERE area > 4000;
```

#### UPDATE Statement

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
  WHERE condition(s);

-- e.g.
UPDATE cities
SET population = 26500000
  WHERE name = "Shanghai";
```

#### DELETE Statement

```sql
DELETE FROM table_name WHERE condition;

-- e.g.
DELETE FROM cities
  WHERE name = 'Shanghai' AND country = "China";
```

### Database For A Photo-Sharing App

- This example assumes that the photo-sharing app has a table with the following columns:
  - users
  - photos
  - comments
  - likes

[![image.png](https://i.postimg.cc/mDLty2p8/image.png)](https://postimg.cc/2qtkzmDZ)

### Relationships

#### One-to-Many And Many-to-One Relationships

[![image.png](https://i.postimg.cc/Z5DWxSzS/image.png)](https://postimg.cc/nXBVnNLR)

- From the student's perspective: One-to-Many. i.e. a student can belong to many clubs.
- In a one-to-many relationship, a single record in one table (parent table) can be linked to multiple records in another table (child table).

- From the club's perspective: Many-to-One. i.e. a many clubs belong to a single student.
- This is the inverse of a one-to-many relationship. Here, multiple records in one table (child table) can be linked to a single record in another table (parent table).

#### One-to-One And Many-to-Many Relationships

- One-to-one: A single record in one table (parent table) is linked to exactly one record in another table (child table). This is less common than other relationship types but can be useful in specific scenarios.

- Many-to-many: This relationship allows multiple records in one table (table A) to be linked to multiple records in another table (table B). This is typically achieved through a junction table or bridge table.

#### Primary Key

- **Definition:** The `primary key` is a unique identifier for each record in a table. It's a mandatory and non-nullable column (cannot be empty) that guarantees every record is distinct and can be uniquely retrieved.

- **Importance:**
  - Ensures data integrity by preventing duplicate records.
  - Serves as the anchor point for establishing relationships with other tables.
  - Optimizes data retrieval and manipulation by allowing efficient indexing.

```sql
CREATE TABLE table_name (
    column_name_1 datatype,
    column_name_2 datatype,
    column_name_3 datatype,
    ...
    column_name_N datatype
);

-- e.g. Postgres
CREATE TABLE users (
    id SERIAL PRIMARY KEY, -- primarykey!
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(250)
);
```

#### Foreign Key

- **Definition:** A `foreign key` is also a unique column (or a combination of columns) within a table, but unlike the primary key, it's optional. It can be nullable and can have duplicate values as long as they don't belong to the same record (identified by the primary key).

- **Purpose:**
- Provides alternative ways to efficiently retrieve specific data based on frequently used search criteria.
- Enforces additional data integrity constraints, such as ensuring certain values are unique within that specific column or group of columns.

```sql
CREATE TABLE photos (
    id SERIAL PRIMARY KEY, -- primarykey!
    url VARCHAR(150),
    users_id INTEGER REFERENCES users(id)  -- foreign key
);
```

### Relating Records With Joins

- It produces values by merging together different related tables.
- Use a `join` when you're asked to find data that involves multiple resources/tables.

[![image.png](https://i.postimg.cc/zXCgwhvC/image.png)](https://postimg.cc/CzK5Szj5)

#### Inner Join

- Returns records that have matching values in both tables based on the specified join condition.
- This is the default behaviour.

```sql
-- ex 1
SELECT * FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- ex 2 (Ignore the keyword INNER)
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

#### Left Outer Join

- Returns all records from the `left table` (specified first) and matching records from the right table based on the join condition.
- If there's no match in the right table, it fills the corresponding columns with `null` values.

```sql
SELECT * FROM orders o
LEFT JOIN products p ON o.product_id = p.id;
```

#### Right Outer Join

- Similar to left join, but reverses the behavior. It returns all records from the `right table` (specified first) and matching records from the left table based on the join condition.
- Unmatched records in the left table will have null values in their corresponding columns.

```sql
SELECT * FROM products p
RIGHT JOIN orders o ON o.product_id = p.id;
```

#### Full Join

- Returns all records from both tables, regardless of whether there's a match in the other table.
- Unmatched records will have null values in the corresponding columns of the unmatched table.

```sql
SELECT * FROM orders o
FULL JOIN customers c ON o.customer_id = c.id;
```

### Aggregations

- It looks at many rows and calculates a single value.
- Words like `most`, `average`, `least` are a sign that you need to use an aggregation.
- `Grouping` and `aggregates` are often used together to analyze and summarize data at different levels of detail. You can group data by multiple columns and apply various aggregate functions to gain deeper insights from your data.

#### Grouping

- **Concept:** Grouping involves categorizing rows in a table based on shared values in one or more columns. This creates groups of related data, enabling you to analyze and summarize these groups effectively.
- **Implementation:** You use the GROUP BY clause in your SELECT statement to specify the column(s) used for grouping.

```sql
SELECT country, COUNT(*) AS total_customers
FROM customers
GROUP BY country;
```

- This query groups the customers table by the country column and calculates the total number of customers for each country using the COUNT(*) aggregate function.

#### Aggregates

- Concept: Aggregates are functions that compute a single value (summary statistic) based on a group of rows. These functions operate on the entire group or specific columns within the group.

- Common Aggregate Functions:
  - `COUNT(*)`: Counts the number of rows in a group.
  - `SUM(column)`: Calculates the sum of values in a specified column across the group.
  - `AVG(column)`: Computes the average value in a specified column within the group.
  - `MIN(column)`: Finds the minimum value in a specified column within the group.
  - `MAX(column)`: Finds the maximum value in a specified column within the group.

```sql
SELECT genre, AVG(rating) AS average_rating
FROM movies
GROUP BY genre;
```

- This query groups the `movies` table by the genre column and calculates the average rating `(AVG(rating)` for each genre.

### HAVING Clause

- The `HAVING` clause provides a way to filter groups created with the `GROUP BY` clause.
- It allows you to specify conditions that must be met for a group to be included in the final result set.
- Here's how it works:
  - **Grouping**: Your SELECT statement uses `GROUP BY` to categorize rows based on shared values in specific columns, creating groups.
  - **Aggregation**: You apply aggregate functions like `COUNT`, `SUM`, `AVG`, etc., to calculate summary statistics for each group.
  - **Filtering**: The `HAVING` clause specifies a condition that must be true for the aggregate values of a group. Only groups that satisfy this condition are included in the final result set.

```sql
SELECT column1, aggregate_function(column2) AS alias
FROM table_name
GROUP BY column1
HAVING condition_on_aggregate;

-- ex 1
SELECT genre, AVG(rating) AS average_rating
FROM movies
GROUP BY genre
HAVING AVG(rating) > 4;


-- ex 2
SELECT country, COUNT(*) AS total_customers
FROM customers
GROUP BY country
HAVING COUNT(*) > 100;
```

**Note**: The `HAVING` clause cannot be used without a prior GROUP BY clause in the same SELECT statement. It operates on the aggregate values calculated after grouping.
