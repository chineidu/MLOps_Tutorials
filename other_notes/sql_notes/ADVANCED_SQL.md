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
