# Automation-script

Service Monitor Script:
This Python script monitors the status of services running on specified servers, logs their availability, and sends email alerts if any service is not active or if a server becomes unreachable. It is designed to run as a lightweight monitoring tool for critical infrastructure.

Features:
Concurrently checks multiple servers using ThreadPoolExecutor.
Detects whether services are running or not via socket connection.
Sends HTML-formatted email alerts when:
A service is reported as not running.
A server is unreachable.
Logs all activity (success, failure, alerts) to a file.
Customizable server list, ports, and email recipients.

Requirements:
Python 3.8+
SMTP server access for sending emails
Network access to the monitored servers

