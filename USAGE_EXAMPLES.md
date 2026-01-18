# Usage Examples

This document provides practical examples and common use cases for the Amazon Kids Plus Content Deactivator.

## Quick Start

### 1. First Time Setup

```bash
# Clone the repository
git clone https://github.com/devkuosi/amzn_kids_plus.git
cd amzn_kids_plus

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your favorite editor and add credentials
nano .env  # or vim, code, etc.

# Validate configuration
python3 validate_config.py
```

### 2. Run the Script

```bash
# Run with visible browser (recommended for first time)
python3 deactivate_content.py

# Run in headless mode (no browser window)
HEADLESS=true python3 deactivate_content.py
```

## Common Scenarios

### Scenario 1: Regular Content Deactivation

You want to disable all content for your child's profile on a regular basis.

```bash
# Run normally (you can watch the progress)
python3 deactivate_content.py
```

Expected output:
```
2026-01-18 10:00:00 - INFO - Setting up Chrome WebDriver...
2026-01-18 10:00:02 - INFO - WebDriver setup complete
2026-01-18 10:00:02 - INFO - Navigating to Amazon Kids parent dashboard...
2026-01-18 10:00:05 - INFO - Login page detected, entering credentials...
2026-01-18 10:00:10 - INFO - Login submitted, waiting for dashboard...
2026-01-18 10:00:15 - INFO - Starting content deactivation process...
2026-01-18 10:00:15 - INFO - 
--- Iteration 1 ---
2026-01-18 10:00:15 - INFO - Found 20 checked items
2026-01-18 10:00:16 - INFO - Unchecked item 1
...
```

### Scenario 2: Scheduled Automation

You want to run this automatically on a schedule (e.g., daily at midnight).

#### Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line to run daily at midnight
0 0 * * * cd /path/to/amzn_kids_plus && /usr/bin/python3 deactivate_content.py >> /tmp/amzn_kids_deactivate.log 2>&1
```

Make sure to set `HEADLESS=true` in your `.env` file for scheduled runs.

#### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create a new task
3. Set trigger to daily at your preferred time
4. Set action to run: `python.exe C:\path\to\amzn_kids_plus\deactivate_content.py`
5. Set start in directory: `C:\path\to\amzn_kids_plus`

### Scenario 3: Debugging Issues

If the script doesn't work as expected:

```bash
# 1. Validate your configuration
python3 validate_config.py

# 2. Run with visible browser to see what's happening
# Edit .env and set HEADLESS=false
python3 deactivate_content.py

# 3. Check the console output for errors
# The script provides detailed logging
```

### Scenario 4: Testing Without Real Credentials

To test the basic functionality without credentials:

```bash
# Run the unit tests
python3 test_deactivate_content.py

# This will validate the code logic without connecting to Amazon
```

## Advanced Usage

### Custom Timeouts

If you have a slow internet connection, increase the timeouts:

```bash
# Edit .env file
PAGE_LOAD_TIMEOUT=60
ELEMENT_WAIT_TIMEOUT=20
```

### Running in a Docker Container

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "deactivate_content.py"]
```

Build and run:

```bash
docker build -t amzn-kids-deactivator .
docker run --rm -v $(pwd)/.env:/app/.env amzn-kids-deactivator
```

## Troubleshooting

### "ChromeDriver not found"

The script uses `webdriver-manager` to automatically download ChromeDriver. If this fails:

```bash
# Manually install webdriver-manager
pip install --upgrade webdriver-manager

# Or download ChromeDriver manually from:
# https://chromedriver.chromium.org/
```

### "Element not found" Errors

Amazon's website structure may have changed. To fix:

1. Open the Amazon Kids dashboard in Chrome
2. Right-click and select "Inspect"
3. Find the checkbox elements
4. Update the selectors in `deactivate_content.py` (around line 130)

### Two-Factor Authentication

If your Amazon account uses 2FA:

1. Run the script in non-headless mode (`HEADLESS=false`)
2. Manually complete the 2FA when prompted
3. The script will continue after authentication

Alternatively, you can manually log in to Amazon in the same browser profile before running the script.

## Performance Tips

1. **Run during off-peak hours** - Faster page loads
2. **Use headless mode** - Slightly faster execution
3. **Increase iteration limits** - Modify `max_iterations` in the code if you have thousands of items
4. **Adjust delays** - Reduce `time.sleep()` values if you have fast internet (be careful not to overwhelm Amazon's servers)

## Security Best Practices

1. **Never share your .env file**
2. **Use a strong, unique password for Amazon**
3. **Consider using a dedicated Amazon account** for automation
4. **Review Amazon's Terms of Service** regarding automation
5. **Keep your dependencies updated** for security patches:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## Getting Help

If you encounter issues:

1. Check the console output for detailed error messages
2. Verify your configuration with `python3 validate_config.py`
3. Review the README.md for setup instructions
4. Open an issue on GitHub with:
   - Your Python version
   - Error messages (without credentials!)
   - Steps to reproduce
