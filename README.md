# Amazon Kids Plus Content Deactivator

Automatically deactivate all contents on the Amazon Kids parent dashboard using Selenium automation.

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Usage Examples](USAGE_EXAMPLES.md)** - Common scenarios and examples
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Customize for Amazon's website structure

## Overview

This Python script uses Selenium WebDriver to automate the process of unchecking all content items on the Amazon Kids parent dashboard. It:
- Logs into your Amazon account
- Navigates to the content management section
- Unchecks all checked content items
- Automatically scrolls down and clicks "Load More" buttons to reveal additional content
- Continues until all content is deactivated

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Amazon account with Kids+ subscription

## Installation

1. Clone this repository:
```bash
git clone https://github.com/devkuosi/amzn_kids_plus.git
cd amzn_kids_plus
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Amazon credentials:
```
AMAZON_EMAIL=your_email@example.com
AMAZON_PASSWORD=your_password
```

## Configuration

The `.env` file supports the following options:

| Variable | Description | Default |
|----------|-------------|---------|
| `AMAZON_EMAIL` | Your Amazon account email | Required |
| `AMAZON_PASSWORD` | Your Amazon account password | Required |
| `PAGE_LOAD_TIMEOUT` | Maximum time to wait for page loads (seconds) | 30 |
| `ELEMENT_WAIT_TIMEOUT` | Maximum time to wait for elements (seconds) | 10 |
| `HEADLESS` | Run browser in headless mode (true/false) | false |
| `MAX_ITERATIONS` | Maximum number of scroll/load iterations | 100 |
| `CHECKBOX_SELECTOR` | CSS selector for checkboxes to uncheck | `input[type="checkbox"]:checked` |
| `CONTENT_LINK_TEXT` | Text of link to content management page | Manage Content |

### Customizing Selectors

**IMPORTANT**: The default CSS selectors are generic and may not match Amazon's actual page structure. Before using this script:

1. Open Amazon Kids dashboard in Chrome
2. Right-click on a checkbox and select "Inspect"
3. Find the appropriate CSS selector for checked checkboxes
4. Update `CHECKBOX_SELECTOR` in your `.env` file

Example:
```bash
# If Amazon uses a custom checkbox class
CHECKBOX_SELECTOR=.content-item.selected input[type="checkbox"]
```

Similarly, if the "Manage Content" link text differs, update `CONTENT_LINK_TEXT` or modify the navigation logic in the script.

## Usage

Run the script:
```bash
python deactivate_content.py
```

The script will:
1. Open a Chrome browser window
2. Navigate to Amazon Kids dashboard
3. Log in with your credentials
4. Start unchecking all content items
5. Automatically handle pagination and lazy loading
6. Display progress in the console

### Running in Headless Mode

For running without a visible browser window:
```bash
# Set HEADLESS=true in .env, or run with environment variable
HEADLESS=true python deactivate_content.py
```

## Features

- **Automatic Login**: Handles Amazon login flow
- **Smart Scrolling**: Automatically scrolls to load more content
- **Load More Detection**: Finds and clicks various "Load More" button types
- **Error Handling**: Robust error handling for common Selenium issues
- **Progress Logging**: Real-time console output showing progress
- **Safe Limits**: Prevents infinite loops with iteration limits
- **Stale Element Handling**: Handles dynamic page updates gracefully

## Logging

The script provides detailed logging output:
- INFO: General progress updates
- WARNING: Non-critical issues
- ERROR: Critical errors with stack traces

## Troubleshooting

### Login Issues
- Ensure your credentials in `.env` are correct
- Amazon may require two-factor authentication - handle this manually if needed
- Check if you need to solve a CAPTCHA

### Element Not Found
- The Amazon Kids dashboard may have changed its layout
- You may need to update the CSS selectors in the script
- Use browser DevTools to inspect the current page structure

### ChromeDriver Issues
- The script uses `webdriver-manager` to automatically download ChromeDriver
- Ensure you have Chrome browser installed
- Check that your Chrome version is compatible

## Customization

To adapt the script to changes in Amazon's website structure, you may need to modify:

1. **Login selectors** (lines ~75-100): Update element IDs if login form changes
2. **Checkbox selectors** (line ~130): Modify CSS selector for checkboxes
3. **Load More buttons** (lines ~200-210): Add new button selectors if needed

## Security Notes

- **Never commit your `.env` file** with real credentials
- The `.env` file is already in `.gitignore`
- Consider using a password manager or environment variables for credentials
- Use at your own risk - automated scripts may violate Amazon's terms of service

## Disclaimer

This script is provided for educational purposes. Automated interaction with websites may violate their Terms of Service. Use responsibly and at your own risk.

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.