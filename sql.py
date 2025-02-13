import os
import pyodbc

def execute_sql_scripts(server, username, password, database, base_dir, start_year, start_month, start_date):
    # Connection string for SQL Server using pyodbc
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        # Connect to SQL Server
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("Connected to SQL Server successfully!")
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")
        exit()

    start_processing_year = False
    start_processing_month = False

    # Get all year folders sorted (e.g., "2024", "2025", "2026" ...)
    year_folders = sorted(os.listdir(base_dir))

    success_count = 0
    fail_count = 0
    paths_successful = []
    paths_failed = []

    for year_folder in year_folders:
        year_path = os.path.join(base_dir, year_folder)

        if not os.path.isdir(year_path):
            print(f"Skipping non-directory: {year_path}")
            continue  # Skip non-directory files

        if year_folder == start_year:
            start_processing_year = True  # Start processing from this year

        if not start_processing_year:
            print(f"Skipping year: {year_folder}")
            continue  # Skip years before the start year

        # Get all month folders in order (e.g., "01.January", "02.February" ...)
        month_folders = sorted(os.listdir(year_path))

        for month_folder in month_folders:
            month_path = os.path.join(year_path, month_folder)

            if not os.path.isdir(month_path):
                print(f"Skipping non-directory: {month_path}")
                continue  # Skip non-directory files

            if year_folder == start_year and month_folder == start_month:
                start_processing_month = True  # Start processing from this month

            if not start_processing_month:
                print(f"Skipping month: {month_folder}")
                continue  # Skip months before the start month in the first year

            # Get all date folders in order (e.g., "02012024", "05012024", "15012024" ...)
            date_folders = sorted(os.listdir(month_path))

            for date_folder in date_folders:
                date_path = os.path.join(month_path, date_folder)

                if not os.path.isdir(date_path):
                    print(f"Skipping non-directory: {date_path}")
                    continue  # Skip non-directory files

                if year_folder == start_year and month_folder == start_month and date_folder < start_date:
                    print(f"Skipping date: {date_folder} (before start date)")
                    continue  # Skip dates before the start date in the first month

                print(f"Executing scripts in: {date_path}")

                # Execute SQL files in order
                sql_files = sorted([f for f in os.listdir(date_path) if f.endswith(".sql")])
                if not sql_files:
                    print(f"No SQL files found in: {date_path}")
                    continue

                for sql_file in sql_files:
                    sql_file_path = os.path.join(date_path, sql_file)
                    print(f"Executing SQL file: {sql_file_path}")

                    try:
                        with open(sql_file_path, "r", encoding="utf-8") as f:
                            sql_script = f.read()
                            print(f"SQL Script Content:\n{sql_script}\n")

                        # Execute the SQL script
                        cursor.execute(sql_script)
                        conn.commit()
                        success_count += 1
                        paths_successful.append(sql_file_path)
                        print(f"Executed {sql_file} successfully")
                    except Exception as e:
                        conn.rollback()
                        fail_count += 1
                        paths_failed.append(sql_file_path)
                        print(f"Error executing {sql_file}: {e}")

    cursor.close()
    conn.close()
    print("Connection closed.")

    return success_count, fail_count, paths_successful, paths_failed