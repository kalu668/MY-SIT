# Sentry Error Tracking Setup Guide

## What is Sentry?
Sentry is a real-time error tracking platform that helps you:
- 📧 Get instant email alerts when errors occur
- 🐛 See detailed error reports with stack traces
- 📊 Track error frequency and trends
- 🔍 Debug issues before users report them
- ⚡ Monitor application performance

## Setup Instructions (5 minutes)

### 1. Create Free Sentry Account
1. Go to https://sentry.io/signup/
2. Sign up with your email (free plan includes 5,000 errors/month)
3. Create a new project
4. Select **Django** as the platform
5. Copy your **DSN** (Data Source Name) - it looks like:
   ```
   https://abc123@o123456.ingest.sentry.io/789012
   ```

### 2. Add DSN to Render Environment

**Option A: Through Render Dashboard**
1. Go to https://dashboard.render.com
2. Select your `my-site` service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Key: `SENTRY_DSN`
6. Value: Your DSN from step 1
7. Click **Save Changes**
8. Service will auto-redeploy

**Option B: Update render.yaml (already configured)**
1. Open `render.yaml`
2. Find the commented lines:
   ```yaml
   # - key: SENTRY_DSN
   #   value: https://your-sentry-dsn-here.ingest.sentry.io/your-project-id
   ```
3. Uncomment and replace with your actual DSN:
   ```yaml
   - key: SENTRY_DSN
     value: https://abc123@o123456.ingest.sentry.io/789012
   ```
4. Commit and push to GitHub - auto-deploy will handle the rest

### 3. Verify It's Working

**Test Error Capture:**
1. Add a test view in any app (e.g., `dashboard/views.py`):
   ```python
   def test_sentry(request):
       # This will trigger Sentry
       division_by_zero = 1 / 0
   ```
2. Add URL in `urls.py`:
   ```python
   path('test-sentry/', test_sentry),
   ```
3. Visit https://elitewealthcapita.uk/test-sentry/
4. Check your Sentry dashboard - you should see the error!
5. Remove the test code after verification

## What Gets Tracked?

Sentry automatically captures:
- ✅ **Python exceptions** (500 errors, database errors, etc.)
- ✅ **Request details** (URL, method, headers - without PII)
- ✅ **User context** (anonymous - no passwords or emails)
- ✅ **Stack traces** (shows exactly where errors occur)
- ✅ **Environment info** (Django version, Python version, etc.)
- ✅ **Performance data** (slow database queries, API calls)

## Email Notifications

Configure in Sentry dashboard:
1. Go to **Settings** > **Alerts**
2. Create alert rule: "When an event is seen"
3. Add your email
4. Get instant notifications when errors occur!

## Benefits for Your Site

### Before Sentry:
❌ Users report bugs days later  
❌ No idea what caused the error  
❌ Difficult to reproduce issues  
❌ Users lose trust due to repeated errors

### After Sentry:
✅ Know about errors immediately  
✅ See exact code that caused the problem  
✅ Fix issues before users complain  
✅ Track which errors are most common  
✅ Monitor site health in real-time

## Best Practices

1. **Check Sentry Weekly:** Review error trends
2. **Set Up Alerts:** Get notified for critical errors
3. **Mark Resolved:** Mark fixed issues as resolved
4. **Use Releases:** Tag deploys to track when errors started
5. **Ignore Noise:** Ignore known/expected errors (e.g., 404s)

## Cost

- **Free Tier:** 5,000 errors/month (plenty for most sites)
- **Paid Plans:** $26/month for 50,000 errors (if you grow)

## Privacy & Security

Configured to NOT send:
- ❌ Passwords
- ❌ Credit card numbers
- ❌ Personal emails
- ❌ Session tokens
- ✅ Only error data for debugging

## Support

If you have questions:
- Sentry Docs: https://docs.sentry.io/platforms/python/guides/django/
- Sentry Support: support@sentry.io

---

**Status:** ✅ Sentry integration code added to `settings.py`  
**Action Required:** Get your DSN from sentry.io and add to Render environment  
**Time to Complete:** 5 minutes
