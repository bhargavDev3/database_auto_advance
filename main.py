import sql
import rdl
import pyttsx3
from log_utils import create_log_file, write_log, close_log_file

# Define the engine to specify which scripts to run
engine = ("sql", "rdl")  # Options: ("sql", "rdl"), ("sql"), ("rdl")
Date = "14/02/2024"  # Date for log file naming

# Common Database Configurations
CLIENT_NAME = "Raghu"  # Change this to the new client name
DataBase = 'RaghuDB'   # Shared between sql.py and rdl.py
Start_Year = "2024"         # Common Year for both SQL and RDL scripts
Start_Month = "09.September"  # Common Month for both SQL and RDL scripts
Start_Date = "01092024"   # Common date for both SQL and RDL scripts

# SQL Server credentials (shared with sql.py)
server = 'HALLMARK2'  # Server name or IP address
username = 'sa'
password = 'New31298@'
database_sql = DataBase  # Shared between sql.py and rdl.py

# SQL Script Directory (GitLab repo location)
SQL_BASE_DIR = r"C:\Users\bhargavhallmark\database automation\database-automation\sqls"
SQL_START_YEAR = Start_Year
SQL_START_MONTH = Start_Month
SQL_START_DATE = Start_Date

# RDL Deployment constants (shared with rdl.py)
RDL_BASE_DIR = r"C:\Users\bhargavhallmark\database automation\database-automation\rdls"
RDL_START_YEAR = Start_Year
RDL_START_MONTH = Start_Month
RDL_START_DATE = Start_Date

VS_PATH = r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"

REPORT_USER = "bhargavhallmark"
REPORT_PASSWORD = "t,}f^:oL^^ZF5^b"
REPORT_SERVER_URL = "http://hallmark2/Reports"

# For .rds DataSource
NEW_DATA_SOURCE = "HALLMARK2"
database_rdl = DataBase  # Shared between sql.py and rdl.py

# Initialize voice engine
Spell = pyttsx3.init()

# Function to play voice alert
def play_voice_alert(client_name):
    voice_message = f"Hi sir, The Deployment of {client_name} completed Successfully"
    Spell.setProperty('volume', 1)
    Spell.setProperty('rate', 125)
    Spell.say(voice_message)
    Spell.runAndWait()

if __name__ == "__main__":
    # Create the log file
    log_file = create_log_file(CLIENT_NAME, Date)  # Pass both CLIENT_NAME and Date

    # Counter for log entries
    s_no = 1

    # Execute sql.py if "sql" is in the engine
    if "sql" in engine:
        print("Executing SQL scripts...")

        # Execute SQL scripts
        success_count, fail_count, paths_successful, paths_failed = sql.execute_sql_scripts(server, username, password, database_sql, SQL_BASE_DIR, SQL_START_YEAR, SQL_START_MONTH, SQL_START_DATE)

        # Log SQL execution results
        write_log(log_file, s_no, "SQL", CLIENT_NAME, success_count, fail_count, paths_failed)
        s_no += 1

    # Execute rdl.py if "rdl" is in the engine
    if "rdl" in engine:
        print("Executing RDL deployment...")

        # Execute RDL deployment
        success_count, fail_count, paths_successful, paths_failed = rdl.execute_rdl_deployment(
            RDL_BASE_DIR, RDL_START_YEAR, RDL_START_MONTH, RDL_START_DATE, 
            CLIENT_NAME, VS_PATH, REPORT_USER, REPORT_PASSWORD, 
            REPORT_SERVER_URL, NEW_DATA_SOURCE, database_rdl
        )

        # Log RDL execution results
        write_log(log_file, s_no, "RDL", CLIENT_NAME, success_count, fail_count, paths_failed)
        s_no += 1

    # Close the log file
    close_log_file(log_file)

    # Play voice alert after deployment
    play_voice_alert(CLIENT_NAME)