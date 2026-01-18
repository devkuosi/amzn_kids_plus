# Developer Guide: Customizing for Amazon's Website

This guide explains how to customize the script to work with Amazon's actual website structure.

## Prerequisites

- Basic understanding of HTML/CSS
- Chrome browser with DevTools
- Amazon Kids+ account

## Step-by-Step Customization

### 1. Identify the Checkbox Selector

1. **Navigate** to Amazon Kids parent dashboard and log in
2. **Open Chrome DevTools** (F12 or right-click → Inspect)
3. **Find a content item** with a checkbox
4. **Right-click on the checkbox** → Inspect
5. **Note the element structure**

Example scenarios:

**Scenario A**: Standard checkbox
```html
<input type="checkbox" checked class="content-checkbox">
```
Use selector: `input[type="checkbox"]:checked`

**Scenario B**: Custom checkbox component
```html
<div class="content-item selected">
  <input type="checkbox" checked>
</div>
```
Use selector: `.content-item.selected input[type="checkbox"]`

**Scenario C**: React/Vue component
```html
<label class="checkbox-wrapper">
  <input type="checkbox" checked data-checked="true">
</label>
```
Use selector: `input[type="checkbox"][data-checked="true"]`

6. **Update your .env file**:
```bash
CHECKBOX_SELECTOR=your-discovered-selector
```

### 2. Find the Content Management Link

1. **Look for the navigation link** to content management
2. **Inspect the link element**

Common variations:
- Link text: "Manage Content", "Content Library", "Parent Dashboard"
- Could be a button instead of a link
- Might require multiple navigation steps

3. **Update .env**:
```bash
CONTENT_LINK_TEXT=Your Actual Link Text
```

OR modify `navigate_to_content_management()` method in the script.

### 3. Identify Load More Button

1. **Scroll to bottom** of content list
2. **Find the "Load More" button**
3. **Inspect its structure**

Common patterns:
```html
<!-- Button with text -->
<button class="load-more-btn">Load More</button>

<!-- Link styled as button -->
<a class="pagination-link" href="#loadMore">Show More Results</a>

<!-- Infinite scroll with sentinel -->
<div class="loading-indicator"></div>
```

4. **Add new selectors** to `click_load_more_button()` method if needed:
```python
button_selectors = [
    (By.CSS_SELECTOR, "button.load-more-btn"),  # Your custom selector
    (By.XPATH, "//button[contains(text(), 'Load More')]"),
    # ... existing selectors
]
```

### 4. Testing Your Customizations

1. **Set HEADLESS=false** in .env to watch the automation
2. **Run the script**:
   ```bash
   python3 deactivate_content.py
   ```
3. **Watch for errors** in the console:
   - "No checkboxes found" → Update CHECKBOX_SELECTOR
   - "Could not find link" → Update CONTENT_LINK_TEXT
   - Script stops after first page → Check load more button logic

### 5. Common Issues and Solutions

#### Issue: "No checkboxes found with selector"

**Debug steps:**
1. Run in non-headless mode
2. Pause script execution with a breakpoint or sleep
3. Manually inspect page in DevTools
4. Copy the actual checkbox selector

**Python debugging trick:**
```python
# Add this temporarily in uncheck_all_visible_content():
all_inputs = self.driver.find_elements(By.TAG_NAME, 'input')
for inp in all_inputs:
    print(f"Found input: type={inp.get_attribute('type')}, checked={inp.get_attribute('checked')}")
```

#### Issue: Elements become stale

This is already handled in the code with try/except blocks. If it persists:
- Increase `time.sleep()` delays
- Add explicit waits before element interaction

#### Issue: Click intercepted

The script tries JavaScript click as fallback. If still failing:
```python
# Replace regular click with:
self.driver.execute_script("arguments[0].click();", element)
```

### 6. Advanced: Handling Two-Factor Authentication

If your Amazon account uses 2FA:

**Option A**: Manual intervention
```python
# Add after login in the login() method:
print("Please complete 2FA manually...")
input("Press Enter after completing 2FA...")
```

**Option B**: Use cookies
1. Log in manually first
2. Export cookies
3. Import cookies in script before navigation

**Option C**: Selenium with SMS API (complex)
- Use a service like Twilio
- Parse 2FA code from SMS
- Enter automatically

### 7. Production Checklist

Before scheduling or deploying:

- [ ] Test manually with HEADLESS=false
- [ ] Verify all checkboxes are found and unchecked
- [ ] Confirm pagination works (load more clicks)
- [ ] Test with different content amounts
- [ ] Set appropriate MAX_ITERATIONS
- [ ] Enable HEADLESS=true for scheduled runs
- [ ] Set up logging to file for debugging
- [ ] Test error recovery (network issues, etc.)

### 8. Logging to File

Add this to capture logs for debugging:

```python
# In deactivate_content.py, update logging configuration:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler('/tmp/amazon_kids_deactivator.log')  # File
    ]
)
```

### 9. Example: Complete Customization

Here's a complete example .env for a customized setup:

```bash
# Credentials
AMAZON_EMAIL=parent@example.com
AMAZON_PASSWORD=SecurePassword123!

# Timeouts (adjusted for slow connection)
PAGE_LOAD_TIMEOUT=60
ELEMENT_WAIT_TIMEOUT=20

# Customized selectors (after inspecting Amazon's page)
CHECKBOX_SELECTOR=div.content-card.active input[type="checkbox"]
CONTENT_LINK_TEXT=Parent Dashboard

# Increased iterations for large library
MAX_ITERATIONS=500

# Headless for automation
HEADLESS=true
```

## Getting Help

If you're stuck:

1. **Check the logs** - they show which selectors failed
2. **Run with browser visible** - watch what's happening
3. **Use browser console** - test selectors with `document.querySelectorAll()`
4. **Share anonymized HTML** - open an issue with the page structure (remove sensitive data)

## Example DevTools Workflow

```javascript
// In Chrome DevTools Console, test your selector:
document.querySelectorAll('input[type="checkbox"]:checked').length
// Should return count of checked items

// Test if selector finds elements:
document.querySelector('input[type="checkbox"]:checked')
// Should return first matching element or null

// Find all checkboxes (checked or not):
document.querySelectorAll('input[type="checkbox"]').length
```

## Security Note

When customizing and debugging, be careful not to:
- Log sensitive data (passwords, personal info)
- Share screenshots with personal information
- Commit .env file with real credentials
- Expose session tokens or cookies
