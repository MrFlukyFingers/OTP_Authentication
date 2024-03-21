import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import random
import threading
import time

# Set your Twilio account SID and auth token
account_sid = "ACb0df8ce500e3a7ac500ce711b093513e"
auth_token = "54a0806d5da552f750417fa282b4822b"
client = Client(account_sid, auth_token)

class OTPVerification:
    def __init__(self, master):
        self.master = master
        self.master.title("OTP Verification")
        self.master.geometry("600x550")
        self.entered_correct_otp = False
        self.otp = None
        self.typing_otp = False
        self.create_widgets()
        self.send_otp()

    def create_widgets(self):
        self.otp_label = tk.Label(self.master, text="Enter OTP:")
        self.otp_label.pack()

        self.otp_entry = tk.Entry(self.master, state='disabled')
        self.otp_entry.pack()

        self.verify_button = tk.Button(self.master, text="Verify", command=self.verify_otp)
        self.verify_button.pack()

        self.countdown_label = tk.Label(self.master, text="")
        self.countdown_label.pack()

        self.output_window = tk.Text(self.master, height=1)
        self.output_window.pack()

        self.otp_entry.bind('<Return>', self.type_otp_callback)

    def type_otp_callback(self, event):
        entered_otp = self.otp_entry.get()
        if entered_otp == self.otp:
            self.entered_correct_otp = True
            self.countdown_label.config(text="OTP verified")
            self.stop_timer()
            self.otp_entry.config(state='normal')
            self.otp_entry.delete(0, tk.END)
        else:
            self.otp_entry.config(fg='red', state='normal')
            self.otp_entry.delete(0, tk.END)
            self.otp_entry.insert(tk.END, "Wrong OTP, try again")
            self.apply_text_timeout()

    def apply_text_timeout(self):
        self.typing_otp = True
        self.after(2000, self.normal_text)

    def normal_text(self):
        self.otp_entry.config(fg='black', state='normal')
        self.typing_otp = False

    def send_otp(self):
        # Extract the phone number (you can modify this part to get user input)
        phone_number = "+919996939729"  # Replace withthe actual phone number

        # Generate a random 6-digit OTP
        self.otp = str(random.randint(100000, 999999))

        # Send the OTP via Twilio
        try:
            client.messages.create(
                body=f"Your OTP is: {self.otp}",
                from_="+15642323430",
                to=phone_number
            )
            print(f"OTP sent to {phone_number}: {self.otp}")
        except Exception as e:
            print(f"Error sending OTP: {e}")

        # Display a message box
        messagebox.showinfo("OTP Sent", "An OTP has been sent to your phone number.")

        # Start the timer (2 minutes)
        self.start_timer()

    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.countdown_timer)
        self.timer_thread.start()

    
    def countdown_timer(self):
        remaining_time = 120
        while remaining_time > 0 and not self.entered_correct_otp and not self.typing_otp:
            time.sleep(1)
            remaining_time -= 1
            self.countdown_label.config(text=f"Time remaining: {remaining_time} seconds")
            self.master.update_idletasks()

        self.countdown_label.config(text="OTP expired")

    def verify_otp(self):
        self.otp_entry.config(state='normal')
        self.otp_entry.focus_set()

    def stop_timer(self):
        if self.timer_thread is not None and self.timer_thread.is_alive():
            self.timer_thread.join()
        self.countdown_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    otp_app = OTPVerification(root)
    root.mainloop()