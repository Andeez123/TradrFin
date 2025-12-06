# Quick Vercel Deployment

## ✅ Files Ready
- `vercel.json` - Configured
- `backend/api/index.py` - Serverless handler created
- `.vercelignore` - Excludes unnecessary files

## 🚀 Deploy Now (3 Steps)

### Step 1: Login to Vercel
```powershell
vercel login
```

### Step 2: Deploy
```powershell
vercel --prod
```

### Step 3: Test
After deployment, Vercel will give you a URL like:
```
https://your-project.vercel.app
```

Test your API:
```
https://your-project.vercel.app/api/
https://your-project.vercel.app/api/portfolio
https://your-project.vercel.app/api/demo
```

## ⚠️ Important Limitations

Your backend will work BUT:
- **10-second timeout** - Long simulations may fail
- **Stateless** - Portfolio state resets between requests
- **Cold starts** - First request slower

## 🔧 If Deployment Fails

**Error: "Build failed"**
```powershell
# Check requirements.txt exists
ls backend\requirements.txt
```

**Error: "Function timeout"**
- Your simulation is too long for Vercel
- Consider Railway instead

**Error: "Module not found"**
- Check `backend/api/index.py` imports correctly
- Verify `backend/app.py` exists

## 📝 Next Steps After Deployment

1. Update frontend API URL to your Vercel URL
2. Test all endpoints
3. Monitor for timeout errors
4. Consider migrating to Railway if issues persist
