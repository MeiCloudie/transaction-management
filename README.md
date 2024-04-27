# Transaction Management Project - Desktop Application

## Business Analysis

### 📌 Purpose

The Transaction Management Project aims to provide a flexible and user-friendly desktop application to efficiently manage users' gold and currency transactions. The main goal is to create a user-friendly interface and integrate flexible features to provide the best user experience.

### ⚠️ Scope

💰 The application will focus on managing two main types of transactions: gold transactions and currency transactions. Features will include viewing, adding, editing, and deleting transactions, as well as reports and statistical charts for data analysis.

#### Gold Transactions:

- Transaction Code
- Transaction Date (day, month, year)
- Unit Price
- Quantity
- Type of Gold
- Total Amount: Total Amount = Quantity \* Unit Price

#### Currency Transactions:

- Transaction Code
- Transaction Date (day, month, year)
- Unit Price
- Quantity
- Exchange Rate
- Currency Type (Vietnamese dong, US dollar, Euro)
- Total Amount:
  - If it's USD or Euro: Total Amount = Quantity _ Unit Price _ Exchange Rate
  - If it's Vietnamese dong: Total Amount = Quantity \* Unit Price

🙂 About Users - Account: (to be expanded later).

## Technical Requirements

The application will be developed using the Python programming language, utilizing Object-Oriented Programming (OOP) principles.

Key characteristics such as inheritance, polymorphism, and abstraction will be implemented in designing classes and modules (excluding encapsulation).

Development will be done on the Desktop platform using the Tkinter framework and supporting libraries.

Algorithms:

- Search: Linear, Binary.
- Sorting: Bubble Sort, Selection Sort, Quick Sort.

⚙️ Feature Requirements

1. Display Language on Desktop Application Screen:
   English.

2. List of basic features required:

   - View Transactions: Filter Tab, Group By, Sort By, Filter, Search.
   - Add Transaction.
   - View Transaction Details.
   - Edit Transaction.
   - Delete Transaction.
   - Report statistical charts: Week Tab (this week) or Month (this month), using Charts (pie chart, bar chart), and Filter.

3. Data Organization
   After completing all functions, store data in JSON file format => issues regarding JSON file Reading & Writing.

   Expansion: Upgrade to version 2 using API.

## 💡 Expansion

- Account.
- API.

(Organization and additional updates will be added after completing the basic features)
