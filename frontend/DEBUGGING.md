# How to Debug on macOS

## View Browser Console (to see errors)

### Chrome/Edge:
1. Open your app at http://localhost:5173
2. Press **Command + Option + J** (⌘ + ⌥ + J)
   - OR right-click on the page → "Inspect"
   - OR go to View → Developer → Developer Tools

### Safari:
1. First enable Developer menu:
   - Safari → Settings → Advanced
   - Check "Show Develop menu in menu bar"
2. Open your app at http://localhost:5173
3. Press **Command + Option + C** (⌘ + ⌥ + C)
   - OR Develop → Show Web Inspector

### Firefox:
1. Open your app at http://localhost:5173
2. Press **Command + Option + K** (⌘ + ⌥ + K)
   - OR right-click → "Inspect Element"

## Common Issues

### White Screen
- Check the Console tab for red error messages
- Common causes:
  - Import path errors
  - Missing dependencies
  - JavaScript syntax errors

### Check Terminal
- Look at the terminal where `npm run dev` is running
- Any errors will show there too

## Quick Test
Open the browser console and type:
```javascript
console.log("Test")
```
If you see "Test" printed, the console is working!

