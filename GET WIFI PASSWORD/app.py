import subprocess
from flask import Flask, render_template

app = Flask(__name__)

def get_wifi_passwords():
    data = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8").split("\n")
    profiles = [line.split(":")[1][1:-1] for line in data if "All User Profile" in line]

    wifi_info = []
    for profile in profiles:
        try:
            results = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode("utf-8").split("\n")
            password_lines = [line for line in results if "Key Content" in line]
            password = password_lines[0].split(":")[1][1:-1] if password_lines else "🔒 Not Available"
            wifi_info.append({"profile": profile, "password": password})
        except subprocess.CalledProcessError:
            wifi_info.append({"profile": profile, "password": "❌ Error"})

    return wifi_info

@app.route('/')
def home():
    wifi_data = get_wifi_passwords()
    return render_template('index.html', wifi_data=wifi_data)

if __name__ == '__main__':
    app.run(debug=True)
