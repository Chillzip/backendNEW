# ChillZip Frontend - Vercel Deployment

This is the frontend part of ChillZip, ready for deployment to Vercel.

## Quick Deployment to Vercel

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI** (if you haven't already):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from this directory**:
   ```bash
   vercel --prod
   ```

4. **Follow the prompts**:
   - Link to existing project? **Yes** (if you have one) or **No** (to create new)
   - Project name: **chillzip**
   - Directory: **./** (current directory)

### Option 2: Deploy via Vercel Dashboard

1. **Zip this folder** and upload to Vercel dashboard
2. **Or connect your GitHub repository** if you've pushed the code there

## Important Configuration

### Backend URL Configuration

After you deploy the backend (Step 2), you'll need to update the API URL:

1. **Open `index.html`**
2. **Find line ~678** with:
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' 
       ? 'http://localhost:5003' 
       : 'https://your-backend-url.herokuapp.com'; // Replace with actual backend URL
   ```

3. **Replace `https://your-backend-url.herokuapp.com`** with your actual backend URL

### Domain Configuration

Since you own `chillzip.com`:

1. **In Vercel Dashboard**, go to your project settings
2. **Add Custom Domain**: `chillzip.com` and `www.chillzip.com`
3. **Update DNS** in your domain registrar:
   - Add CNAME record: `www` → `cname.vercel-dns.com`
   - Add A record: `@` → `76.76.19.61` (Vercel's IP)

## Files Included

- `index.html` - Complete frontend application
- `package.json` - Project configuration
- `vercel.json` - Vercel deployment configuration
- `README.md` - This file

## Next Steps

1. ✅ Deploy this frontend to Vercel
2. ⏳ Deploy the backend (Flask app) to Heroku/Railway
3. ⏳ Update the API_BASE_URL in index.html
4. ⏳ Configure your domain
5. ⏳ Set up Stripe keys
6. ⏳ Test and launch!

## Support

If you need help with deployment, the main project includes comprehensive guides and documentation.

# backend
