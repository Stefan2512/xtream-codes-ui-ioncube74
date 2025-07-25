# Xtream Codes UI with ION Cube 7.4 - Fixed Distribution

This distribution contains pre-configured Xtream Codes UI archives with ION Cube 7.4 already installed and configured, eliminating common compatibility issues.

## Files Included

- **xtream-codes-ui-main-ioncube74.zip** - Main server archive (includes admin panel)
- **xtream-codes-ui-loadbalancer-ioncube74.zip** - Load balancer archive (no admin panel)  
- **install-xtream-codes-ioncube74.py** - Installation script
- **README.md** - This documentation

## What's Fixed

✅ **ION Cube 7.4** pre-installed and configured  
✅ **All configuration files** updated to use ION Cube 7.4  
✅ **Case-insensitive** installation type input (main/MAIN/Main all work)  
✅ **Zero compatibility issues** - no more "undefined symbol" errors  
✅ **Clean archives** - sensitive server data removed  
✅ **Ready to use** - no additional fixes required  

## Installation Instructions

### 1. Upload Archives
Upload the ZIP files to your server or GitHub releases.

### 2. Update Installer URLs
Edit `install-xtream-codes-ioncube74.py` and update the download URLs:

```python
rDownloadURL = {
    "main": "https://your-server.com/releases/xtream-codes-ui-main-ioncube74.zip", 
    "sub": "https://your-server.com/releases/xtream-codes-ui-loadbalancer-ioncube74.zip"
}
```

### 3. Run Installation
```bash
chmod +x install-xtream-codes-ioncube74.py
sudo python3 install-xtream-codes-ioncube74.py
```

Choose installation type:
- **MAIN** - For main server (includes admin panel and database)
- **LB** - For load balancer (streaming only, no admin)
- **UPDATE** - For updating existing installations

## Verification

After installation, verify ION Cube 7.4 is working:

```bash
# Check ION Cube version
/home/xtreamcodes/iptv_xtream_codes/php/bin/php -m | grep -i ioncube

# Should show: ionCube Loader v14.4.1

# Access admin panel (MAIN installations only)
http://YOUR_SERVER_IP:25500
Username: admin
Password: admin
```

## Technical Details

- **Source**: Generated from working Xtream Codes installation  
- **ION Cube Version**: 7.4 (v14.4.1)  
- **PHP Version**: 7.4.33  
- **Supported OS**: Ubuntu 20.04 LTS  
- **Architecture**: x86_64  

## Archive Contents

### Main Server Archive
- Complete Xtream Codes installation
- Admin panel included
- Database SQL included
- ION Cube 7.4 pre-installed
- All services configured

### Load Balancer Archive  
- Xtream Codes installation without admin
- No database SQL (connects to main server)
- ION Cube 7.4 pre-installed
- Streaming services only

## Support

This fixed distribution eliminates the common ION Cube 7.2 compatibility issues that cause:
- "undefined symbol" errors
- "cannot open shared object file" errors  
- PHP module loading failures

No additional fixes or patches required - works out of the box.

---

*Generated automatically from working Xtream Codes UI installation with ION Cube 7.4*
