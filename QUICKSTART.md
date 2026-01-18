# Quick Start Guide

Get started with Amazon Kids Plus Content Deactivator in 5 minutes!

## ⚡ Fast Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
# Edit .env and add your Amazon email and password

# 3. Validate setup
python3 validate_config.py

# 4. Run the script
python3 deactivate_content.py
```

## 📋 What You Need

- ✅ Python 3.7+
- ✅ Chrome browser
- ✅ Amazon account with Kids+
- ✅ 5 minutes

## ⚠️ Important Notes

### Before First Run

**The script uses default CSS selectors that may not match Amazon's current website structure.**

You will likely need to:
1. Inspect Amazon's actual page with Chrome DevTools
2. Update `CHECKBOX_SELECTOR` in your `.env` file
3. Update `CONTENT_LINK_TEXT` if the navigation link differs

See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for detailed instructions.

### Default Behavior

- **Browser Window**: Visible (HEADLESS=false)
- **Max Iterations**: 100 content load cycles
- **Timeouts**: 30s page load, 10s element wait

Change these in `.env` if needed.

## 🎯 Expected Behavior

When you run the script successfully:

1. **Chrome opens** and navigates to Amazon
2. **Logs in** with your credentials
3. **Navigates** to content management
4. **Finds checkboxes** and starts unchecking
5. **Scrolls down** automatically
6. **Clicks "Load More"** as needed
7. **Continues** until all content is deactivated
8. **Reports** total items unchecked

Console output example:
```
2026-01-18 10:00:00 - INFO - Setting up Chrome WebDriver...
2026-01-18 10:00:02 - INFO - WebDriver setup complete
2026-01-18 10:00:02 - INFO - Navigating to Amazon Kids parent dashboard...
2026-01-18 10:00:05 - INFO - Login submitted, waiting for dashboard...
2026-01-18 10:00:15 - INFO - Starting content deactivation process...
2026-01-18 10:00:15 - INFO - Maximum iterations set to: 100
2026-01-18 10:00:15 - INFO - Using checkbox selector: input[type="checkbox"]:checked
2026-01-18 10:00:15 - INFO - 
--- Iteration 1 ---
2026-01-18 10:00:15 - INFO - Found 20 checked items
2026-01-18 10:00:16 - INFO - Unchecked item 1
2026-01-18 10:00:16 - INFO - Unchecked item 2
...
2026-01-18 10:02:00 - INFO - Deactivation complete! Total items unchecked: 156
```

## 🔧 Troubleshooting

### "No checkboxes found with selector"

**Fix**: Update `CHECKBOX_SELECTOR` in `.env`

1. Open Amazon Kids dashboard in Chrome
2. Press F12 (DevTools)
3. Right-click a checkbox → Inspect
4. Find the correct CSS selector
5. Update `.env`: `CHECKBOX_SELECTOR=your-selector-here`

### "Could not find 'Manage Content' link"

**Fix**: Update `CONTENT_LINK_TEXT` in `.env`

1. Look at the actual link text on Amazon's page
2. Update `.env`: `CONTENT_LINK_TEXT=Your Link Text`

### "AMAZON_EMAIL and AMAZON_PASSWORD must be set"

**Fix**: Create `.env` file

```bash
cp .env.example .env
# Edit .env and add your credentials
```

### Script does nothing after login

**Fix**: The selectors probably don't match Amazon's structure

1. Run with `HEADLESS=false`
2. Watch what happens in the browser
3. Check console for warnings about selectors
4. Follow [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) to customize

## 📚 Next Steps

- **Read**: [README.md](README.md) for complete documentation
- **Examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for common scenarios
- **Customize**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for Amazon-specific setup
- **Test**: Run `python3 test_deactivate_content.py` to verify installation

## 🔒 Security

- ✅ Never commit your `.env` file
- ✅ Use strong, unique passwords
- ✅ Review Amazon's Terms of Service
- ✅ Keep dependencies updated

## 💡 Pro Tips

1. **First run**: Use `HEADLESS=false` to watch what happens
2. **Debugging**: Check logs for specific error messages
3. **Large libraries**: Increase `MAX_ITERATIONS` in `.env`
4. **Slow internet**: Increase timeout values in `.env`
5. **Automation**: Use cron/Task Scheduler for scheduled runs

## ❓ Need Help?

1. Check console output for errors
2. Run `python3 validate_config.py`
3. Review troubleshooting section above
4. Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
5. Open an issue on GitHub (without credentials!)

---

**Ready to start?** Run `python3 deactivate_content.py` and watch the magic happen! ✨
