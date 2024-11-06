import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import datetime

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nitesh462",
        database="library_db"
    )

# Add a new book to the library
def add_book(title, author, year):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, available) VALUES (%s, %s, %s, TRUE)", (title, author, year))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Book added successfully!")

# Add a new user
def add_user(name, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "User added successfully!")

# Borrow a book
def borrow_book(book_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET available = FALSE WHERE book_id = %s", (book_id,))
    cursor.execute("INSERT INTO transactions (book_id, user_id, borrow_date) VALUES (%s, %s, %s)",
                   (book_id, user_id, datetime.date.today()))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Book borrowed successfully!")

# Return a book
def return_book(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET available = TRUE WHERE book_id = (SELECT book_id FROM transactions WHERE transaction_id = %s)", (transaction_id,))
    cursor.execute("UPDATE transactions SET return_date = %s WHERE transaction_id = %s", 
                   (datetime.date.today(), transaction_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Book returned successfully!")

# View all books
def view_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author, year, available FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    # Clear existing entries in the treeview
    for row in book_tree.get_children():
        book_tree.delete(row)

    # Insert new entries with availability as "Yes" or "No"
    for book in books:
        available = "Yes" if book[4] else "No"
        book_tree.insert("", "end", values=(book[0], book[1], book[2], book[3], available))

# View all users
def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Clear existing entries in the treeview
    for row in user_tree.get_children():
        user_tree.delete(row)

    # Insert new entries
    for user in users:
        user_tree.insert("", "end", values=(user[0], user[1], user[2]))

# View active transactions
def view_active_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT t.transaction_id, b.title, u.name, t.borrow_date "
                   "FROM transactions t "
                   "JOIN books b ON t.book_id = b.book_id "
                   "JOIN users u ON t.user_id = u.user_id "
                   "WHERE t.return_date IS NULL")
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    # Clear existing entries in the transaction_tree
    for row in transaction_tree.get_children():
        transaction_tree.delete(row)

    # Insert new entries
    for transaction in transactions:
        transaction_tree.insert("", "end", values=(transaction[0], transaction[1], transaction[2], transaction[3]))

# GUI Functions for button actions
def add_book_gui():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    if title and author and year.isdigit():
        add_book(title, author, int(year))
    else:
        messagebox.showerror("Error", "Please enter valid book details.")

def add_user_gui():
    name = user_name_entry.get()
    email = user_email_entry.get()
    if name and email:
        add_user(name, email)
    else:
        messagebox.showerror("Error", "Please enter valid user details.")

def borrow_book_gui():
    book_id = book_id_entry.get()
    user_id = user_id_entry.get()
    if book_id.isdigit() and user_id.isdigit():
        borrow_book(int(book_id), int(user_id))
    else:
        messagebox.showerror("Error", "Please enter valid IDs.")

def return_book_gui():
    transaction_id = transaction_id_entry.get()
    if transaction_id.isdigit():
        return_book(int(transaction_id))
    else:
        messagebox.showerror("Error", "Please enter a valid Transaction ID.")

# GUI Setup
app = tk.Tk()
app.title("Library Management System")
app.geometry("1000x600")

# Create Notebook for tabs
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True)

# Tab for adding books
add_book_tab = ttk.Frame(notebook)
notebook.add(add_book_tab, text="Add Book")

tk.Label(add_book_tab, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
title_entry = tk.Entry(add_book_tab, width=30)
title_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(add_book_tab, text="Author:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
author_entry = tk.Entry(add_book_tab, width=30)
author_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(add_book_tab, text="Year:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
year_entry = tk.Entry(add_book_tab, width=30)
year_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(add_book_tab, text="Add Book", command=add_book_gui).grid(row=3, columnspan=2, pady=10)

# Tab for adding users
add_user_tab = ttk.Frame(notebook)
notebook.add(add_user_tab, text="Add User")

tk.Label(add_user_tab, text="User Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
user_name_entry = tk.Entry(add_user_tab, width=30)
user_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(add_user_tab, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
user_email_entry = tk.Entry(add_user_tab, width=30)
user_email_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(add_user_tab, text="Add User", command=add_user_gui).grid(row=2, columnspan=2, pady=10)

# Tab for borrowing books
borrow_book_tab = ttk.Frame(notebook)
notebook.add(borrow_book_tab, text="Borrow Book")

tk.Label(borrow_book_tab, text="Book ID:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
book_id_entry = tk.Entry(borrow_book_tab, width=30)
book_id_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(borrow_book_tab, text="User ID:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
user_id_entry = tk.Entry(borrow_book_tab, width=30)
user_id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(borrow_book_tab, text="Borrow Book", command=borrow_book_gui).grid(row=2, columnspan=2, pady=10)

# Tab for returning books
return_book_tab = ttk.Frame(notebook)
notebook.add(return_book_tab, text="Return Book")

tk.Label(return_book_tab, text="Transaction ID:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
transaction_id_entry = tk.Entry(return_book_tab, width=30)
transaction_id_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Button(return_book_tab, text="Return Book", command=return_book_gui).grid(row=1, columnspan=2, pady=10)

# Tab for viewing books
view_books_tab = ttk.Frame(notebook)
notebook.add(view_books_tab, text="View Books")

# Treeview for displaying books
book_tree = ttk.Treeview(view_books_tab, columns=("Book ID", "Title", "Author", "Year", "Available"), show='headings')
book_tree.heading("Book ID", text="Book ID")
book_tree.heading("Title", text="Title")
book_tree.heading("Author", text="Author")
book_tree.heading("Year", text="Year")
book_tree.heading("Available", text="Available")
book_tree.column("Book ID", width=80)
book_tree.pack(padx=10, pady=10, fill='both', expand=True)

# Button to refresh books list
tk.Button(view_books_tab, text="Refresh Books", command=view_books).pack(pady=10)

# Tab for viewing users
view_users_tab = ttk.Frame(notebook)
notebook.add(view_users_tab, text="View Users")

# Treeview for displaying users
user_tree = ttk.Treeview(view_users_tab, columns=("User ID", "Name", "Email"), show='headings')
user_tree.heading("User ID", text="User ID")
user_tree.heading("Name", text="Name")
user_tree.heading("Email", text="Email")
user_tree.pack(padx=10, pady=10, fill='both', expand=True)

# Button to refresh users list
tk.Button(view_users_tab, text="Refresh Users", command=view_users).pack(pady=10)

# Tab for viewing active transactions
view_transactions_tab = ttk.Frame(notebook)
notebook.add(view_transactions_tab, text="Active Transactions")

# Treeview for displaying active transactions
transaction_tree = ttk.Treeview(view_transactions_tab, columns=("Transaction ID", "Book Title", "User Name", "Borrow Date"), show='headings')
transaction_tree.heading("Transaction ID", text="Transaction ID")
transaction_tree.heading("Book Title", text="Book Title")
transaction_tree.heading("User Name", text="User Name")
transaction_tree.heading("Borrow Date", text="Borrow Date")
transaction_tree.pack(padx=10, pady=10, fill='both', expand=True)

# Button to refresh active transactions
tk.Button(view_transactions_tab, text="Refresh Transactions", command=view_active_transactions).pack(pady=10)

# Run the app
app.mainloop()
