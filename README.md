Security-Analysis-Tool
# Comprehensive Automated Server Log Analysis and Reporting Script with OpenAI

This Python script offers a fully automated solution for server log collection, cybersecurity analysis, and PDF reporting. It securely connects to your Linux-based server via SSH using the paramiko library to collect critical logs, including MariaDB logs, authentication logs, system logs, firewall logs, and web server logs (Apache and Nginx). The collected logs are then sent to OpenAI’s GPT-4 model for deep analysis, uncovering potential threats like brute-force attacks, SQL injections, and unauthorized access attempts.

The script uses FPDF to generate a professional PDF report summarizing the findings and delivers it via SMTP email to designated recipients. With cron job integration, this script ensures daily log analysis and reporting, helping administrators stay proactive about their server security posture.

# Key Features

- SSH-based Log Collection:
Collects logs from multiple services like authentication, MariaDB, system events, firewall, and web server logs (Apache and Nginx).

- OpenAI GPT-4 Analysis:
Leverages AI-powered analysis to detect anomalies, malicious activities, and security incidents.

- PDF Report Generation:
Summarizes analysis results into a professional PDF report using the FPDF library.

- Automated Email Delivery:
Sends the PDF report via SMTP email to administrators, ensuring seamless report delivery.

- MariaDB Integration:
Monitors MariaDB logs for suspicious queries, authentication failures, and SQL injections.

- Daily Automation with Cron Jobs:
Integrates with cron jobs to automate the entire process for daily log analysis.

- Security Best Practices:
Supports SSH key authentication and environment variable storage for sensitive credentials.
