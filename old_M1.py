import sql
import rdl


# Common Database Configurations
CLIENT_NAME = "DemoReports"  # Mention Client name For RDL Properties
DataBase = 'DemoReportsDB'   # Shared between sql.py and rdl.py     --->  check dataBase name in sql server before execute
Start_Year = "2024"         # Common Year for both SQL and RDL scripts
Start_Month = "09.September"  # Common Month for both SQL and RDL scripts
Start_Date = "01092024"   # Common date for both SQL and RDL scripts

# SQL Server credentials (shared with sql.py)
server = 'HALLMARK2'  # Server name or IP address
username = 'sa'
password = 'New31298@'
database = DataBase  # Shared between sql.py and rdl.py 

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
REPORT_PASSWORD = "qL5R*MLO[h_S<26"
REPORT_SERVER_URL = "http://hallmark2/Reports"

# For .rds DataSource
NEW_DATA_SOURCE = "HALLMARK2"
database = "DemoReportsDB"  # Shared between sql.py and rdl.py

if __name__ == "__main__":
    # Execute sql.py first
    sql.execute_sql_scripts(server, username, password, database, SQL_BASE_DIR, SQL_START_YEAR, SQL_START_MONTH, SQL_START_DATE)
    
    # Execute rdl.py after sql.py completes
    rdl.execute_rdl_deployment(
        RDL_BASE_DIR, RDL_START_YEAR, RDL_START_MONTH, RDL_START_DATE, 
        CLIENT_NAME, VS_PATH, REPORT_USER, REPORT_PASSWORD, 
        REPORT_SERVER_URL, NEW_DATA_SOURCE, database
    )