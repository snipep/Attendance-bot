# 🤖 GreytHR Attendance Bot

**Automate your daily Punch In/Out routine seamlessly using Python & GitHub Actions.**

This project eliminates the repetitive task of logging into greytHR to mark attendance. It utilizes **Selenium** for browser automation and **GitHub Actions** to run the script on a schedule in the cloud.

> **✨ Key Benefit:** This runs **serverlessly**. You do not need to keep your laptop on or have your computer awake. GitHub's servers handle everything automatically.

---

## 🚀 Features

*   **100% Cloud-Based:** Runs on GitHub runners (Ubuntu). No local machine required.
*   **Smart Detection:** Automatically handles "Happy Birthday" popups or announcements that block buttons.
*   **Universal Button Search:** Dynamically finds "Sign In", "Sign Out", or "Web Punch" buttons regardless of HTML changes.
*   **Secure:** Credentials are stored in encrypted Repository Secrets, never in the code.
*   **Scheduled:** Pre-configured for standard office hours (e.g., 10:00 AM & 7:30 PM IST).

---

## 🛠️ Project Structure

```text
Attendance-bot/
├── .github/
│   └── workflows/
│       └── attendance.yml   # The schedule configuration
├── greytHR_punch.py         # The main automation script
└── README.md                # Documentation
```

---

## ⚙️ Setup Guide (3 Steps)

### Step 1: Create the Repository
1.  Create a new **Private** repository on GitHub.
2.  Upload the `greytHR_punch.py` file to the root of the repository.

### Step 2: Configure Secrets (Security)
*Never hardcode passwords in the script.*
1.  Go to your Repository **Settings** tab.
2.  On the left sidebar, click **Secrets and variables** > **Actions**.
3.  Click **New repository secret** and add the following three secrets:

| Name | Value |
| :--- | :--- |
| `GREYTHR_URL` | `https://yourcompany.greythr.com/` |
| `GREYTHR_USER` | `Your Employee ID` |
| `GREYTHR_PASS` | `Your Password` |

### Step 3: Set the Schedule (GitHub Actions)
1.  In your repository, click **Add file** > **Create new file**.
2.  Name the file exactly: `.github/workflows/attendance.yml`
3.  Paste the following configuration:

```yaml
name: GreytHR Auto Punch

on:
  schedule:
    # ⚠️ TIMEZONE NOTE: GitHub uses UTC time. 
    # IST is UTC + 5:30.
    
    # Morning Punch: 10:00 AM IST (04:30 UTC) - Mon to Fri
    - cron: '30 4 * * 1-5'
    
    # Evening Punch: 07:30 PM IST (14:00 UTC) - Mon to Fri
    - cron: '0 14 * * 1-5'

  # Allows manual trigger from Actions tab for testing
  workflow_dispatch:

jobs:
  punch-attendance:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: |
          pip install selenium webdriver-manager

      - name: Run Punch Script
        env:
          GREYTHR_URL: ${{ secrets.GREYTHR_URL }}
          GREYTHR_USER: ${{ secrets.GREYTHR_USER }}
          GREYTHR_PASS: ${{ secrets.GREYTHR_PASS }}
        run: python greytHR_punch.py
```

4.  Commit the file. The automation is now live!

---

## 🕒 How to Change the Time
GitHub Actions uses **Cron Syntax** in **UTC Time**.

To calculate your time:
1.  Go to [WorldTimeBuddy](https://www.worldtimebuddy.com/) or a converter.
2.  Convert your desired **IST** time to **UTC**.
3.  Update the `cron` line in `.github/workflows/attendance.yml`.

**Example:**
*   **Want:** 9:00 AM IST
*   **UTC:** 3:30 AM
*   **Cron:** `30 3 * * 1-5`

---

## 🧪 How to Test Manually
You don't have to wait for the schedule to see if it works.
1.  Go to the **Actions** tab in your repository.
2.  Click **GreytHR Auto Punch** on the left sidebar.
3.  Click the **Run workflow** button (blue button on the right).
4.  Wait ~1 minute. If it shows a Green Checkmark (✅), it worked!

---

## ⚠️ Disclaimer
This script is for educational purposes and personal automation.
*   **Policy Violation:** Automating attendance may violate your company's IT or HR policies. Use this at your own risk.
*   **Maintenance:** If greytHR updates their website structure significantly, the script may need updates.