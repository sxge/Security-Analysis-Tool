import openai
import paramiko
import os
from datetime import datetime
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# OpenAI API Key
openai.api_key = 'your-openai-api-key'

# SSH Configuration
HOST = 'your-server-ip'
USERNAME = 'username'
PASSWORD = 'password'

# Define logs to collect, including MariaDB
LOG_PATHS = [
    "/var/log/auth.log",           # Authentication logs
    "/var/log/syslog",             # System logs
    "/var/log/ufw.log",            # UFW firewall logs
    "/var/log/apache2/access.log", # Apache access logs
    "/var/log/nginx/access.log",   # Nginx access logs
    "/var/log/mysql/error.log",    # MySQL/MariaDB error logs
    "/var/log/fail2ban.log",       # Fail2Ban logs
    "/var/log/mariadb/mariadb.log", # MariaDB general logs
]

def ssh_collect_logs():
    """SSH into the server and collect multiple logs."""
    collected_logs = ""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USERNAME, password=PASSWORD)

        sftp = ssh.open_sftp()
        for log_path in LOG_PATHS:
            try:
                # Download each log to local machine
                log_filename = os.path.basename(log_path)
                sftp.get(log_path, log_filename)

                # Read and append log content
                with open(log_filename, 'r') as f:
                    collected_logs += f"\n--- {log_filename} ---\n"
                    collected_logs += f.read()
            except Exception as e:
                print(f"Failed to collect {log_path}: {e}")

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"SSH connection failed: {e}")

    return collected_logs

def analyze_logs_with_gpt(log_content):
    """Send collected logs to OpenAI API for analysis."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert."},
            {"role": "user", "content": f"Analyze these logs:\n{log_content}"}
        ]
    )
    return response.choices[0].message['content']

def generate_pdf_report(analysis, filename='daily_report.pdf'):
    """Generate a PDF report from the analysis."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Daily Cybersecurity Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=analysis)

    pdf.output(filename)
    print(f"Report saved as {filename}")

def send_email_report(to_address, pdf_filename):
    """Send the PDF report via email."""
    msg = MIMEMultipart()
    msg['From'] = 'your-email@example.com'
    msg['To'] = to_address
    msg['Subject'] = "Daily Cybersecurity Report"

    body = "Attached is the daily cybersecurity report."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_filename, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
        msg.attach(attach)

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your-email@example.com', 'your-password')
        server.send_message(msg)

    print(f"Email sent to {to_address}")

# Main workflow
if __name__ == "__main__":
    print("Collecting logs...")
    collected_logs = ssh_collect_logs()

    print("Analyzing logs with OpenAI...")
    analysis = analyze_logs_with_gpt(collected_logs)

    print("Generating PDF report...")
    generate_pdf_report(analysis)

    print("Sending email report...")
    send_email_report('recipient@example.com', 'daily_report.pdf')
