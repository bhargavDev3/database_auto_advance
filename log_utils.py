# log_utils.py
import os
import datetime

# Log file configuration
LOG_DIR = "logs"  # Logs will be saved in the "logs" directory inside the current directory
os.makedirs(LOG_DIR, exist_ok=True)

def create_log_file(client_name, date):
    """Creates a new log file with the given client name and date."""
    # Generate the base log file name
    base_log_file = f"{client_name}_{date.replace('/', '_')}.html"
    log_file = os.path.join(LOG_DIR, base_log_file)

    # Check if the log file already exists
    counter = 1
    while os.path.exists(log_file):
        # Append a suffix like "-2nd", "-3rd", etc.
        suffix = f"-{counter}nd" if counter == 2 else f"-{counter}rd" if counter == 3 else f"-{counter}th"
        log_file = os.path.join(LOG_DIR, f"{client_name}_{date.replace('/', '_')}{suffix}.html")
        counter += 1

    # Create the log file with the HTML structure
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Deployment Logs - {client_name} - {date}</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
        <style>
            .failed-link {{
                color: #ef4444;
                text-decoration: underline;
            }}
            .failed-link:hover {{
                color: #dc2626;
            }}
            .table-row:hover {{
                transform: scale(1.02);
                transition: transform 0.2s ease-in-out;
            }}
            .fade-in {{
                animation: fadeIn 0.5s ease-in;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>
    </head>
    <body class="bg-gradient-to-r from-blue-50 to-purple-50 p-8">
        <div class="max-w-6xl mx-auto bg-white shadow-2xl rounded-lg p-6 animate__animated animate__fadeIn">
            <h1 class="text-4xl font-bold text-center mb-8 text-gray-800 animate__animated animate__bounceIn">
                Deployment Logs - <span class="text-blue-600">{client_name}</span> - <span class="text-purple-600">{date}</span>
            </h1>
            <table class="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden shadow-lg">
                <thead class="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                    <tr>
                        <th class="py-4 px-6 text-left">S-No</th>
                        <th class="py-4 px-6 text-left">Date</th>
                        <th class="py-4 px-6 text-left">Execution Type</th>
                        <th class="py-4 px-6 text-left">Client-Name</th>
                        <th class="py-4 px-6 text-left">Successful</th>
                        <th class="py-4 px-6 text-left">Failed</th>
                        <th class="py-4 px-6 text-left">Paths_failed</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
    """
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    return log_file

def write_log(log_file, s_no, execution_type, client_name, successful, failed, paths_failed):
    """Writes a log entry to the log file."""
    # Format failed paths as clickable links
    failed_links = "<br>".join([f'<a href="{path}" class="failed-link">{path}</a>' for path in paths_failed])

    log_entry = f"""
    <tr class="table-row hover:bg-gray-50 fade-in">
        <td class="py-4 px-6 border-b">{s_no}</td>
        <td class="py-4 px-6 border-b">{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
        <td class="py-4 px-6 border-b">{execution_type}</td>
        <td class="py-4 px-6 border-b">{client_name}</td>
        <td class="py-4 px-6 border-b text-green-600 font-semibold">{successful}</td>
        <td class="py-4 px-6 border-b text-red-600 font-semibold">{failed}</td>
        <td class="py-4 px-6 border-b">{failed_links}</td>
    </tr>
    """
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)

def close_log_file(log_file):
    """Closes the log file by adding the closing HTML tags."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write("""
                </tbody>
            </table>
        </div>
    </body>
    </html>
        """)