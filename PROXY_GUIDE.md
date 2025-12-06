# Scrape.do Setup Guide 🚀

## What is Scrape.do?

Scrape.do is a smart proxy service that handles:
- 🔄 IP rotation
- 🤖 CAPTCHA solving
- 🌐 Geo-targeting
- ⚡ Fast response times

## ✨ Free Tier

- **1,000 requests/month FREE**
- No credit card required
- 99.9% uptime
- JavaScript rendering

## 🎯 How Your Scraper Uses It

**Smart Fallback Strategy:**
1. ✅ First tries **direct scraping** (free, fast)
2. ❌ If blocked/failed → Automatically uses **Scrape.do**
3. 💰 Only uses your quota when needed!

## 📝 Setup (2 Minutes)

### Step 1: Get Your Free Token

1. Visit: https://scrape.do
2. Click **"Sign Up"** (top right)
3. Enter your email
4. Verify email
5. Copy your **API token**

### Step 2: Add to Local Environment

Update your `.env` file:

```env
SCRAPE_DO_TOKEN=your_token_here_1234567890abcdef
```

### Step 3: Add to Streamlit Cloud

Go to your app → Settings → Secrets:

```toml
SCRAPE_DO_TOKEN = "your_token_here_1234567890abcdef"
```

### Step 4: Done! 🎉

Your scraper will now:
- Try direct scraping first (saves quota)
- Use Scrape.do only when blocked
- Handle tough sites automatically

## 💡 Example Usage

```python
# Your scraper automatically handles this:

# Attempt 1: Direct scraping (FREE)
html = scraper.scrape("https://example.com")

# If blocked...
# Attempt 2: Via Scrape.do (uses 1 API call)
html = scraper.scrape_with_proxy("https://example.com")
```

## 📊 Monitor Your Usage

Check your usage at: https://scrape.do/dashboard

You'll see:
- Requests used this month
- Remaining requests
- Success rate

## 🎯 Free Tier = 1,000 Requests

**What you can scrape with 1,000 requests:**

- 🏢 **50 full websites** (20 pages each)
- 📄 **1,000 single pages**
- 🔄 **Unlimited retries** on failed requests (only successful ones count)

## 🚀 Pro Tips

### 1. Save Your Quota
✅ **Good:** Scrape small sites directly (no quota used)  
❌ **Bad:** Use proxy for everything

### 2. When Scrape.do Activates
- Large e-commerce sites (Amazon, eBay)
- Sites with bot protection (Cloudflare, etc.)
- Social media platforms
- News sites with paywalls

### 3. When You Don't Need It
- Small business websites
- Blogs
- Documentation sites
- Your own websites

## 🔧 Advanced Configuration

Want to force proxy for specific domains?

Update your `.env`:

```env
# Always use proxy for these domains
FORCE_PROXY_DOMAINS=amazon.com,ebay.com,twitter.com
```

## 📈 Upgrade Options

**If 1,000 requests/month isn't enough:**

| Plan | Requests | Price |
|------|----------|-------|
| Free | 1,000/mo | $0 |
| Starter | 10,000/mo | $10 |
| Pro | 100,000/mo | $50 |
| Business | 1M/mo | $200 |

## ❓ Troubleshooting

### "Token is invalid"
- Check you copied the full token
- No extra spaces
- Get a fresh token from dashboard

### "Quota exceeded"
- You've used 1,000 requests this month
- Wait for monthly reset
- Or upgrade plan

### "Proxy not being used"
- This is normal! Proxy only activates when needed
- If direct scraping works, it won't use proxy
- Check logs: `Loading with Scrape.do proxy:` means it's active

## 🎊 Success Messages

When working correctly, you'll see:

```
  Loading: https://example.com
  Got HTML: 50234 chars
```

When proxy kicks in:

```
  Direct scraping failed: Timeout
  Retrying with Scrape.do proxy...
  Loading with Scrape.do proxy: https://example.com
  Got HTML via proxy: 50234 chars
```

## 📞 Support

- **Dashboard:** https://scrape.do/dashboard
- **Docs:** https://docs.scrape.do/
- **Email:** support@scrape.do

---

**Ready to start?** Just add your token to `.env` and you're good to go! 🚀
