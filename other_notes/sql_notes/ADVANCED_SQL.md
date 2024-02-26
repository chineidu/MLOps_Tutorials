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

-- e.g.
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
```
