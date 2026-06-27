# CoachJVTech - Cloudflare DNS Configuration Guide

## ✅ Current Status

- **Domain:** coachjvtech.us (Purchased & managed via Cloudflare)
- **DNS Provider:** Cloudflare
- **GitHub Repo:** https://github.com/KINGSACCOUNT1/coach-jv
- **Application:** Ready to deploy

---

## 🌐 DNS Configuration for Deployment

### Option 1: Deploy to Render.com (Recommended - render.yaml already configured)

#### Step 1: Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select repository: `KINGSACCOUNT1/coach-jv`
5. Render will auto-detect settings from `render.yaml`
6. Set environment variables:
   ```
   SECRET_KEY=<generate-strong-key>
   DEBUG=False
   DATABASE_URL=<will-be-auto-provided>
   ZOHO_EMAIL=support@coachjvtech.us
   ZOHO_APP_PASSWORD=<your-zoho-app-password>
   ```
7. Click "Create Web Service"
8. Wait for deployment (5-10 minutes)
9. Note your Render URL (e.g., `coach-jv-xyz.onrender.com`)

#### Step 2: Configure Cloudflare DNS
1. Log in to Cloudflare Dashboard: https://dash.cloudflare.com
2. Select domain: **coachjvtech.us**
3. Go to **DNS** → **Records**
4. Add/Update these records:

**Root Domain (coachjvtech.us):**
```
Type: CNAME
Name: @
Target: coach-jv-xyz.onrender.com (your Render URL)
Proxy status: Proxied (orange cloud)
TTL: Auto
```

**WWW Subdomain:**
```
Type: CNAME
Name: www
Target: coach-jv-xyz.onrender.com (your Render URL)
Proxy status: Proxied (orange cloud)
TTL: Auto
```

#### Step 3: Configure Custom Domain in Render
1. In Render Dashboard → Your Service → Settings
2. Scroll to "Custom Domain"
3. Click "Add Custom Domain"
4. Enter: `coachjvtech.us`
5. Click "Add Custom Domain" again
6. Enter: `www.coachjvtech.us`
7. Render will provide verification instructions
8. SSL certificate will be auto-generated

#### Step 4: Cloudflare SSL Settings
1. In Cloudflare → SSL/TLS
2. Set SSL mode to: **Full (strict)**
3. Enable "Always Use HTTPS"
4. Enable "Automatic HTTPS Rewrites"

---

### Option 2: Deploy to DigitalOcean App Platform

#### Step 1: Deploy on DigitalOcean
1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect GitHub: `KINGSACCOUNT1/coach-jv`
4. Configure:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command: `gunicorn coach.wsgi:application`
5. Add PostgreSQL database
6. Set environment variables
7. Deploy app
8. Note your app URL (e.g., `coach-jv-xyz.ondigitalocean.app`)

#### Step 2: Cloudflare DNS (Same as above)
Use the DigitalOcean app URL as the CNAME target

---

### Option 3: Deploy to VPS (Manual Setup)

#### If you have a VPS with IP address (e.g., 123.45.67.89):

**Cloudflare DNS Records:**
```
Type: A
Name: @
Content: 123.45.67.89 (your VPS IP)
Proxy status: Proxied (orange cloud)
TTL: Auto

Type: A
Name: www
Content: 123.45.67.89 (your VPS IP)
Proxy status: Proxied (orange cloud)
TTL: Auto
```

---

## 📧 Email Configuration (Cloudflare)

### Email Records for Zoho Mail

If using Zoho Mail for support@coachjvtech.us, add these DNS records in Cloudflare:

#### MX Records (Mail Exchange):
```
Type: MX
Name: @
Mail server: mx.zoho.com
Priority: 10
TTL: Auto

Type: MX
Name: @
Mail server: mx2.zoho.com
Priority: 20
TTL: Auto

Type: MX
Name: @
Mail server: mx3.zoho.com
Priority: 50
TTL: Auto
```

#### TXT Records (SPF & DKIM):
```
Type: TXT
Name: @
Content: v=spf1 include:zoho.com ~all
TTL: Auto

Type: TXT
Name: zmail._domainkey
Content: <your-zoho-dkim-key>
TTL: Auto
```

#### CNAME Records:
```
Type: CNAME
Name: mail
Target: business.zoho.com
Proxy status: DNS only (grey cloud)
TTL: Auto
```

---

## 🔐 Cloudflare Security Settings (Recommended)

### 1. SSL/TLS Settings
- **SSL/TLS encryption mode:** Full (strict)
- **Always Use HTTPS:** On
- **Automatic HTTPS Rewrites:** On
- **Minimum TLS Version:** TLS 1.2
- **Opportunistic Encryption:** On
- **TLS 1.3:** On

### 2. Firewall Rules
Go to Security → WAF → Create Firewall Rule

**Rule 1: Block Bad Bots**
```
(cf.client.bot) and not (cf.verified_bot_category in {"Search Engine Crawler"})
Action: Block
```

**Rule 2: Rate Limiting**
```
(http.request.uri.path contains "/api/")
Action: Rate Limit (100 requests per minute)
```

**Rule 3: Geo-blocking (Optional)**
```
(ip.geoip.country ne "US" and ip.geoip.country ne "CA")
Action: Challenge (CAPTCHA)
```

### 3. Page Rules
**Force HTTPS:**
```
URL: http://*coachjvtech.us/*
Setting: Always Use HTTPS
```

**Cache Everything:**
```
URL: coachjvtech.us/static/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
```

### 4. Speed Optimization
- **Auto Minify:** Enable JavaScript, CSS, HTML
- **Brotli Compression:** On
- **Rocket Loader:** Off (for Django apps)
- **Mirage:** On (image optimization)

---

## ✅ Verification Checklist

After DNS configuration:

- [ ] Wait 5-10 minutes for DNS propagation
- [ ] Test: http://coachjvtech.us (should redirect to HTTPS)
- [ ] Test: https://coachjvtech.us (should load your app)
- [ ] Test: https://www.coachjvtech.us (should work)
- [ ] Test: Email delivery from support@coachjvtech.us
- [ ] Check SSL certificate (should show valid/secure)
- [ ] Test all pages (home, dashboard, login, etc.)
- [ ] Test email functionality (password reset, registration)
- [ ] Monitor Cloudflare Analytics

---

## 🛠️ Quick Commands

### Check DNS Propagation:
```bash
# Check A record
dig coachjvtech.us

# Check CNAME
dig www.coachjvtech.us

# Check MX records
dig MX coachjvtech.us

# Check from specific DNS
nslookup coachjvtech.us 1.1.1.1
```

### Test SSL:
```bash
curl -I https://coachjvtech.us
openssl s_client -connect coachjvtech.us:443 -servername coachjvtech.us
```

---

## 📞 Support Resources

**Cloudflare Support:**
- Dashboard: https://dash.cloudflare.com
- Docs: https://developers.cloudflare.com
- Community: https://community.cloudflare.com

**Domain:** coachjvtech.us  
**Emails:**
- support@coachjvtech.us
- admin@coachjvtech.us
- billing@coachjvtech.us

**Repository:** https://github.com/KINGSACCOUNT1/coach-jv

---

## 🚀 Recommended: Deploy to Render.com

Since your `render.yaml` is already configured, Render.com is the fastest option:

1. Connect GitHub repo to Render
2. Auto-deploy (5 minutes)
3. Get Render URL
4. Update Cloudflare CNAME to point to Render URL
5. Done! ✅

**Cloudflare will handle:**
- SSL certificates (automatic)
- DDoS protection
- CDN/caching
- Firewall protection
- Analytics

---

Generated: June 5, 2026  
Status: Ready for deployment 🎉
