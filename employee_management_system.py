import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from tkinter import PhotoImage
from PIL import Image, ImageTk 
from tkinter import font  
import tkinter.font as tkFont


# Create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='employee_db',
            user='root',  # replace with your MySQL username
            password='CHEPCanada2024'  # replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Connection Error", f"Error: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()

# Employee CRUD operations
def create_employee(connection, first_name, last_name, department_id, salary, supervisor_id=None):
    cursor = connection.cursor()
    sql = "INSERT INTO employees (first_name, last_name, department_id, salary, supervisor_id) VALUES (%s, %s, %s, %s, %s)"
    val = (first_name, last_name, department_id, salary, supervisor_id)
    cursor.execute(sql, val)
    connection.commit()
    messagebox.showinfo("Success", f"Employee {first_name} {last_name} added successfully.")

def update_employee(connection, employee_id, first_name, last_name, department_id, salary, supervisor_id=None):
    cursor = connection.cursor()
    sql = """UPDATE employees
             SET first_name = %s, last_name = %s, department_id = %s, salary = %s, supervisor_id = %s
             WHERE employee_id = %s"""
    val = (first_name, last_name, department_id, salary, supervisor_id, employee_id)
    cursor.execute(sql, val)
    connection.commit()
    messagebox.showinfo("Success", f"Employee {employee_id} updated successfully.")

def delete_employee(connection, employee_id):
    cursor = connection.cursor()
    print(f"Attempting to delete employee with ID: {employee_id}")  # Debugging line
    sql = "DELETE FROM employees WHERE employee_id = %s"
    val = (employee_id,)
    cursor.execute(sql, val)
    connection.commit()
    print(f"Deleted employee with ID: {employee_id}")  # Confirm deletion
    messagebox.showinfo("Success", f"Employee {employee_id} deleted successfully.")


def read_employees(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT e.employee_id, e.first_name, e.last_name, d.name AS department_name, e.salary, e.supervisor_id 
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
    """)
    rows = cursor.fetchall()
    return rows


# Department CRUD operations
def create_department(connection, name):
    cursor = connection.cursor()
    sql = "INSERT INTO departments (name) VALUES (%s)"
    val = (name,)
    cursor.execute(sql, val)
    connection.commit()
    messagebox.showinfo("Success", f"Department {name} added successfully.")

def read_departments(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT department_id, name FROM departments")
    rows = cursor.fetchall()
    return rows

def delete_department(self, name, departments, delete_window):
    department_id = None
    for dept_name, dept_id in departments:
        if dept_name == name:
            department_id = dept_id
            break

    if department_id is None:
        messagebox.showerror("Error", "Invalid department selected.")
        return

    cursor = self.connection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM employees WHERE department_id = %s", (department_id,))
        employee_count = cursor.fetchone()[0]

        if employee_count > 0:
            messagebox.showerror("Error", f"Cannot delete department '{name}': it has {employee_count} associated employees.")
        else:
            cursor.execute("DELETE FROM departments WHERE department_id = %s", (department_id,))
            self.connection.commit()
            messagebox.showinfo("Success", f"Department '{name}' deleted successfully.")
            delete_window.destroy()  # Close the delete window
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while deleting the department.")
        print(f"Error: {e}")


# Helper Functions
def get_valid_employee_ids(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT employee_id FROM employees")
    rows = cursor.fetchall()
    return {row[0] for row in rows}

def get_valid_department_ids(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT department_id FROM departments")
    rows = cursor.fetchall()
    return {row[0] for row in rows}

def all_fields_filled(*fields):
    """Checks if all fields are filled."""
    for field in fields:
        if not field.strip():  # Check if the field is empty or contains only spaces
            return False
    return True

def validate_numeric_input(value):
    """Validate if the input is numeric."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_employee_id(connection, employee_id):
    valid_ids = get_valid_employee_ids(connection)
    return int(employee_id) in valid_ids

def validate_department_id(connection, department_id):
    valid_ids = get_valid_department_ids(connection)
    return int(department_id) in valid_ids


# Complex query functions
def complex_query_1(connection):
    cursor = connection.cursor()
    sql = """
    WITH salary_rank AS (
        SELECT employee_id, salary,
               PERCENT_RANK() OVER (ORDER BY salary) AS percentile
        FROM employees
    )
    SELECT e.first_name, e.last_name, sr.salary
    FROM employees e
    JOIN salary_rank sr ON e.employee_id = sr.employee_id
    WHERE sr.percentile >= 0.90;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def complex_query_2(connection):
    cursor = connection.cursor()
    sql = """
    SELECT d.name AS department, SUM(e.salary) AS total_expenditure
    FROM departments d
    JOIN employees e ON d.department_id = e.department_id
    GROUP BY ROLLUP(d.name);
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    # Replace None with 'Total' for the department name
    rows = [('Total' if department is None else department, total_expenditure) for department, total_expenditure in rows]

    return rows

def complex_query_3(connection):
    cursor = connection.cursor()
    sql = """
    WITH DepartmentHighestSalary AS (
        SELECT department_id, MAX(salary) AS max_salary
        FROM employees
        GROUP BY department_id
    )
    SELECT d.name, e.first_name, e.last_name, e.salary
    FROM DepartmentHighestSalary dh
    JOIN employees e ON dh.department_id = e.department_id AND dh.max_salary = e.salary
    JOIN departments d ON dh.department_id = d.department_id;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def complex_query_4(connection):
    cursor = connection.cursor()
    sql = """
    SELECT e.first_name AS employee_first_name, e.last_name AS employee_last_name,
           s.first_name AS supervisor_first_name, s.last_name AS supervisor_last_name, e.salary
    FROM employees e
    JOIN employees s ON e.supervisor_id = s.employee_id
    WHERE e.salary = s.salary;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def complex_query_5(connection):
    cursor = connection.cursor()
    sql = """
    SELECT e.first_name, e.last_name,e.salary, d.name
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE e.supervisor_id IS NULL;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def complex_query_6(connection):
    cursor = connection.cursor()
    sql = """
    SELECT e.first_name, e.last_name, e.salary, d.name AS department_name,
           RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_rank
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    ORDER BY d.name, salary_rank;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def complex_query_7(connection):
    cursor = connection.cursor()
    sql = """
    SELECT d.name, AVG(e.salary) AS department_avg_salary, (SELECT AVG(salary) FROM employees) AS total_avg_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.name
    HAVING AVG(e.salary) > (SELECT AVG(salary) FROM employees);
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def complex_query_8(connection):
    cursor = connection.cursor()
    sql = """
    SELECT d.name, COUNT(DISTINCT e.employee_id) AS employee_count
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.name;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def complex_query_9(connection):
    cursor = connection.cursor()
    sql = """
    SELECT e.first_name, e.last_name, e.salary, d.name AS department_name,
           AVG(e.salary) OVER (PARTITION BY e.department_id) AS avg_department_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def complex_query_10(connection):
    cursor = connection.cursor()
    sql = """
    WITH DepartmentAverage AS (
        SELECT department_id, AVG(salary) AS avg_salary
        FROM employees
        GROUP BY department_id
    )
    SELECT d.name, e.first_name, e.last_name, e.salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    JOIN DepartmentAverage da ON e.department_id = da.department_id
    WHERE e.salary > da.avg_salary;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# GUI Setup
class App:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Employee Management System")

       
        # Load and convert icon images for main buttons
        self.employee_icon_large = ImageTk.PhotoImage(Image.open("Images/Employee icon.png"))  # Large employee icon
        self.department_icon_large = ImageTk.PhotoImage(Image.open("Images/Department icon.png"))  # Large department icon
        self.query_icon_large = ImageTk.PhotoImage(Image.open("Images/query_icon.png"))  # Large query icon
        self.exit_icon_large = ImageTk.PhotoImage(Image.open("Images/Exit icon.png"))  # Large exit icon

        # Main buttons (large icons)
        self.employee_button = ttk.Button(self.root, image=self.employee_icon_large, text="Employee Operations", compound=tk.TOP, command=self.show_employee_operations)
        self.employee_button.grid(row=0, column=0, padx=20, pady=20)

        self.department_button = ttk.Button(self.root, image=self.department_icon_large, text="Department Operations", compound=tk.TOP, command=self.show_department_operations)
        self.department_button.grid(row=0, column=1, padx=20, pady=20)

        self.query_button = ttk.Button(self.root, image=self.query_icon_large, text="Advanced Queries", compound=tk.TOP, command=self.show_advanced_queries)
        self.query_button.grid(row=0, column=2, padx=20, pady=20)

        self.exit_button = ttk.Button(self.root, image=self.exit_icon_large, text="Exit", compound=tk.TOP, command=self.root.quit)
        self.exit_button.grid(row=0, column=3, padx=20, pady=20)


    def show_employee_operations(self):
        # Open a new window with employee operation buttons
        employee_window = tk.Toplevel(self.root)
        employee_window.title("Employee Operations")

        # Load small icons for each operation
        self.add_employee_icon = ImageTk.PhotoImage(Image.open("Images/add emp.png").resize((50, 50)))
        self.update_employee_icon = ImageTk.PhotoImage(Image.open("Images/Update emp.png").resize((50, 50)))
        self.delete_employee_icon = ImageTk.PhotoImage(Image.open("Images/Del emp.png").resize((50, 50)))
        self.show_employee_icon = ImageTk.PhotoImage(Image.open("Images/show emp.png").resize((50, 50)))

        ttk.Button(employee_window, image=self.add_employee_icon, text="Add Employee", compound=tk.TOP, command=self.add_employee).grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(employee_window, image=self.update_employee_icon, text="Update Employee", compound=tk.TOP, command=self.update_employee).grid(row=0, column=1, padx=20, pady=20)
        ttk.Button(employee_window, image=self.delete_employee_icon, text="Delete Employee", compound=tk.TOP, command=self.delete_employee).grid(row=1, column=0, padx=20, pady=20)
        ttk.Button(employee_window, image=self.show_employee_icon, text="Show Employees", compound=tk.TOP, command=self.show_employees).grid(row=1, column=1, padx=20, pady=20)

    def show_department_operations(self):
        # Open a new window with department operation buttons
        department_window = tk.Toplevel(self.root)
        department_window.title("Department Operations")

        # Load small icons for each operation
        self.add_department_icon = ImageTk.PhotoImage(Image.open("Images/add dep.png").resize((50, 50)))
        self.delete_department_icon = ImageTk.PhotoImage(Image.open("Images/Del dep.png").resize((50, 50)))
        self.show_department_icon = ImageTk.PhotoImage(Image.open("Images/show dep.png").resize((50, 50)))

        ttk.Button(department_window, image=self.add_department_icon, text="Add Department", compound=tk.TOP, command=self.department_window).grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(department_window, image=self.delete_department_icon, text="Delete Department", compound=tk.TOP, command=self.delete_department_window).grid(row=0, column=1, padx=20, pady=20)
        ttk.Button(department_window, image=self.show_department_icon, text="Show Departments", compound=tk.TOP, command=self.show_departments).grid(row=1, column=0, padx=20, pady=20)

    def show_advanced_queries(self):
        # Open a new window with query operation buttons
        query_window = tk.Toplevel(self.root)
        query_window.title("Advanced Queries")

        # Load small icons for each query
        self.top_salaries_icon = ImageTk.PhotoImage(Image.open("Images/q1.png").resize((50, 50)))
        self.department_salary_icon = ImageTk.PhotoImage(Image.open("Images/q2.png").resize((50, 50)))
        self.highest_paid_icon = ImageTk.PhotoImage(Image.open("Images/q3.png").resize((50, 50)))
        self.same_salary_icon = ImageTk.PhotoImage(Image.open("Images/q4.png").resize((50, 50)))
        self.supervisor_salary_icon = ImageTk.PhotoImage(Image.open("Images/q5.png").resize((50, 50)))
        self.rank_salary_icon = ImageTk.PhotoImage(Image.open("Images/q6.png").resize((50, 50)))
        self.above_avg_salary_icon = ImageTk.PhotoImage(Image.open("Images/q7.png").resize((50, 50)))
        self.employee_count_icon = ImageTk.PhotoImage(Image.open("Images/q8.png").resize((50, 50)))
        self.department_avg_salary_icon = ImageTk.PhotoImage(Image.open("Images/q9.png").resize((50, 50)))
        self.employees_above_avg_icon = ImageTk.PhotoImage(Image.open("Images/q10.png").resize((50, 50)))

        # Create buttons for each query
        ttk.Button(query_window, image=self.top_salaries_icon, text="Top 10% Salaries", compound=tk.TOP, command=self.query_1).grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(query_window, image=self.department_salary_icon, text="Total Salary by Department", compound=tk.TOP, command=self.query_2).grid(row=0, column=1, padx=20, pady=20)
        ttk.Button(query_window, image=self.highest_paid_icon, text="Highest Paid by Department", compound=tk.TOP, command=self.query_3).grid(row=1, column=0, padx=20, pady=20)
        ttk.Button(query_window, image=self.same_salary_icon, text="Same Salary as Supervisor", compound=tk.TOP, command=self.query_4).grid(row=1, column=1, padx=20, pady=20)
        ttk.Button(query_window, image=self.supervisor_salary_icon, text="Supervisors with Salary and Department", compound=tk.TOP, command=self.query_5).grid(row=2, column=0, padx=20, pady=20)
        ttk.Button(query_window, image=self.rank_salary_icon, text="Rank Employees by Salary within Departments", compound=tk.TOP, command=self.query_6).grid(row=2, column=1, padx=20, pady=20)
        ttk.Button(query_window, image=self.above_avg_salary_icon, text="Departments with Above-Average Salaries", compound=tk.TOP, command=self.query_7).grid(row=3, column=0, padx=20, pady=20)
        ttk.Button(query_window, image=self.employee_count_icon, text="Employee Count by Department", compound=tk.TOP, command=self.query_8).grid(row=3, column=1, padx=20, pady=20)
        ttk.Button(query_window, image=self.department_avg_salary_icon, text="Salaries and Department Average", compound=tk.TOP, command=self.query_9).grid(row=4, column=0, padx=20, pady=20)
        ttk.Button(query_window, image=self.employees_above_avg_icon, text="Employees Above Department Average Salary", compound=tk.TOP, command=self.query_10).grid(row=4, column=1, padx=20, pady=20)





    def delete_department_window(self):
        # Create a new window for department deletion
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Department")

        # Fetch department names and corresponding IDs
        departments = self.get_department_list()

        if not departments:
            messagebox.showerror("Error", "No departments available.")
            return

        # Store the selected department (name, id) tuple
        self.selected_department = tk.StringVar()

        # Create a dropdown for departments (showing names)
        department_combobox = ttk.Combobox(delete_window, textvariable=self.selected_department)
        department_combobox['values'] = [dept[0] for dept in departments]  # Show department names
        department_combobox.grid(row=0, column=0, padx=10, pady=10)

        # Add a delete button
        delete_button = ttk.Button(delete_window, text="Delete Department", 
                                command=lambda: self.delete_department(department_combobox.get(), departments, delete_window))
        delete_button.grid(row=1, column=0, padx=10, pady=10)





    def refresh_employee_data(self):
        """Refresh the employee dropdown list."""
        self.supervisor_ids = read_employees(self.connection)
        self.supervisor_names = [f"{emp[1]} {emp[2]}" for emp in self.supervisor_ids]

    def refresh_department_data(self):
        # Method to refresh department data, populating self.department_list
        cursor = self.connection.cursor()
        cursor.execute("SELECT department_id FROM departments")  # Adjust to fetch department names if needed
        self.department_list = [row[0] for row in cursor.fetchall()]  # Assuming the first column is the department ID
        self.department_combobox['values'] = self.department_list  # Update the combobox with new values

		
	# Add Employee
    def add_employee(self):
        self.employee_window("Add Employee", self.create_employee_callback)
		
		
    # Update Employee
    def update_employee(self):
        # Create a new window for updating an employee
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Employee")

        frame = ttk.Frame(update_window)
        frame.pack(padx=20, pady=20)

        # Fetch employee names and corresponding IDs
        employees = read_employees(self.connection)

        if not employees:
            messagebox.showerror("Error", "No employees available.")
            return

        # Extract employee full names and IDs for the dropdown
        employee_names = [f"{emp[1]} {emp[2]}" for emp in employees]
        employee_ids = [emp[0] for emp in employees]

        # Label for selecting an employee
        ttk.Label(frame, text="Select Employee:").grid(row=0, column=0, padx=10, pady=10)

        # Employee dropdown
        self.selected_employee = tk.StringVar()
        employee_combobox = ttk.Combobox(frame, textvariable=self.selected_employee, values=employee_names)
        employee_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Button to proceed to update
        update_button = ttk.Button(frame, text="Next", command=lambda: self.populate_update_fields(employee_combobox.get(), employees, update_window))
        update_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def populate_update_fields(self, selected_employee_name, employees, update_window):
        # Find the selected employee's ID and data based on the name
        selected_employee_data = None
        for emp in employees:
            if f"{emp[1]} {emp[2]}" == selected_employee_name:
                selected_employee_data = emp
                break

        if selected_employee_data is None:
            messagebox.showerror("Error", "No employee selected.")
            return

        # Destroy the selection window
        update_window.destroy()

        # Open a new window for updating employee details with employee data
        self.employee_window("Update Employee", 
                            lambda *args: self.update_employee_callback(selected_employee_data[0], *args),
                            update=True, 
                            employee_data=selected_employee_data)

		
		
    def delete_employee(self):
        employee_id = self.select_employee()  # This function should return the selected employee's ID
        if employee_id:  # Ensure that an employee was actually selected and it's not empty or None
            try:
                delete_employee(self.connection, int(employee_id))  # Call to delete the employee
                self.refresh_employee_data()  # Refresh the employee dropdown data
                #self.show_employees()  # Show updated employee list
            except ValueError:
                messagebox.showerror("Error", "Invalid employee ID. Please select a valid employee.")
        else:
            messagebox.showinfo("Action Canceled", "No employee selected.")


			
    # Add Department
    def add_department(self, name):
        cursor = self.connection.cursor()
        try:
            # Update the query to use the correct column name "name"
            cursor.execute("INSERT INTO departments (name) VALUES (%s)", (name,))
            self.connection.commit()
            messagebox.showinfo("Success", f"Department '{name}' added successfully.")  # Success message
            return True  # Success
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return False  # Failure


    def delete_department(self, name, departments, delete_window):
        department_id = None
        for dept_name, dept_id in departments:
            if dept_name == name:
                department_id = dept_id
                break

        if department_id is None:
            messagebox.showerror("Error", "Invalid department selected.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM employees WHERE department_id = %s", (department_id,))
            employee_count = cursor.fetchone()[0]

            if employee_count > 0:
                messagebox.showerror("Error", f"Cannot delete department '{name}': it has {employee_count} associated employees.")
            else:
                cursor.execute("DELETE FROM departments WHERE department_id = %s", (department_id,))
                self.connection.commit()
                messagebox.showinfo("Success", f"Department '{name}' deleted successfully.")
                delete_window.destroy()  # Close the delete window after success
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while deleting the department.")
            print(f"Error: {e}")

    def get_department_list(self):
        """
        Fetch the list of departments from the database. 
        Returns a list of tuples [(name, department_id)].
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, department_id FROM departments")
        departments = cursor.fetchall()  # Fetch all department names and their IDs
        return departments


    # Show Employees
    def show_employees(self):
        # Create a new window for filtering employees
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Employees")

        # Create a frame for the form
        frame = ttk.Frame(filter_window)
        frame.pack(padx=20, pady=20)

        # Fetch the department list
        departments = read_departments(self.connection)
        department_names = [dept[1] for dept in departments]

        # Fetch the list of supervisors
        supervisors = [emp for emp in read_employees(self.connection) if emp[5] is None]
        supervisor_names = [f"{sup[1]} {sup[2]}" for sup in supervisors]

        # Department Dropdown
        dept_label = ttk.Label(frame, text="Select Department:")
        dept_label.grid(row=0, column=0, padx=10, pady=10)
        dept_combobox = ttk.Combobox(frame, values=department_names)
        dept_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Supervisor Dropdown
        supervisor_label = ttk.Label(frame, text="Select Supervisor:")
        supervisor_label.grid(row=1, column=0, padx=10, pady=10)
        supervisor_combobox = ttk.Combobox(frame, values=supervisor_names)
        supervisor_combobox.grid(row=1, column=1, padx=10, pady=10)

        def filter_and_show_employees():
            # Get the selected department and supervisor
            selected_department = dept_combobox.get()
            selected_supervisor = supervisor_combobox.get()

            # Find the selected department ID and supervisor ID
            department_id = None
            supervisor_id = None
            for dept in departments:
                if dept[1] == selected_department:
                    department_id = dept[0]
                    break

            for sup in supervisors:
                if f"{sup[1]} {sup[2]}" == selected_supervisor:
                    supervisor_id = sup[0]
                    break

            # Build a SQL query based on the selected filters
            query = """
                SELECT e.employee_id, e.first_name, e.last_name, d.name AS department_name, e.salary, e.supervisor_id 
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.department_id
                WHERE 1=1
            """
            query_params = []

            if department_id:
                query += " AND e.department_id = %s"
                query_params.append(department_id)

            if supervisor_id:
                query += " AND e.supervisor_id = %s"
                query_params.append(supervisor_id)

            # Execute the query with the filters
            cursor = self.connection.cursor()
            cursor.execute(query, query_params)
            rows = cursor.fetchall()

            # Show filtered results in a table
            self.show_table(rows, ["ID", "First Name", "Last Name", "Department Name", "Salary", "Supervisor ID"])

            # Close the filter window
            filter_window.destroy()

        # Submit Button to show filtered employees
        filter_button = ttk.Button(frame, text="Show Employees", command=filter_and_show_employees)
        filter_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Reset Filters Button (Optional)
        reset_button = ttk.Button(frame, text="Reset Filters", command=lambda: [dept_combobox.set(''), supervisor_combobox.set('')])
        reset_button.grid(row=3, column=0, columnspan=2, pady=10)




    # Show Departments
    def show_departments(self):
        rows = read_departments(self.connection)
        self.show_table(rows, ["Dept ID", "Department Name"])

    # Advanced Queries
    def advanced_queries(self):
        query_window = tk.Toplevel(self.root)
        query_window.title("Advanced Queries")
        query_frame = ttk.Frame(query_window)
        query_frame.pack(padx=20, pady=20)

        # Button for Query 1: Top 10% Salaries
        query_1_button = ttk.Button(query_frame, text="Top 10% Salaries", command=self.query_1)
        query_1_button.grid(row=0, column=0, padx=10, pady=10)

        # Button for Query 2: Total Salary by Department
        query_2_button = ttk.Button(query_frame, text="Total Salary by Department", command=self.query_2)
        query_2_button.grid(row=1, column=0, padx=10, pady=10)

        # Button for Query 3: Highest Paid by Department
        query_3_button = ttk.Button(query_frame, text="Highest Paid by Department", command=self.query_3)
        query_3_button.grid(row=2, column=0, padx=10, pady=10)

        # Button for Query 4: Same Salary as Supervisor
        query_4_button = ttk.Button(query_frame, text="Same Salary as Supervisor", command=self.query_4)
        query_4_button.grid(row=3, column=0, padx=10, pady=10)

        # Button for Complex Query 5: Show Supervisors with Name, Salary, and Department
        query_5_button = ttk.Button(query_frame, text="Supervisors with Salary and Department", command=self.query_5)
        query_5_button.grid(row=4, column=0, padx=10, pady=10)

        # Button for Complex Query 6: Employees in Departments 1, 2 & 3
        query_6_button = ttk.Button(query_frame, text="Rank Employees by Salary within Departments", command=self.query_6)
        query_6_button.grid(row=5, column=0, padx=10, pady=10)

        # Button for Complex Query 7: Departments with Above Average Salary
        query_7_button = ttk.Button(query_frame, text="Departments with Above-Average Salaries", command=self.query_7)
        query_7_button.grid(row=6, column=0, padx=10, pady=10)

        # Button for Complex Query 8: Employee Count by Department
        query_8_button = ttk.Button(query_frame, text="Employee Count by Department", command=self.query_8)
        query_8_button.grid(row=7, column=0, padx=10, pady=10)

        # Button for Complex Query 9: Salaries and Department Average
        query_9_button = ttk.Button(query_frame, text="Salaries and Department Average", command=self.query_9)
        query_9_button.grid(row=8, column=0, padx=10, pady=10)

        # Button for Complex Query 10: Employees Above Department Average Salary
        query_10_button = ttk.Button(query_frame, text="Employees Above Department Average Salary", command=self.query_10)
        query_10_button.grid(row=9, column=0, padx=10, pady=10)


    # Callback functions for employee and department actions
    def create_employee_callback(self, first_name, last_name, department_id, salary, supervisor_id):
        create_employee(self.connection, first_name, last_name, department_id, salary, supervisor_id)
        # Refresh employee data after adding a new employee
        self.refresh_employee_data()
		
    def update_employee_callback(self, employee_id, first_name, last_name, department_id, salary, supervisor_id):
        update_employee(self.connection, employee_id, first_name, last_name, department_id, salary, supervisor_id)
        # Refresh employee data after updating an employee
        self.refresh_employee_data()
		
    def create_department_callback(self, name):
        create_department(self.connection, name)
        # Refresh department data after adding a new department
        self.refresh_department_data()
		
    # Employee Input Window
    def employee_window(self, title, callback, update=False, employee_data=None):
        emp_window = tk.Toplevel(self.root)
        emp_window.title(title)

        frame = ttk.Frame(emp_window)
        frame.pack(padx=20, pady=20)

        # If updating, pre-populate the fields with the employee's data
        first_name = employee_data[1] if update and employee_data else ""
        last_name = employee_data[2] if update and employee_data else ""
        department_name = employee_data[3] if update and employee_data else ""
        salary = employee_data[4] if update and employee_data else ""
        supervisor_id = employee_data[5] if update and employee_data else None

        # First Name
        ttk.Label(frame, text="First Name:").grid(row=1, column=0, padx=10, pady=10)
        first_name_entry = ttk.Entry(frame)
        first_name_entry.grid(row=1, column=1, padx=10, pady=10)
        first_name_entry.insert(0, first_name)

        # Last Name
        ttk.Label(frame, text="Last Name:").grid(row=2, column=0, padx=10, pady=10)
        last_name_entry = ttk.Entry(frame)
        last_name_entry.grid(row=2, column=1, padx=10, pady=10)
        last_name_entry.insert(0, last_name)

        # Department Dropdown
        dept_label = ttk.Label(frame, text="Department (Choose from the List):")
        dept_label.grid(row=3, column=0, padx=10, pady=10)
        self.department_ids = read_departments(self.connection)
        self.department_names = [dept[1] for dept in self.department_ids]
        dept_combobox = ttk.Combobox(frame, values=self.department_names)
        dept_combobox.grid(row=3, column=1, padx=10, pady=10)
        # Pre-fill the department name
        if department_name:
            dept_combobox.set(department_name)  # Set the department name directly

        # Salary
        salary_label = ttk.Label(frame, text="Salary (Should be a number):")
        salary_label.grid(row=4, column=0, padx=10, pady=10)
        salary_entry = ttk.Entry(frame)
        salary_entry.grid(row=4, column=1, padx=10, pady=10)
        salary_entry.insert(0, salary)

        # Supervisor Dropdown
        supervisor_label = ttk.Label(frame, text="Supervisor (Choose from the List \nLeave blank for self-supervisor):")
        supervisor_label.grid(row=5, column=0, padx=10, pady=10)

        # Fetch the list of supervisors (employees with supervisor_id as None)
        self.supervisor_ids = [emp for emp in read_employees(self.connection) if emp[5] is None]
        self.supervisor_names = [f"{emp[1]} {emp[2]}" for emp in self.supervisor_ids]

        supervisor_combobox = ttk.Combobox(frame, values=self.supervisor_names)
        supervisor_combobox.grid(row=5, column=1, padx=10, pady=10)

        # Pre-select the supervisor if there is a supervisor_id
        if supervisor_id:
            supervisor_combobox.set(next((f"{emp[1]} {emp[2]}" for emp in self.supervisor_ids if emp[0] == supervisor_id), ""))


        def submit_employee():
            first_name_value = first_name_entry.get()
            last_name_value = last_name_entry.get()
            salary_value = salary_entry.get()

            # Validate that all required fields are filled
            if not all_fields_filled(first_name_value, last_name_value, salary_value, dept_combobox.get()):
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return

            # Validate numeric input for salary
            if not validate_numeric_input(salary_value):
                messagebox.showerror("Input Error", "Salary must be a valid number.")
                return

            # Get selected department and supervisor IDs
            selected_department_index = dept_combobox.current()
            selected_supervisor_index = supervisor_combobox.current()
            department_id = self.department_ids[selected_department_index][0] if selected_department_index != -1 else None
            supervisor_id = self.supervisor_ids[selected_supervisor_index][0] if selected_supervisor_index != -1 else None

            # Call the callback function (either create or update the employee)
            callback(
                first_name_value,
                last_name_value,
                department_id,
                salary_value,
                supervisor_id
            )
            emp_window.destroy()

        submit_button = ttk.Button(frame, text="Submit", command=submit_employee)
        submit_button.grid(row=6, column=1, padx=10, pady=10)



    # Department Input Window
    def department_window(self):
        dept_window = tk.Toplevel(self.root)
        dept_window.title("Add Department")

        frame = ttk.Frame(dept_window)
        frame.pack(padx=20, pady=20)

        dept_name_label = ttk.Label(frame, text="Department Name:")
        dept_name_label.grid(row=0, column=0, padx=10, pady=10)
        dept_name_entry = ttk.Entry(frame)
        dept_name_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit_department():
            department_name = dept_name_entry.get()
            if department_name:
                self.add_department(department_name)  # Call the add_department method with the input name
                dept_window.destroy()  # Close the window after the department is added
            else:
                messagebox.showerror("Error", "Department name cannot be empty.")

        submit_button = ttk.Button(frame, text="Submit", command=submit_department)
        submit_button.grid(row=1, column=1, padx=10, pady=10)


    # Query 1
    def query_1(self):
        try:
            rows = complex_query_1(self.connection)
            self.show_table(rows, ["First Name", "Last Name", "Salary"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Query 2
    def query_2(self):
        try:
            rows = complex_query_2(self.connection)
            self.show_table(rows, ["Department", "Total Salary Expenditure"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Query 3
    def query_3(self):
        try:
            rows = complex_query_3(self.connection)
            self.show_table(rows, ["Department", "First Name", "Last Name", "Salary"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Query 4
    def query_4(self):
        try:
            rows = complex_query_4(self.connection)
            self.show_table(rows, ["Employee First Name", "Employee Last Name", "Supervisor First Name", "Supervisor Last Name", "Salary"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_5(self):
        try:
            rows = complex_query_5(self.connection)
            self.show_table(rows, ["Supervisor First Name", "Supervisor Last Name", "Salary", "Department"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_6(self):
        try:
            rows = complex_query_6(self.connection)
            self.show_table(rows, ["First Name", "Last Name","Salary", "Department", "Salary Rank"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_7(self):
        try:
            rows = complex_query_7(self.connection)
            self.show_table(rows, ["Department Name", "Department Average Salary", "Total Average Salary"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_8(self):
        try:
            rows = complex_query_8(self.connection)
            self.show_table(rows, ["Department Name", "Employee Count"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_9(self):
        try:
            rows = complex_query_9(self.connection)
            self.show_table(rows, ["First Name", "Last Name", "Salary","Department Name", "Avg Dept Salary"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def query_10(self):
        try:
            rows = complex_query_10(self.connection)
            self.show_table(rows, ["Department Name", "First Name", "Last Name", "Salary"])
        except Exception as e:
            messagebox.showerror("Error", str(e))


    # Utility functions
    def show_table(self, rows, headers):
        table_window = tk.Toplevel(self.root)
        table_window.title("Results")
        frame = ttk.Frame(table_window)
        frame.pack(padx=20, pady=20)

        tree = ttk.Treeview(frame, columns=headers, show="headings")
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor=tk.CENTER, width=150)

        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.pack()

    def select_employee(self):
        employees = read_employees(self.connection)  # Fetch all employees
        employee_window = tk.Toplevel(self.root)
        employee_window.title("Select Employee")
        frame = ttk.Frame(employee_window)
        frame.pack(padx=20, pady=20)

        employee_id_var = tk.StringVar()

        for employee in employees:
            ttk.Radiobutton(
                frame, text=f"{employee[0]}: {employee[1]} {employee[2]}",
                variable=employee_id_var, value=str(employee[0])
            ).pack(anchor=tk.W)

        def submit():
            employee_id = employee_id_var.get()
            if employee_id:
                employee_window.destroy()
                return employee_id  # Return the selected employee ID
            else:
                messagebox.showerror("Error", "Please select an employee.")
                employee_window.destroy()
                return None

        submit_button = ttk.Button(frame, text="Submit", command=submit)
        submit_button.pack(pady=10)

        employee_window.wait_window()  # Wait for the window to close before returning
        return employee_id_var.get()  # Return the selected employee ID


    def select_department(self):
        departments = read_departments(self.connection)  # Fetch all departments
        department_window = tk.Toplevel(self.root)
        department_window.title("Select Department")
        frame = ttk.Frame(department_window)
        frame.pack(padx=20, pady=20)

        department_id_var = tk.StringVar()

        for department in departments:
            ttk.Radiobutton(
                frame, text=f"{department[0]}: {department[1]}",
                variable=department_id_var, value=str(department[0])
            ).pack(anchor=tk.W)

        def submit():
            department_id = department_id_var.get()
            if department_id:
                department_window.destroy()
                return department_id  # Return the selected department ID
            else:
                messagebox.showerror("Error", "Please select a department.")
                department_window.destroy()
                return None

        submit_button = ttk.Button(frame, text="Submit", command=submit)
        submit_button.pack(pady=10)

# Initialize the application
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        root = tk.Tk()
        app = App(root, conn)
        root.mainloop()
        close_connection(conn)
