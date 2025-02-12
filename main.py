import sql
import rdl

# Define the engine to specify which scripts to run
engine = ("sql","rdl")  # Options: ("sql", "rdl"), ("sql"), ("rdl")

# Common Database Configurations
CLIENT_NAME = "DemoReports2"  # Mention Client name For RDL Properties
DataBase = 'DemoReports2DB'   # Shared between sql.py and rdl.py     --->  check dataBase name in sql server before execute
Start_Year = "2024"         # Common Year for both SQL and RDL scripts
Start_Month = "09.September"  # Common Month for both SQL and RDL scripts
Start_Date = "01092024"   # Common date for both SQL and RDL scripts

# SQL Server credentials (shared with sql.py)
server = 'HALLMARK2'  # Server name or IP address
username = 'sa'
password = 'New31298@'
database_sql = DataBase  # Shared between sql.py and rdl.py  or You can give DataBase name manually 

# SQL Script Directory (GitLab repo location)   & you can manually edit the year, month, date
SQL_BASE_DIR = r"C:\Users\bhargavhallmark\database automation\database-automation\sqls"
SQL_START_YEAR = Start_Year
SQL_START_MONTH = Start_Month
SQL_START_DATE = Start_Date

# RDL Deployment constants (shared with rdl.py)  & you can manually edit the year, month, date
RDL_BASE_DIR = r"C:\Users\bhargavhallmark\database automation\database-automation\rdls"
RDL_START_YEAR = Start_Year
RDL_START_MONTH = Start_Month
RDL_START_DATE = Start_Date

VS_PATH = r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"

REPORT_USER = "bhargavhallmark"
REPORT_PASSWORD = "|#a(F~Ox{Quw4~{"
REPORT_SERVER_URL = "http://hallmark2/Reports"

# For .rds DataSource
NEW_DATA_SOURCE = "HALLMARK2"
database_rdl = DataBase  # Shared between sql.py and rdl.py or You can give DataBase name manually for catlog Shared DataSource

if __name__ == "__main__":
    # Execute sql.py if "sql" is in the engine
    if "sql" in engine:
        print("Executing SQL scripts...")
        sql.execute_sql_scripts(server, username, password, database_sql, SQL_BASE_DIR, SQL_START_YEAR, SQL_START_MONTH, SQL_START_DATE)
    else:
        print("Skipping SQL scripts (not in engine).")

    # Execute rdl.py if "rdl" is in the engine
    if "rdl" in engine:
        print("Executing RDL deployment...")
        rdl.execute_rdl_deployment(
            RDL_BASE_DIR, RDL_START_YEAR, RDL_START_MONTH, RDL_START_DATE, 
            CLIENT_NAME, VS_PATH, REPORT_USER, REPORT_PASSWORD, 
            REPORT_SERVER_URL, NEW_DATA_SOURCE, database_rdl
        )
    else:
        print("Skipping RDL deployment (not in engine).")