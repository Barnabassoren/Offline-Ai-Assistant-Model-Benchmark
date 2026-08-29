# Database Normalization

## What is Normalization?

Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. It involves dividing large tables into smaller, related tables and defining relationships between them using foreign keys. The main goals are to eliminate redundant data, ensure data dependencies make logical sense, and reduce the chances of data anomalies during insert, update, and delete operations. Without normalization, databases can suffer from update anomalies, where changing one piece of data requires changing it in multiple places, insertion anomalies, where you can't add certain data without also having unrelated data present, and deletion anomalies, where deleting one piece of data unintentionally removes other useful data.

## First Normal Form (1NF)

A table is in 1NF if all columns contain atomic, indivisible values, each column contains values of a single type, and each row is unique, typically enforced by a primary key. A common violation is storing multiple values in a single column, such as a "Subjects" column containing "Math, Physics, Chemistry" as one comma-separated string instead of separate rows or a separate table entirely.

## Second Normal Form (2NF)

A table is in 2NF if it is already in 1NF and all non-key attributes are fully functionally dependent on the entire primary key, not just part of it. This rule specifically matters for tables that have a composite primary key made of two or more columns. If a non-key column depends on only one part of that composite key rather than the whole thing, the table violates 2NF and should be split into separate tables to remove that partial dependency.

## Third Normal Form (3NF)

A table is in 3NF if it is already in 2NF and contains no transitive dependencies, meaning non-key attributes should not depend on other non-key attributes. For example, if StudentID determines DeptID, and DeptID determines DeptName, then DeptName depends transitively on StudentID through DeptID. This violates 3NF, and DeptName should be moved into a separate Department table where DeptID is the primary key.

## Example SQL

Here is a normalized schema separating students from departments:

```sql
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100),
    DeptID INT,
    FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
);

CREATE TABLE Department (
    DeptID INT PRIMARY KEY,
    DeptName VARCHAR(100)
);
```

## Denormalization

Denormalization is the deliberate introduction of redundancy into a database design for performance reasons. It is often used in read-heavy systems like data warehouses and reporting systems, where joining many normalized tables on every query becomes too slow. Denormalization trades increased storage and more complex update logic for significantly faster read queries, since fewer joins are needed to retrieve the data an application actually wants to display.