import os
import re
import subprocess
import requests
from requests_ntlm import HttpNtlmAuth

def find_solution_files(folder_path):
    """Finds all .sln files in a given folder."""
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".sln")]

def find_rdl_files(folder_path):
    """Finds all .rdl files in the same directory as the .sln file."""
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".rdl")]

def update_rptproj_file(rptproj_path, client_name, report_server_url):
    """Updates the .rptproj file with correct report server paths."""
    try:
        with open(rptproj_path, 'r') as file:
            content = file.read()

        content = re.sub(r'<TargetReportFolder>.*?</TargetReportFolder>', 
                         f'<TargetReportFolder>/{client_name}/RDLS</TargetReportFolder>', content)
        content = re.sub(r'<TargetDatasourceFolder>.*?</TargetDatasourceFolder>', 
                         f'<TargetDatasourceFolder>/{client_name}/DS</TargetDatasourceFolder>', content)
        content = re.sub(r'<TargetServerURL>.*?</TargetServerURL>', 
                         f'<TargetServerURL>{report_server_url}</TargetServerURL>', content)

        with open(rptproj_path, 'w') as file:
            file.write(content)

        print(f"Updated: {rptproj_path}")
    except Exception as e:
        print(f"Error updating {rptproj_path}: {e}")

def update_rds_file(rds_path, new_data_source, DataBase):
    """Updates the .rds file with the new data source and catalog."""
    try:
        with open(rds_path, 'r') as file:
            content = file.read()

        content = re.sub(r'<ConnectString>Data Source=.*?;Initial Catalog=.*?</ConnectString>', 
                         f'<ConnectString>Data Source={new_data_source};Initial Catalog={DataBase}</ConnectString>', content)

        with open(rds_path, 'w') as file:
            file.write(content)

        print(f"Updated: {rds_path}")
    except Exception as e:
        print(f"Error updating {rds_path}: {e}")

def rebuild_and_deploy_solution(sln_path, vs_path):
    """Rebuilds and deploys the solution using Visual Studio's CLI."""
    if not os.path.exists(vs_path):
        print(f"Error: Visual Studio not found at {vs_path}")
        return False
    
    try:
        rebuild_command = [vs_path, sln_path, "/Rebuild", "Release"]
        rebuild_result = subprocess.run(rebuild_command, capture_output=True, text=True)

        if rebuild_result.returncode != 0:
            print("Solution rebuild failed!")
            print(rebuild_result.stderr)
            return False

        print("Solution rebuilt successfully.")

        deploy_command = [vs_path, sln_path, "/Deploy", "Release"]
        deploy_result = subprocess.run(deploy_command, capture_output=True, text=True)

        if deploy_result.returncode == 0:
            print("Deployment successful!")
            return True
        else:
            print("Deployment failed!")
            print(deploy_result.stderr)
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

def deploy_rdl_files(rdl_files, client_name, username, password, report_server_url):
    """Uploads RDL files to SSRS via HTTP PUT request."""
    success_count = 0
    fail_count = 0
    paths_successful = []
    paths_failed = []

    for rdl_file in rdl_files:
        report_name = os.path.basename(rdl_file).replace('.rdl', '')
        target_folder = f"/{client_name}/RDLS"
        url = f"{report_server_url}/browse/{client_name}/RDLS"
        headers = {'Content-Type': 'application/octet-stream'}
        params = {'TargetFolder': target_folder, 'Overwrite': 'true'}

        with open(rdl_file, 'rb') as file:
            try:
                response = requests.put(
                    url, headers=headers, params=params, data=file, 
                    auth=HttpNtlmAuth(username, password)
                )
                if response.status_code == 200:
                    success_count += 1
                    paths_successful.append(rdl_file)
                    print(f"Successfully deployed {report_name} to {target_folder}")
                else:
                    fail_count += 1
                    paths_failed.append(rdl_file)
                    print(f"Failed to deploy {report_name}: {response.status_code} - {response.text}")
            except Exception as e:
                fail_count += 1
                paths_failed.append(rdl_file)
                print(f"Error deploying {report_name}: {e}")

    return success_count, fail_count, paths_successful, paths_failed

def process_folder(folder_path, client_name, vs_path, report_server_url, new_data_source, database, report_user, report_password):
    """Processes all subdirectories inside a date folder for .sln files."""
    subfolders = sorted([os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))])
    
    success_count = 0
    fail_count = 0
    paths_successful = []
    paths_failed = []

    for subfolder in subfolders:
        sln_files = find_solution_files(subfolder)
        if not sln_files:
            continue

        for sln_file in sln_files:
            rdl_files = find_rdl_files(os.path.dirname(sln_file))

            print(f"Found Solution: {sln_file}")
            print(f"Found RDL Files: {len(rdl_files)}")

            rptproj_files = [os.path.join(subfolder, file) for file in os.listdir(subfolder) if file.endswith(".rptproj")]
            for rptproj_file in rptproj_files:
                update_rptproj_file(rptproj_file, client_name, report_server_url)

            rds_files = [os.path.join(subfolder, file) for file in os.listdir(subfolder) if file.endswith(".rds")]
            for rds_file in rds_files:
                update_rds_file(rds_file, new_data_source, database)

            if rebuild_and_deploy_solution(sln_file, vs_path):
                success, fail, paths_success, paths_fail = deploy_rdl_files(rdl_files, client_name, report_user, report_password, report_server_url)
                success_count += success
                fail_count += fail
                paths_successful.extend(paths_success)
                paths_failed.extend(paths_fail)

    return success_count, fail_count, paths_successful, paths_failed

def execute_rdl_deployment(base_dir, start_year, start_month, start_date, client_name, vs_path, report_user, report_password, report_server_url, new_data_source, database):
    """Processes all folders from START_YEAR/START_MONTH/START_DATE onward."""
    start_processing = False

    year_folders = sorted(os.listdir(base_dir))

    success_count = 0
    fail_count = 0
    paths_successful = []
    paths_failed = []

    for year_folder in year_folders:
        year_path = os.path.join(base_dir, year_folder)

        if not os.path.isdir(year_path):
            continue

        if year_folder == start_year:
            start_processing = True

        if not start_processing:
            continue

        month_folders = sorted(os.listdir(year_path))

        for month_folder in month_folders:
            month_path = os.path.join(year_path, month_folder)

            if not os.path.isdir(month_path):
                continue

            if year_folder == start_year and month_folder == start_month:
                start_processing = True

            if not start_processing:
                continue

            date_folders = sorted(os.listdir(month_path))

            for date_folder in date_folders:
                date_path = os.path.join(month_path, date_folder)

                if not os.path.isdir(date_path):
                    continue

                if year_folder == start_year and month_folder == start_month and date_folder == start_date:
                    start_processing = True

                if not start_processing:
                    continue

                print(f"Processing: {date_path}")
                success, fail, paths_success, paths_fail = process_folder(date_path, client_name, vs_path, report_server_url, new_data_source, database, report_user, report_password)
                success_count += success
                fail_count += fail
                paths_successful.extend(paths_success)
                paths_failed.extend(paths_fail)

    return success_count, fail_count, paths_successful, paths_failed