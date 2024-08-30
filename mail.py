import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json

def save_smtp_settings():
    smtp_info = {
        "server": smtp_entry.get(),
        "port": port_entry.get(),
        "username": username_entry.get(),
        "password": password_entry.get(),
    }
    with open("smtp_settings.json", "w") as f:
        json.dump(smtp_info, f)
    messagebox.showinfo("Başarılı", "SMTP bilgileri kaydedildi!")

def load_smtp_settings():
    try:
        with open("smtp_settings.json", "r") as f:
            smtp_info = json.load(f)
            smtp_entry.delete(0, tk.END)
            smtp_entry.insert(0, smtp_info['server'])
            port_entry.delete(0, tk.END)
            port_entry.insert(0, smtp_info['port'])
            username_entry.delete(0, tk.END)
            username_entry.insert(0, smtp_info['username'])
            password_entry.delete(0, tk.END)
            password_entry.insert(0, smtp_info['password'])
        messagebox.showinfo("Başarılı", "SMTP bilgileri yüklendi!")
    except FileNotFoundError:
        messagebox.showerror("Hata", "SMTP bilgileri bulunamadı.")

def send_email():
    progress['value'] = 0
    root.update_idletasks()
    
    try:
        smtp_server = smtp_entry.get()
        port = int(port_entry.get())
        username = username_entry.get()
        password = password_entry.get()

        sender = sender_entry.get()
        recipient = recipient_entry.get()
        subject = subject_entry.get()
        body = body_text.get("1.0", tk.END)

        body += f"\n\nSaygılarımla,\n{sender}"

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))

        if attachment_path.get():
            filename = os.path.basename(attachment_path.get())
            attachment = open(attachment_path.get(), "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)
        
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        
        progress['value'] = 50
        root.update_idletasks()
        
        server.sendmail(sender, recipient.split(','), text)
        server.quit()

        log_email(sender, recipient, subject)
        
        progress['value'] = 100
        root.update_idletasks()
        
        messagebox.showinfo("Başarılı", "E-posta başarıyla gönderildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"E-posta gönderilemedi: {str(e)}")

def log_email(sender, recipient, subject):
    with open("email_log.txt", "a") as log_file:
        log_file.write(f"Gönderen: {sender}, Alıcı: {recipient}, Konu: {subject}\n")

def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Dosya Seçin",
                                          filetypes=(("Tüm Dosyalar", "*.*"), ("Text files", "*.txt*"), ("PDF files", "*.pdf*")))
    attachment_path.set(filename)

root = tk.Tk()
root.title("E-posta Gönderme Uygulaması")
root.geometry("650x750")
root.configure(bg='#dfe6e9')

style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12), background='#dfe6e9')
style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=6)
style.configure('TEntry', font=('Helvetica', 12))

title_label = tk.Label(root, text="E-posta Gönderme Uygulaması", font=('Helvetica', 18, 'bold'), bg='#0984e3', fg='white', padx=20, pady=10)
title_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="ew")

ttk.Label(root, text="SMTP Sunucusu:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
smtp_entry = ttk.Entry(root, width=40)
smtp_entry.grid(row=1, column=1, pady=10, padx=10, columnspan=2)

ttk.Label(root, text="Port:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
port_entry = ttk.Entry(root, width=40)
port_entry.grid(row=2, column=1, pady=10, padx=10, columnspan=2)

ttk.Label(root, text="Kullanıcı Adı:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
username_entry = ttk.Entry(root, width=40)
username_entry.grid(row=3, column=1, pady=10, padx=10, columnspan=2)

ttk.Label(root, text="Şifre:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
password_entry = ttk.Entry(root, width=40, show="*")
password_entry.grid(row=4, column=1, pady=10, padx=10, columnspan=2)

save_button = tk.Button(root, text="SMTP Kaydet", command=save_smtp_settings, bg='#0984e3', fg='white', font=('Helvetica', 12, 'bold'), padx=10, pady=5)
save_button.grid(row=5, column=0, pady=10, padx=10)

load_button = tk.Button(root, text="SMTP Yükle", command=load_smtp_settings, bg='#74b9ff', fg='white', font=('Helvetica', 12, 'bold'), padx=10, pady=5)
load_button.grid(row=5, column=1, pady=10, padx=10)

ttk.Label(root, text="Gönderici E-posta:").grid(row=6, column=0, padx=10, pady=10, sticky='e')
sender_entry = ttk.Entry(root, width=40)
sender_entry.grid(row=6, column=1, pady=10, padx=10, columnspan=2)

ttk.Label(root, text="Alıcı E-posta:").grid(row=7, column=0, padx=10, pady=10, sticky='e')
recipient_entry = ttk.Entry(root, width=40)
recipient_entry.grid(row=7, column=1, pady=10, padx=10, columnspan=2)

ttk.Label(root, text="Konu Başlığı:").grid(row=8, column=0, padx=10, pady=10, sticky='e')
subject_entry = ttk.Entry(root, width=40)
subject_entry.grid(row=8, column=1, pady=10, padx=10, columnspan=2)

ttk.Label(root, text="E-posta İçeriği:").grid(row=9, column=0, padx=10, pady=10, sticky='ne')
body_text = tk.Text(root, width=55, height=10, font=('Helvetica', 12))
body_text.grid(row=9, column=1, pady=10, padx=10, columnspan=2)

attachment_path = tk.StringVar()
ttk.Label(root, text="Dosya Eki:").grid(row=10, column=0, padx=10, pady=10, sticky='e')
attachment_entry = ttk.Entry(root, textvariable=attachment_path, width=40)
attachment_entry.grid(row=10, column=1, pady=10, padx=10)
browse_button = tk.Button(root, text="Dosya Seç", command=browse_files, bg='#fdcb6e', fg='white', font=('Helvetica', 12, 'bold'), padx=10, pady=5)
browse_button.grid(row=10, column=2, pady=10, padx=10)

send_button = tk.Button(root, text="Gönder", command=send_email, bg='#00b894', fg='white', font=('Helvetica', 12, 'bold'), padx=10, pady=5)
send_button.grid(row=11, column=1, pady=20)

progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress.grid(row=12, column=0, columnspan=3, pady=10)

root.mainloop()
