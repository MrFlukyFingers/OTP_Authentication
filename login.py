import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import random
import threading
import time
import sys

# Set your Twilio account SID and auth token
account_sid = "AC1af84181181aa308c13232ba57673bc4"
auth_token = "6dcf974c469b0ce0670d391d6924c4ff"
client = Client(account_sid, auth_token)

# Set the expiration time for the OTP (in seconds)
expiration_time = 120

class OTPVerification:
    
    def __init__(self, master):
        self.master = master
        self.master.title("OTP Verification")
        self.master.geometry("600x400")
        self.otp = None
        self.timer_thread = None
        self.resend_timer = None
        self.verified = False  # Flag to indicate whether OTP has been verified
        self.label = tk.Label(master, text="OTP Verification", font=('calibre',20,'bold'))
        self.label.pack()
        self.otp_input = tk.StringVar()  # StringVar to store the entry value
        self.entry = tk.Entry(master, textvariable=self.otp_input, font=('calibre',10,'normal'))
        self.entry.pack()
        self.entry.focus_set()
        self.submit_button = tk.Button(master, text="Submit", command=self.store_value)
        self.submit_button.pack()


    # This function sends the OTP to User
    def send_otp(self, locked=False):
        if locked:
            messagebox.showinfo("Account Locked", "Your account is locked. Please contact support.")
        else:
            # Extract the phone number (you can modify this part to get user input)
            phone_number = "+919996939729"  # Replace with your phone number

            # Generate a random 6-digit OTP
            self.otp = str(random.randint(100000, 999999))

            # Send the OTP via Twilio
            try:
                client.messages.create(
                    body=f"Your OTP is: {self.otp}",
                    from_="+15642343867",
                    to=phone_number
                )
                print(f"OTP sent to {phone_number}: {self.otp}")
                # Start the timer (2 minutes)
                self.start_timer()
                # Display a message box
                messagebox.showinfo("OTP Sent", "An OTP has been sent to your phone number.")
                
            except Exception as e:
                print(f"Error sending OTP: {e}")

    # This Function start's the Timer of 2 mins
    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.countdown_timer)
        self.timer_thread.start()

    # This function prints the remaining time in the Terminal
    def countdown_timer(self):
        remaining_time = expiration_time
        while remaining_time > 0 and not self.verified:
            time.sleep(1)
            remaining_time -= 1
            print(f"Time remaining: {remaining_time} seconds")
        if not self.verified:
            print("OTP expired")
            sys.exit()  # Exit the program if OTP is not verified and the timer expires

    # This function checks if the correct OTP is entered
    def store_value(self):
        entered_otp = self.otp_input.get()  # Get the value from StringVar
        self.otp_input.set("")  # Clear the entry
        if entered_otp == self.otp:
            messagebox.showinfo("Verified User", "You entered the correct OTP")
            self.verified = True  # Set verified flag to True
            self.master.quit()  # Exit the Tkinter application
        else:
            messagebox.showerror("Error", "Incorrect OTP Entered")

if __name__ == "__main__":
    root = tk.Tk()
    otp_app = OTPVerification(root)
    otp_app.send_otp()  # You can call this method to send the OTP
    root.mainloop()
