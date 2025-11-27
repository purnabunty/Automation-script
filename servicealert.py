#!/usr/bin/python3

import socket
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


# Configure logging
logging.basicConfig(filename='/home/CSSLNDL101/Script/servicemon.log',
#logging.basicConfig(filename='d:\\Script\\servicemon.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global dictionary to track last statuses
last_statuses = {}

def send_email(report_html, recipient_email):
    sender_email = "sender@gmail.com"
    subject = "CRITICAL: Service Alert"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(report_html, 'html'))

    try:
        smtp_server = "SMTP_Server1.iftas.in"  # Adjust with your SMTP server
        with smtplib.SMTP(smtp_server, 25) as server:
            server.send_message(msg)
            logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def get_server_status(server):
    server_port = 8420  # Adjusted to match your original port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)  # Set timeout for the socket
            client_socket.connect((server, server_port))
            combined_status = client_socket.recv(1024).decode("utf-8")

            # Normalize the combined status for comparison
            normalized_status = combined_status.strip().lower()
            #logging.info(f"Normalized status for {server}: '{normalized_status}'")  # Log normalized status

            # Split the status into lines and check each one
            lines = combined_status.splitlines()
            active_status_found = True
            status_report = []

            for line in lines:
                if "not running" in line.lower():
                    active_status_found = False
                status_report.append(line.strip())

            # Report of the current status
            report_status = "\n".join(status_report)

            # Send an alert if any process is not active
            if active_status_found:
                report_html = f'''
                <html>
                <head>
                <style>
                    table {{
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                    }}

                    td, th 
                    {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }}

                    tr:nth-child(even) {{
                    background-color: #dddddd;
                    }}

                    th.server, th.status {{
                    background-color: yellow;
                    color: blue;
                    }}
                </style>
                </head>
                <body>

                <h2>Alert: Service Not Active</h2>

                <table>
                    <tr>
                    <th class="server">Server</th>
                    <th class="status">Status</th>
                    </tr>
                    <tr>
                    <td>{server}</td>
                    <td>{report_status}</td>
                    </tr>
                </table>

                </body>
                </html>
                '''
                send_email(report_html, "Purna.raparthi@iftas.in")  # Replace with the appropriate recipient
                logging.info(f"Email sent for active server: {server}")
            else:
                logging.info(f"Service issue detected on {server}, but no email sent (testing mode)")

            return server, combined_status, False # Returning the original status for logging
    except Exception as e:
        logging.error(f"Error connecting to {server}: {e}")
        return server, f"Error connecting: {e}", True

def main():
    server_addresses = [
        'm-psg-ua-dwdb01',
        'm-css-ua-cbdb01',
        'm-pmg-pr-wind01',
        'm-psg-ua-rcdb01'
    ]
    all_statuses = {}
    unreachable_servers = []

    # Using ThreadPoolExecutor to fetch server statuses concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_server = {executor.submit(get_server_status, server): server for server in server_addresses}

        for future in as_completed(future_to_server):
            server, status = future.result()
            all_statuses[server] = status
            logging.info(f"Status for {server}: {status}")

            if unreachable:
                unreachable_servers.append(server)

    if unreachable_servers:
        report_html = f'''
        <html>
        <head>
        <style>
            table {{
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }}

            td, th 
            {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            }}

            tr:nth-child(even) {{
            background-color: #dddddd;
            }}

            th.server, th.status {{
            background-color: yellow;
            color: blue;
            }}
        </style>
        </head>
        <body>

        <h2>Alert: Unreachable Servers</h2>

        <table>
            <tr>
            <th class="server">Server</th>
            <th class="status">Status</th>
            </tr>
            <tr>
            <td>{server}</td>
            <td>{report_status}</td>
            </tr>
        </table>

        </body>
        </html>
        '''
    send_email(report_html, "raparthipurnarao11@gmail.com")

if __name__ == "__main__":
    main()

