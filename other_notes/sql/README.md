# SQL Cheat Sheet

## Table of Contents

- [SQL Cheat Sheet](#sql-cheat-sheet)
  - [Table of Contents](#table-of-contents)
  - [SQL Data Definition Language (DDL)](#sql-data-definition-language-ddl)
    - [CREATE Statement](#create-statement)
      - [Create A Database](#create-a-database)
      - [Create A Table](#create-a-table)
    - [SELECT Statement](#select-statement)
      - [INSERT Statement](#insert-statement)
    - [WHERE CLAUSE](#where-clause)
    - [UPDATE Statement](#update-statement)
    - [DELETE Statement](#delete-statement)
    - [ORDER BY Clause](#order-by-clause)
    - [LIMIT Clause](#limit-clause)
    - [ALIAS Keyword](#alias-keyword)
    - [IN Clause](#in-clause)
    - [OR Clause](#or-clause)
    - [BETWEEN Clause](#between-clause)

## SQL Data Definition Language (DDL)

### CREATE Statement

#### Create A Database

```sql
CREATE DATABASE database_name;

# Or
CREATE DATABASE [IF NOT EXISTS] database_name;
```

#### Create A Table

```sql
CREATE TABLE [IF NOT EXISTS] table_name (
    column_name_1 datatype,
    column_name_2 datatype,
    column_name_3 datatype,
    ...
    column_name_N datatype
);

-- e.g. SQLite
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mts201 INT,
    gns203 INT
);
```

### SELECT Statement

```sql
SELECT * FROM table_name;

-- Or
SELECT column_1, column_2, ..., column_n
  FROM table_name;
```

#### INSERT Statement

```sql
INSERT INTO table_name (column_1, column_2, ..., column_n)
  VALUES (value_1, value_2, ..., value_n)
```

### WHERE CLAUSE

- It is used to filter a condition.

```sql
SELECT * FROM table_name
WHERE condition(s);

-- e.g.
SELECT * FROM students
WHERE LOWER(faculty) = "engineering" AND LOWER(last_name) = "noni";
```

### UPDATE Statement

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
  WHERE condition(s);

-- e.g.
UPDATE students
SET faculty = "ICT"
  WHERE LOWER(gender) = 'm' AND LOWER(first_name) = "segun";
```

### DELETE Statement

```sql
DELETE FROM table_name WHERE condition;

-- e.g,
DELETE FROM students
  WHERE LOWER(gender) = 'm' AND LOWER(first_name) = "bola" AND LOWER(last_name) = "obi";
```

### ORDER BY Clause

- It's used to sort your query results.
- By default, it orders by the specified column_name(s) in an ascending order. i.e ASC

```sql
SELECT column_1, column_2, ..., column_n
  FROM table_name
ORDER BY column_1, column_2, ..., column_n [ASC|DESC]
```

### LIMIT Clause

- `LIMIT` clause is ALWAYS the last statement in the query.

```sql
SELECT column_1, column_2, column_3
FROM table_name
LIMIT n;
```

### ALIAS Keyword

- You can also omit the `AS` keyword.

```sql
SELECT column_1 AS 'new_col1', column_2 AS 'new_col2',..., column_n 'new_coln'
  FROM table_name;
```

### IN Clause

```sql
SELECT column_1, column_2, ..., column_n
  FROM table_name
WHERE column_1 IN ('option_1', 'option_2', ..., 'option_n');
```

### OR Clause

```sql
SELECT column_1, column_2,..., column_n
  FROM table_name
WHERE column_1 = 'option_1' OR column_1 = 'option_2';
```

### BETWEEN Clause

```sql
SELECT column_1, column_2,..., column_n
  FROM table_name
WHERE column_1 BETWEEN num_value_1 AND num_val_2;
```
