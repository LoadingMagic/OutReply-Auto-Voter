## 📋 Features

- ✅ **Automatic IP Rotation** - Each vote uses a different residential IP.
- ✅ **Anti-Bot Bypass** - Uses undetected-chromedriver to avoid detection.
- ✅ **Headless Mode** - Runs completely in the background.
- ✅ **Configurable** - Easily customize votes, delays, and target options.
- ✅ **Fast Mode** - ~5-7 seconds per vote.
- ✅ **Progress Tracking** - Real-time statistics and logging.
- ✅ **Error Handling** - Automatic retry logic and detailed error logs.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Settings

Edit `auto_voter.py` and update the configuration section at the top:

```python
# ========== CONFIGURATION ==========
# Poll Settings
POLL_URL = "https://www.outreply.com/polls/YOUR_POLL_ID_HERE"
VOTE_OPTION = "Example"

# Proxy Settings
PROXY_USERNAME = "your_username__cr.us"
PROXY_PASSWORD = "your_password"
PROXY_HOST = "74.81.81.81"
PROXY_PORT = 823

# Vote Settings
NUMBER_OF_VOTES = 10
HEADLESS = True
FAST_MODE = True
DELAY_BETWEEN_VOTES = (1.0, 3.0)
# ===================================
```

### 3. Run the Bot

```bash
python auto_voter.py
```

### Proxy Settings

| Setting | Description | Format |
|---------|-------------|--------|
| `PROXY_USERNAME` | Proxy username with country code | `"username__cr.us"` |
| `PROXY_PASSWORD` | Proxy password | `"password123"` |
| `PROXY_HOST` | Proxy server IP address | `"74.81.81.81"` |
| `PROXY_PORT` | Proxy server port | `823` |

## 📊 Example Output

```
============================================================
🤖 AUTOMATED OUTREPLY VOTER
============================================================
Poll: https://www.outreply.com/polls/abc123
Voting For: Example
Total Votes: 10
Mode: HEADLESS (background)
============================================================

🎯 VOTE #1/2 - Session: auto-1-543210
✅ Vote #1 SUCCESSFUL!
⏳ Waiting 2.1s before next vote...

🎯 VOTE #2/2 - Session: auto-2-987654
✅ Vote #2 SUCCESSFUL!
⏳ Waiting 1.4s before next vote...

...

============================================================
📊 FINAL RESULTS
============================================================
Total Votes: 2
✅ Successful: 2
❌ Failed: 0
Success Rate: 100.0%
Total Time: 67.3s (1.1 minutes)
Average Time Per Vote: 6.7s
============================================================

🎉 ALL 10 VOTES SUCCESSFUL!
```

## 🔧 How It Works

1. **Session ID Generation** - Each vote gets a unique session ID for proxy rotation.
2. **Proxy Authentication** - Selenium-wire handles proxy authentication automatically.
3. **Page Load** - Browser navigates to poll URL using residential IP.
4. **Option Selection** - Finds the vote option by text match.
5. **Vote Submission** - Clicks the card and submit button.
6. **Verification** - Waits for server response and checks for success message.
7. **IP Rotation** - Next vote uses a completely different residential IP.

## 📁 File Structure

```
├── auto_voter.py          # Main script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔍 Finding Your Settings

### Finding the Poll URL

1. Open the poll in your browser.
2. Copy the full URL from the address bar.

### Finding the Vote Option Text

1. Open the poll page.
2. Right-click on the option you want to vote for.
3. Select "Inspect" or "Inspect Element".
4. Look for `<h5>` tag with the option text.
5. Copy the exact text (case-sensitive!).

Example HTML:
```html
<h5>Alien Update</h5>  ← Use "Alien Update"
```

### Vote 100 times

```python
NUMBER_OF_VOTES = 100
```

### Vote for different option

```python
VOTE_OPTION = "New Update Feature"
```

### Show browser window

```python
HEADLESS = False
```

### Slower, more human-like behavior

```python
FAST_MODE = False
DELAY_BETWEEN_VOTES = (3.0, 7.0)
```

### Different poll

```python
POLL_URL = "https://www.outreply.com/polls/different-poll-id"
VOTE_OPTION = "Your Option Here"
```

## 🐛 Troubleshooting

### Error: "Please configure POLL_URL"
- Edit `auto_voter.py`
- Replace `YOUR_POLL_ID_HERE` with your actual poll ID.

### Error: "Please configure proxy credentials"
- Edit `auto_voter.py`
- Replace placeholder proxy settings with your actual credentials.

### Error: "Could not find 'Your Option' option"
- Check spelling and capitalization (must match exactly).
- Inspect the page HTML to verify the exact text.
- Option text is case-sensitive!

### Votes failing / not saving
- Check proxy is working (view logs).
- Try reducing `NUMBER_OF_VOTES` to test.
- Set `HEADLESS = False` to watch what's happening.
- Check poll hasn't closed or changed.

### Proxy authentication errors
- Verify credentials are correct.
- Check proxy format: `username__cr.us:password@host:port`
- Ensure proxy service is active and has bandwidth.

## 📝 Log Files

Each run creates a timestamped log file:
```
auto_voter_20241126_191234.log
```

View logs to see detailed execution, errors, and timing information.

## ⚠️ Legal & Ethical Considerations

This tool is for:
- ✅ Testing anti-bot measures on YOUR OWN polls
- ✅ Stress testing poll infrastructure
- ✅ Educational purposes

Do NOT use for:
- ❌ Manipulating polls you don't own
- ❌ Fraudulent voting
- ❌ Violating terms of service

**Use responsibly and only on polls you have permission to test.**

## 🛠️ Requirements

- Python 3.8+
- Chrome browser installed
- Residential proxy service (DataImpulse or compatible)
- Windows, macOS, or Linux

## 📦 Dependencies

```
selenium-wire==5.1.0
undetected-chromedriver==3.5.4
selenium==4.15.2
blinker==1.6.2
```

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review log files for detailed error messages
3. Verify configuration settings are correct

## 📜 License

MIT License - Use at your own risk!!!!!

---

Bandwidth:  
100 MB ~ 25  
200 MB ~ 50  
500 MB ~ 120  
1 GB ~ 250  
2 GB ~ 500  
5 GB ~ 1,250  

**Made for testing anti-bot systems on OutReply polls** 🎯
