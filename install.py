#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Xtream Codes UI Installer with ION Cube 7.4 + Auto Update System - Production Ready Version
import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime

# Updated URLs for Stefan's repository
rDownloadURL = {
    "main": "https://github.com/Stefan2512/xtream-codes-ui-ioncube74/releases/download/v1.0/xtream-codes-ui-main-ioncube74.zip", 
    "sub": "https://github.com/Stefan2512/xtream-codes-ui-ioncube74/releases/download/v1.0/xtream-codes-ui-loadbalancer-ioncube74.zip"
}

rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "mariadb-server", "libpng16-16", "libzip5", "python3-paramiko", "python-is-python3", "python3-requests"]
rInstall = {"MAIN": "main", "LB": "sub"}
rUpdate = {"UPDATE": "update"}

rVersions = {
    "20.04": "focal"
}

class col:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def generate(length=19): return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getVersion():
    try: return os.popen("lsb_release -d").read().split(":")[-1].strip()
    except: return ""

def printc(rText, rColour=col.BRIGHT_GREEN, rPadding=0, rLimit=46):
    print("%s ┌─────────────────────────────────────────────────┐ %s" % (rColour, col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    array = [rText[i:i+rLimit] for i in range(0, len(rText), rLimit)]
    for i in array : print("%s │ %s%s%s │ %s" % (rColour, " "*round(23-(len(i)/2)), i, " "*round(46-(22-(len(i)/2))-len(i)), col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    print("%s └─────────────────────────────────────────────────┘ %s" % (rColour, col.ENDC))
    print(" ")

def install_update_system():
    """Install the auto-update system"""
    printc("Installing Auto-Update System", col.BRIGHT_CYAN)
    
    # Ensure python3-requests is installed
    os.system("apt-get install -y python3-requests > /dev/null 2>&1")
    
    # Create update checker script
    update_checker_content = '''#!/usr/bin/python3
import requests
import json
import os
import zipfile
import shutil
import subprocess
from datetime import datetime

class XtreamUpdater:
    def __init__(self):
        self.github_api = "https://api.github.com/repos/Stefan2512/xtream-codes-ui-ioncube74/releases/latest"
        self.current_version_file = "/home/xtreamcodes/iptv_xtream_codes/version.json"
        self.notification_file = "/home/xtreamcodes/iptv_xtream_codes/admin/update_notification.json"
        self.xtream_path = "/home/xtreamcodes/iptv_xtream_codes"
        
    def get_current_version(self):
        """Get currently installed version"""
        try:
            if os.path.exists(self.current_version_file):
                with open(self.current_version_file, 'r') as f:
                    return json.load(f).get("version", "unknown")
            return "v1.0-initial"
        except:
            return "v1.0-initial"
    
    def check_for_updates(self):
        """Check GitHub for new releases"""
        try:
            response = requests.get(self.github_api, timeout=10)
            if response.status_code == 200:
                release = response.json()
                
                # Find release archive
                update_asset = None
                for asset in release.get('assets', []):
                    if 'release_22f' in asset['name'] and asset['name'].endswith('.zip'):
                        update_asset = asset
                        break
                
                if update_asset:
                    current_version = self.get_current_version()
                    latest_version = release['tag_name']
                    
                    # Check if update is available
                    update_available = latest_version != current_version
                    
                    # Save notification for admin panel
                    notification = {
                        "update_available": update_available,
                        "current_version": current_version,
                        "latest_version": latest_version,
                        "download_url": update_asset['browser_download_url'],
                        "file_size": update_asset.get('size', 0),
                        "release_notes": release.get('body', 'New update available'),
                        "published_at": release.get('published_at'),
                        "check_time": datetime.now().isoformat(),
                        "show_notification": update_available
                    }
                    
                    # Create admin directory if it doesn't exist
                    os.makedirs(os.path.dirname(self.notification_file), exist_ok=True)
                    
                    with open(self.notification_file, 'w') as f:
                        json.dump(notification, f, indent=2)
                    
                    return notification
                
        except Exception as e:
            # Silent fail for cron job
            pass
        
        return {"update_available": False, "error": "Check failed"}
    
    def apply_update(self, download_url):
        """Apply update from download URL"""
        try:
            # Create backup
            backup_dir = f"/tmp/xtream_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup current admin and pytools
            if os.path.exists(f"{self.xtream_path}/admin"):
                shutil.copytree(f"{self.xtream_path}/admin", f"{backup_dir}/admin")
            if os.path.exists(f"{self.xtream_path}/pytools"):
                shutil.copytree(f"{self.xtream_path}/pytools", f"{backup_dir}/pytools")
            
            # Download update
            response = requests.get(download_url, timeout=60)
            if response.status_code == 200:
                update_file = "/tmp/xtream_update.zip"
                with open(update_file, 'wb') as f:
                    f.write(response.content)
                
                # Extract and apply update
                with zipfile.ZipFile(update_file, 'r') as zip_ref:
                    zip_ref.extractall("/tmp/xtream_update")
                
                update_source = "/tmp/xtream_update/XtreamUI-master"
                if os.path.exists(update_source):
                    # Stop services
                    subprocess.run(["systemctl", "stop", "xtreamcodes"], capture_output=True)
                    
                    # Apply update
                    if os.path.exists(f"{update_source}/admin"):
                        if os.path.exists(f"{self.xtream_path}/admin"):
                            shutil.rmtree(f"{self.xtream_path}/admin")
                        shutil.copytree(f"{update_source}/admin", f"{self.xtream_path}/admin")
                    
                    if os.path.exists(f"{update_source}/pytools"):
                        if os.path.exists(f"{self.xtream_path}/pytools"):
                            shutil.rmtree(f"{self.xtream_path}/pytools")
                        shutil.copytree(f"{update_source}/pytools", f"{self.xtream_path}/pytools")
                    
                    # Copy permissions script
                    if os.path.exists(f"{update_source}/permissions.sh"):
                        shutil.copy2(f"{update_source}/permissions.sh", f"{self.xtream_path}/permissions.sh")
                    
                    # Update version info
                    if os.path.exists(f"{update_source}/version.json"):
                        shutil.copy2(f"{update_source}/version.json", self.current_version_file)
                    
                    # Set permissions
                    subprocess.run(["chown", "-R", "xtreamcodes:xtreamcodes", "/home/xtreamcodes"], capture_output=True)
                    if os.path.exists(f"{self.xtream_path}/permissions.sh"):
                        subprocess.run([f"{self.xtream_path}/permissions.sh"], capture_output=True)
                    
                    # Start services
                    subprocess.run([f"{self.xtream_path}/start_services.sh"], capture_output=True)
                    
                    # Cleanup
                    os.remove(update_file)
                    shutil.rmtree("/tmp/xtream_update", ignore_errors=True)
                    
                    return {"success": True, "message": "Update applied successfully", "backup": backup_dir}
                else:
                    return {"success": False, "message": "Invalid update package"}
            else:
                return {"success": False, "message": "Failed to download update"}
                
        except Exception as e:
            return {"success": False, "message": f"Update failed: {str(e)}"}

# API endpoints for admin panel
def api_check_updates():
    updater = XtreamUpdater()
    return json.dumps(updater.check_for_updates())

def api_apply_update():
    try:
        # This would be called from admin panel with POST data
        updater = XtreamUpdater()
        # For now, get latest release
        check_result = updater.check_for_updates()
        if check_result.get("update_available"):
            return json.dumps(updater.apply_update(check_result["download_url"]))
        else:
            return json.dumps({"success": False, "message": "No updates available"})
    except Exception as e:
        return json.dumps({"success": False, "message": str(e)})

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            updater = XtreamUpdater()
            result = updater.check_for_updates()
            if result.get("update_available"):
                print(f"Update available: {result['latest_version']}")
            else:
                print("No updates available")
        elif sys.argv[1] == "apply":
            updater = XtreamUpdater()
            check_result = updater.check_for_updates()
            if check_result.get("update_available"):
                result = updater.apply_update(check_result["download_url"])
                print(result["message"])
            else:
                print("No updates available")
    else:
        # Default: just check and create notification
        updater = XtreamUpdater()
        updater.check_for_updates()
'''
    
    # Write update checker script
    with open("/usr/local/bin/xtream_updater.py", "w") as f:
        f.write(update_checker_content)
    
    os.chmod("/usr/local/bin/xtream_updater.py", 0o755)
    
    # Create admin panel update integration
    admin_integration = '''<?php
/**
 * Xtream Codes Auto-Update System Integration
 * Include this in your admin panel header
 */

function getUpdateNotification() {
    $notification_file = "/home/xtreamcodes/iptv_xtream_codes/admin/update_notification.json";
    
    if (file_exists($notification_file)) {
        $notification = json_decode(file_get_contents($notification_file), true);
        if ($notification && $notification['show_notification'] && $notification['update_available']) {
            return $notification;
        }
    }
    return null;
}

function dismissUpdateNotification() {
    $notification_file = "/home/xtreamcodes/iptv_xtream_codes/admin/update_notification.json";
    if (file_exists($notification_file)) {
        $notification = json_decode(file_get_contents($notification_file), true);
        $notification['show_notification'] = false;
        file_put_contents($notification_file, json_encode($notification, JSON_PRETTY_PRINT));
    }
}

// Handle AJAX requests
if (isset($_POST['action'])) {
    if ($_POST['action'] == 'dismiss_notification') {
        dismissUpdateNotification();
        echo json_encode(['success' => true]);
        exit;
    }
    
    if ($_POST['action'] == 'apply_update') {
        $output = shell_exec('/usr/local/bin/xtream_updater.py apply 2>&1');
        echo json_encode(['success' => true, 'output' => $output]);
        exit;
    }
    
    if ($_POST['action'] == 'check_updates') {
        $output = shell_exec('/usr/local/bin/xtream_updater.py check 2>&1');
        echo json_encode(['success' => true, 'output' => $output]);
        exit;
    }
}

$update_notification = getUpdateNotification();
?>

<?php if ($update_notification): ?>
<div id="update-notification" class="alert alert-info" style="margin: 10px; border-left: 4px solid #007bff; background: #d1ecf1; padding: 15px;">
    <div style="display: flex; justify-content: between; align-items: center;">
        <div style="flex: 1;">
            <h4 style="margin: 0 0 10px 0; color: #0c5460;">
                <i class="fa fa-download"></i> Update Available: <?php echo htmlspecialchars($update_notification['latest_version']); ?>
            </h4>
            <p style="margin: 0 0 10px 0; color: #0c5460;">
                Current: <?php echo htmlspecialchars($update_notification['current_version']); ?> | 
                Size: <?php echo round($update_notification['file_size'] / 1024 / 1024, 1); ?> MB
            </p>
            <div style="margin-top: 15px;">
                <button onclick="applyUpdate()" class="btn btn-success" style="margin-right: 10px;">
                    <i class="fa fa-download"></i> Update Now
                </button>
                <button onclick="dismissNotification()" class="btn btn-secondary">
                    <i class="fa fa-times"></i> Dismiss
                </button>
            </div>
        </div>
        <button onclick="dismissNotification()" style="background: none; border: none; font-size: 20px; color: #0c5460; cursor: pointer; padding: 0; margin-left: 20px;">&times;</button>
    </div>
</div>

<script>
function dismissNotification() {
    fetch(window.location.href, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'action=dismiss_notification'
    }).then(() => {
        document.getElementById('update-notification').style.display = 'none';
    });
}

function applyUpdate() {
    if (confirm('Apply update now? This will restart Xtream Codes services.')) {
        document.getElementById('update-notification').innerHTML = '<div style="text-align: center; padding: 20px;"><i class="fa fa-spinner fa-spin"></i> Updating... Please wait.</div>';
        
        fetch(window.location.href, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'action=apply_update'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('update-notification').innerHTML = '<div style="color: green; text-align: center; padding: 20px;"><i class="fa fa-check"></i> Update completed successfully! Refreshing page...</div>';
                setTimeout(() => window.location.reload(), 3000);
            } else {
                document.getElementById('update-notification').innerHTML = '<div style="color: red; text-align: center; padding: 20px;"><i class="fa fa-exclamation-triangle"></i> Update failed. Please try again.</div>';
            }
        });
    }
}
</script>
<?php endif; ?>
'''
    
    # Create admin integration file
    admin_dir = "/home/xtreamcodes/iptv_xtream_codes/admin"
    if os.path.exists(admin_dir):
        with open(f"{admin_dir}/update_integration.php", "w") as f:
            f.write(admin_integration)
        
        # Also create the notification file structure
        os.makedirs(admin_dir, exist_ok=True)
    
    # Create cron job for periodic checking
    cron_entry = "*/30 * * * * root /usr/local/bin/xtream_updater.py check > /dev/null 2>&1"
    
    # Add to crontab if not already present
    try:
        with open("/etc/crontab", "r") as f:
            crontab_content = f.read()
        
        if "xtream_updater.py" not in crontab_content:
            with open("/etc/crontab", "a") as f:
                f.write(f"\n{cron_entry}\n")
            printc("Auto-update checker scheduled every 30 minutes")
    except:
        pass
    
    # Create initial version file
    version_info = {
        "version": "v1.0-initial",
        "build": "initial",
        "date": datetime.now().isoformat(),
        "installed_via": "installer"
    }
    
    version_file = "/home/xtreamcodes/iptv_xtream_codes/version.json"
    os.makedirs(os.path.dirname(version_file), exist_ok=True)
    with open(version_file, "w") as f:
        json.dump(version_info, f, indent=2)
    
    printc("✅ Auto-Update System Installed Successfully!", col.BRIGHT_GREEN)
    printc("🔔 Users will be notified of updates in admin panel", col.BRIGHT_CYAN)
    printc("⏰ Checks for updates every 30 minutes automatically", col.BRIGHT_CYAN)

def prepare(rType="MAIN"):
    global rPackages
    if rType != "MAIN": rPackages = rPackages[:-1]
    printc("Preparing Installation")
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        shutil.copyfile('/home/xtreamcodes/iptv_xtream_codes/config', '/tmp/config.xtmp')
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):    
        os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try: os.remove(rFile)
        except: pass
    printc("Updating Operating System")
    os.system("apt-get update > /dev/null")
    os.system("apt-get -y full-upgrade > /dev/null")
    if rType == "MAIN":
        printc("Install MariaDB 10.5 repository")
        os.system("apt-get install -y software-properties-common > /dev/null")
        os.system("apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8 >/dev/null 2>&1")
        os.system("add-apt-repository 'deb [arch=amd64,arm64,ppc64el] http://mirror.lstn.net/mariadb/repo/10.5/ubuntu focal main'  > /dev/null")
        os.system("apt-get update > /dev/null")
    for rPackage in rPackages:
        printc("Installing %s" % rPackage)
        os.system("apt-get install %s -y > /dev/null" % rPackage)
    printc("Installing pip2 and python2 paramiko")
    
    os.system("add-apt-repository universe > /dev/null 2>&1 && curl https://raw.githubusercontent.com/Stefan2512/xtream-codes-ui-ioncube74/master/files/get-pip.py --output get-pip.py > /dev/null 2>&1 && python2 get-pip.py > /dev/null 2>&1 && pip2 install paramiko > /dev/null 2>&1")    
    os.system("apt-get install -f > /dev/null")
    try:
        subprocess.check_output("getent passwd xtreamcodes > /dev/null".split())
    except:
        printc("Creating user xtreamcodes")
        os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True

def install(rType="MAIN"):
    global rInstall, rDownloadURL
    printc("Downloading Xtream Codes UI with ION Cube 7.4")
    try: rURL = rDownloadURL[rInstall[rType]]
    except:
        printc("Invalid download URL!", col.BRIGHT_RED)
        return False
    os.system('wget -q -O "/tmp/xtreamcodes.zip" "%s"' % rURL)
    if os.path.exists("/tmp/xtreamcodes.zip"):
        printc("Installing Xtream Codes UI with ION Cube 7.4")
        os.system('unzip -o "/tmp/xtreamcodes.zip" -d "/home/xtreamcodes/" > /dev/null')
        try: os.remove("/tmp/xtreamcodes.zip")
        except: pass
        
        # Download database.sql for MAIN server installation
        if rType == "MAIN":
            printc("Downloading Database Schema")
            rDatabaseURL = "https://raw.githubusercontent.com/Stefan2512/xtream-codes-ui-ioncube74/main/database.sql"
            os.system('wget -q -O "/home/xtreamcodes/iptv_xtream_codes/database.sql" "%s"' % rDatabaseURL)
            if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/database.sql"):
                printc("Failed to download database schema!", col.BRIGHT_RED)
                return False
            printc("Database schema downloaded successfully")
        
        return True
    printc("Failed to download installation file!", col.BRIGHT_RED)
    return False

def mysql(rUsername, rPassword):
    printc("Configuring MySQL")
    
    # Configure MariaDB to run on port 7999 (Xtream Codes requirement)
    printc("Configuring MariaDB for port 7999")
    
    # Stop MariaDB to change configuration
    os.system("systemctl stop mariadb > /dev/null 2>&1")
    
    # Create Xtream-specific MariaDB configuration
    xtream_config = """[mysqld]
port = 7999
bind-address = 127.0.0.1

# Xtream Codes optimizations
max_connections = 2000
back_log = 4096
open_files_limit = 16384
innodb_open_files = 16384
max_connect_errors = 3072
table_open_cache = 4096
table_definition_cache = 4096

tmp_table_size = 1G
max_heap_table_size = 1G

innodb_buffer_pool_size = 12G
innodb_buffer_pool_instances = 1
innodb_read_io_threads = 64
innodb_write_io_threads = 64
innodb_thread_concurrency = 0
innodb_flush_log_at_trx_commit = 0
innodb_flush_method = O_DIRECT
performance_schema = ON
innodb-file-per-table = 1
innodb_io_capacity = 20000
innodb_table_locks = 0
innodb_lock_wait_timeout = 0
innodb_deadlock_detect = 0
innodb_log_file_size = 512M

sql-mode = "NO_ENGINE_SUBSTITUTION"

[mysqldump]
quick
quote-names
max_allowed_packet = 16M

[mysql]

[isamchk]
key_buffer_size = 16M
"""
    
    # Write Xtream MariaDB configuration
    with open("/etc/mysql/mariadb.conf.d/99-xtream.cnf", "w") as config_file:
        config_file.write(xtream_config)
    
    # Start MariaDB with new configuration
    printc("Starting MariaDB on port 7999")
    os.system("systemctl start mariadb > /dev/null 2>&1")
    
    # Wait for MariaDB to fully start
    printc("Waiting for MariaDB to start...")
    import time
    time.sleep(8)
    
    # Fix MariaDB authentication first
    printc("Configuring MariaDB authentication")
    os.system('mysql -u root -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED BY \'\';" > /dev/null 2>&1')
    os.system('mysql -u root -e "FLUSH PRIVILEGES;" > /dev/null 2>&1')
    
    # Try to connect with root user on port 7999
    printc("Testing MySQL connection on port 7999")
    
    # Test connection
    test_result = os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "SELECT 1;" > /dev/null 2>&1')
    if test_result != 0:
        printc("Failed to connect to MySQL on port 7999!", col.BRIGHT_RED)
        return False
    
    # Verify database.sql exists
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/database.sql"):
        printc("Database schema file not found!", col.BRIGHT_RED)
        return False
    
    printc("Creating database and user")
    
    # Create database
    result = os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;" > /dev/null 2>&1')
    if result != 0:
        printc("Failed to create database!", col.BRIGHT_RED)
        return False
    
    printc("Importing database schema")
    # Import database schema
    result = os.system("mysql -u root -P 7999 -h 127.0.0.1 xtream_iptvpro < /home/xtreamcodes/iptv_xtream_codes/database.sql > /dev/null 2>&1")
    if result != 0:
        printc("Failed to import database schema!", col.BRIGHT_RED)
        return False
    
    printc("Configuring database settings")
    # Update settings
    settings_sql = 'USE xtream_iptvpro; UPDATE settings SET live_streaming_pass = \'%s\', unique_id = \'%s\', crypt_load_balancing = \'%s\';' % (generate(20), generate(10), generate(20))
    os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % settings_sql)
    
    # Insert server configuration
    server_sql = 'USE xtream_iptvpro; REPLACE INTO streaming_servers (id, server_name, domain_name, server_ip, vpn_ip, ssh_password, ssh_port, diff_time_main, http_broadcast_port, total_clients, system_os, network_interface, latency, status, enable_geoip, geoip_countries, last_check_ago, can_delete, server_hardware, total_services, persistent_connections, rtmp_port, geoip_type, isp_names, isp_type, enable_isp, boost_fpm, http_ports_add, network_guaranteed_speed, https_broadcast_port, https_ports_add, whitelist_ips, watchdog_data, timeshift_only) VALUES (1, \'Main Server\', \'\', \'%s\', \'\', NULL, NULL, 0, 25461, 1000, \'%s\', \'eth0\', 0, 1, 0, \'\', 0, 0, \'{}\', 3, 0, 25462, \'low_priority\', \'\', \'low_priority\', 0, 1, \'\', 1000, 25463, \'\', \'[\"127.0.0.1\",\"\"]\', \'{}\', 0);' % (getIP(), getVersion())
    os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % server_sql)
    
    # Create admin user with ALL required fields
    admin_sql = 'USE xtream_iptvpro; INSERT INTO reg_users (id, username, password, email, member_group_id, verified, status, date_registered, default_lang, reseller_dns, google_2fa_sec) VALUES (1, \'admin\', \'\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\', \'admin@website.com\', 1, 1, 1, UNIX_TIMESTAMP(), \'English\', \'\', \'\') ON DUPLICATE KEY UPDATE password=\'\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\';'
    os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % admin_sql)
    
    printc("Creating MySQL user for Xtream Codes")
    # Drop existing users first
    os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "DROP USER IF EXISTS \'%s\'@\'localhost\'; DROP USER IF EXISTS \'%s\'@\'127.0.0.1\'; DROP USER IF EXISTS \'%s\'@\'%%\';" > /dev/null 2>&1' % (rUsername, rUsername, rUsername))
    
    # Create database user for all possible hosts
    user_creation_sql = 'CREATE USER \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'; CREATE USER \'%s\'@\'127.0.0.1\' IDENTIFIED BY \'%s\'; CREATE USER \'%s\'@\'%%\' IDENTIFIED BY \'%s\';' % (rUsername, rPassword, rUsername, rPassword, rUsername, rPassword)
    result = os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % user_creation_sql)
    if result != 0:
        printc("Failed to create database user!", col.BRIGHT_RED)
        return False
    
    # Grant privileges to all hosts
    grant_sql = 'GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO \'%s\'@\'localhost\' WITH GRANT OPTION; GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO \'%s\'@\'127.0.0.1\' WITH GRANT OPTION; GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO \'%s\'@\'%%\' WITH GRANT OPTION; GRANT SELECT, LOCK TABLES ON *.* TO \'%s\'@\'localhost\'; GRANT SELECT, LOCK TABLES ON *.* TO \'%s\'@\'127.0.0.1\'; GRANT SELECT, LOCK TABLES ON *.* TO \'%s\'@\'%%\'; FLUSH PRIVILEGES;' % (rUsername, rUsername, rUsername, rUsername, rUsername, rUsername)
    os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % grant_sql)
    
    # Create dashboard statistics table
    stats_sql = 'USE xtream_iptvpro; CREATE TABLE IF NOT EXISTS dashboard_statistics (id int(11) NOT NULL AUTO_INCREMENT, type varchar(16) NOT NULL DEFAULT \'\', time int(16) NOT NULL DEFAULT \'0\', count int(16) NOT NULL DEFAULT \'0\', PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=latin1; INSERT INTO dashboard_statistics (type, time, count) VALUES(\'conns\', UNIX_TIMESTAMP(), 0),(\'users\', UNIX_TIMESTAMP(), 0);'
    os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % stats_sql)
    
    # Test the created user
    printc("Testing database connection with new user")
    test_user_result = os.system('mysql -u %s -p%s -P 7999 -h 127.0.0.1 -e "USE xtream_iptvpro; SELECT COUNT(*) FROM reg_users;" > /dev/null 2>&1' % (rUsername, rPassword))
    if test_user_result != 0:
        printc("Failed to connect with new database user!", col.BRIGHT_RED)
        return False
    
    printc("Database configured successfully on port 7999", col.GREEN)
    
    # Cleanup database.sql file
    try: 
        os.remove("/home/xtreamcodes/iptv_xtream_codes/database.sql")
        printc("Cleaned up temporary files")
    except: 
        pass
        
    return True

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        rDecrypt = decrypt()
        rHost = rDecrypt["host"]
        rPassword = rDecrypt["db_pass"]
        rServerID = int(rDecrypt["server_id"])
        rUsername = rDecrypt["db_user"]
        rDatabase = rDecrypt["db_name"]
        rPort = int(rDecrypt["db_port"])
    printc("Encrypting...")
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass

    rf = open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb')
    lestring=''.join(chr(ord(c)^ord(k)) for c,k in zip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
    rf.write(base64.b64encode(bytes(lestring, 'ascii')))
    rf.close()

def decrypt():
    rConfigPath = "/home/xtreamcodes/iptv_xtream_codes/config"
    try: return json.loads(''.join(chr(c^ord(k)) for c,k in zip(base64.b64decode(open(rConfigPath, 'rb').read()), cycle('5709650b0d7806074842c6de575025b1'))))
    except: return None

def configure():
    printc("Configuring System")
    
    # Create all necessary directories first (REMOVED nginx_rtmp)
    printc("Creating required directories")
    required_dirs = [
        "/home/xtreamcodes/iptv_xtream_codes/streams",
        "/home/xtreamcodes/iptv_xtream_codes/tmp",
        "/home/xtreamcodes/iptv_xtream_codes/logs", 
        "/home/xtreamcodes/iptv_xtream_codes/tmp/client_temp",
        "/home/xtreamcodes/iptv_xtream_codes/tmp/proxy_temp",
        "/home/xtreamcodes/iptv_xtream_codes/tmp/fastcgi_temp",
        "/home/xtreamcodes/iptv_xtream_codes/tmp/uwsgi_temp",
        "/home/xtreamcodes/iptv_xtream_codes/tmp/scgi_temp",
        "/home/xtreamcodes/iptv_xtream_codes/tv_archive"
    ]
    
    for rDir in required_dirs:
        if not os.path.exists(rDir):
            os.makedirs(rDir, exist_ok=True)
    
    # Create essential log files
    log_files = [
        "/home/xtreamcodes/iptv_xtream_codes/logs/error.log",
        "/home/xtreamcodes/iptv_xtream_codes/logs/access.log",
        "/home/xtreamcodes/iptv_xtream_codes/logs/nginx_error.log",
        "/home/xtreamcodes/iptv_xtream_codes/logs/nginx_access.log"
    ]
    
    for log_file in log_files:
        if not os.path.exists(log_file):
            open(log_file, 'a').close()
    
    # Configure fstab for tmpfs
    fstab_content = open("/etc/fstab").read()
    if not "/home/xtreamcodes/iptv_xtream_codes/" in fstab_content:
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    
    # Configure sudoers
    sudoers_content = open("/etc/sudoers").read()
    if not "xtreamcodes" in sudoers_content:
        os.system('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables, /usr/bin/chattr" >> /etc/sudoers')
    
    # Create init script
    if not os.path.exists("/etc/init.d/xtreamcodes"):
        rFile = open("/etc/init.d/xtreamcodes", "w")
        rFile.write("#! /bin/bash\n/home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        rFile.close()
        os.system("chmod +x /etc/init.d/xtreamcodes > /dev/null")
    
    # Remove old ffmpeg link and create new one
    try: os.remove("/usr/bin/ffmpeg")
    except: pass
    
    if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg"):
        os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    
    # Download missing files
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb"): 
        printc("Downloading GeoLite2 database")
        os.system("wget -q https://raw.githubusercontent.com/Stefan2512/xtream-codes-ui-ioncube74/master/files/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php"): 
        printc("Downloading PID monitor")
        
        os.system("wget -q https://raw.githubusercontent.com/Stefan2512/xtream-codes-ui-ioncube74/master/files/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")
    
    # Set ownership and permissions
    printc("Setting permissions and ownership")
    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("chattr -ai /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sudo chmod 0777 /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    
    # Update start_services.sh and REMOVE nginx_rtmp references
    if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/start_services.sh"):
        os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        # Remove nginx_rtmp references from start script
        os.system("sed -i '/nginx_rtmp/d' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
    
    # Mount tmpfs filesystems
    printc("Mounting tmpfs filesystems")
    os.system("mount -a 2>/dev/null")
    
    # Secure config file
    if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/config"):
        os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config > /dev/null")
    
    # Redirect index.php
    if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php"):
        os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")
    
    # Update hosts file
    hosts_entries = [
        ("api.xtream-codes.com", "127.0.0.1    api.xtream-codes.com"),
        ("downloads.xtream-codes.com", "127.0.0.1    downloads.xtream-codes.com"),
        ("xtream-codes.com", "127.0.0.1    xtream-codes.com")
    ]
    
    hosts_content = open("/etc/hosts").read()
    for domain, entry in hosts_entries:
        if not domain in hosts_content:
            os.system('echo "%s" >> /etc/hosts' % entry)
    
    # Add crontab entry
    crontab_content = open("/etc/crontab").read()
    if not "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" in crontab_content:
        os.system('echo "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" >> /etc/crontab')
    
    printc("System configuration completed")

def start(first=True):
    if first: printc("Starting Xtream Codes UI with ION Cube 7.4")
    else: printc("Restarting Xtream Codes UI with ION Cube 7.4")
    os.system("/home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")

def modifyNginx():
    printc("Modifying Nginx")
    rPath = "/home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf"
    if not os.path.exists(rPath):
        printc("Nginx config not found, skipping modification")
        return
        
    rPrevData = open(rPath, "r").read()
    if not "listen 25500;" in rPrevData:
        shutil.copy(rPath, "%s.xc" % rPath)
        rData = "}".join(rPrevData.split("}")[:-1]) + "    server {\n        listen 25500;\n        index index.php index.html index.htm;\n        root /home/xtreamcodes/iptv_xtream_codes/admin/;\n\n        location ~ \.php$ {\n			limit_req zone=one burst=8;\n            try_files $uri =404;\n			fastcgi_index index.php;\n			fastcgi_pass php;\n			include fastcgi_params;\n			fastcgi_buffering on;\n			fastcgi_buffers 96 32k;\n			fastcgi_buffer_size 32k;\n			fastcgi_max_temp_file_size 0;\n			fastcgi_keep_conn on;\n			fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n			fastcgi_param SCRIPT_NAME $fastcgi_script_name;\n        }\n    }\n}"
        rFile = open(rPath, "w")
        rFile.write(rData)
        rFile.close()

def update(rType="MAIN"):
    if rType == "UPDATE":
        printc("Enter the link of release_xyz.zip file:", col.BRIGHT_RED)
        rlink = input('Example: https://github.com/Stefan2512/xtream-codes-ui-ioncube74/releases/download/v1.0/release_22f.zip\n\nNow enter the link:\n\n')
        
        printc("Downloading Software Update")  
        os.system('wget -q -O "/tmp/update.zip" "%s"' % rlink)
        if os.path.exists("/tmp/update.zip"):
            try: is_ok = zipfile.ZipFile("/tmp/update.zip")
            except:
                printc("Invalid link or zip file is corrupted!", col.BRIGHT_RED)
                os.remove("/tmp/update.zip")
                return False
        
        printc("Installing Admin Panel Update")
        if os.path.exists("/tmp/update.zip"):
            try: is_ok = zipfile.ZipFile("/tmp/update.zip")
            except:
                printc("Invalid link or zip file is corrupted!", col.BRIGHT_RED)
                os.remove("/tmp/update.zip")
                return False
            printc("Updating Software")
            os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null && rm -rf /home/xtreamcodes/iptv_xtream_codes/admin > /dev/null && rm -rf /home/xtreamcodes/iptv_xtream_codes/pytools > /dev/null && unzip -o /tmp/update.zip -d /tmp/update/ > /dev/null && cp -rf /tmp/update/XtreamUI-master/* /home/xtreamcodes/iptv_xtream_codes/ > /dev/null && rm -rf /tmp/update/XtreamUI-master > /dev/null && rm -rf /tmp/update > /dev/null && chown -R xtreamcodes:xtreamcodes /home/xtreamcodes/ > /dev/null && chmod +x /home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null && chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
            if not "sudo chmod 400 /home/xtreamcodes/iptv_xtream_codes/config" in open("/home/xtreamcodes/iptv_xtream_codes/permissions.sh").read(): os.system('echo "#!/bin/bash\nsudo chmod -R 777 /home/xtreamcodes 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/admin/ -type f -exec chmod 644 {} \; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/admin/ -type d -exec chmod 755 {} \; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/wwwdir/ -type f -exec chmod 644 {} \; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/wwwdir/ -type d -exec chmod 755 {} \; 2>/dev/null\nsudo chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx/sbin/nginx 2>/dev/null\nsudo chmod 400 /home/xtreamcodes/iptv_xtream_codes/config 2>/dev/null" > /home/xtreamcodes/iptv_xtream_codes/permissions.sh')
            os.system("/home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null")
            try: os.remove("/tmp/update.zip")
            except: pass
            return True
        printc("Failed to download installation file!", col.BRIGHT_RED)
        return False
    else:
        # Skip update for MAIN installation since archive already contains everything needed
        printc("Skipping admin panel update - using files from main archive")
        return True

if __name__ == "__main__":
    try: rVersion = os.popen('lsb_release -sr').read().strip()
    except: rVersion = None
    if not rVersion in rVersions:
        printc("Unsupported Operating System, Works only on Ubuntu Server 20")
        sys.exit(1)
    printc("Xtream Codes UI Ubuntu %s Installer with ION Cube 7.4 + Auto Updates" % rVersion, col.GREEN, 2)
    printc("✅ Zero configuration • ✅ Auto database setup • ✅ No RTMP conflicts • ✅ Auto-Update System", col.BRIGHT_YELLOW, 1)
    print(" ")
    rType = input("  Installation Type [MAIN, LB, UPDATE]: ")
    print(" ")
    
    # Convert to uppercase for case-insensitive comparison
    rType = rType.strip().upper()
    
    if rType in ["MAIN", "LB"]:
        if rType == "LB":
            rHost = input("  Main Server IP Address: ")
            rPassword = input("  MySQL Password: ")
            try: rServerID = int(input("  Load Balancer Server ID: "))
            except: rServerID = -1
            print(" ")
        else:
            rHost = "127.0.0.1"
            rPassword = generate()
            rServerID = 1
        rUsername = "user_iptvpro"
        rDatabase = "xtream_iptvpro"
        rPort = 7999
        if len(rHost) > 0 and len(rPassword) > 0 and rServerID > -1:
            printc("Start installation with ION Cube 7.4 + Auto Updates? Y/N", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                print(" ")
                rRet = prepare(rType)
                if not install(rType): sys.exit(1)
                if rType == "MAIN":
                    if not mysql(rUsername, rPassword): sys.exit(1)
                encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
                configure()
                if rType == "MAIN": 
                    modifyNginx()
                    # Install auto-update system
                    install_update_system()
                start()
                if rType == "MAIN":
                    printc("✅ Installation completed successfully! ✅", col.GREEN, 2)
                    printc("🌐 Admin Panel: http://%s:25500" % getIP(), col.BRIGHT_YELLOW)
                    printc("👤 Username: admin | 🔑 Password: admin", col.BRIGHT_YELLOW)
                    printc("🔐 MySQL Password: %s" % rPassword, col.BRIGHT_YELLOW)
                    printc("🚀 ION Cube 7.4 pre-installed and working!", col.BRIGHT_GREEN)
                    printc("🔔 Auto-Update System installed and active!", col.BRIGHT_CYAN)
                    printc("📄 All credentials saved to /root/credentials.txt", col.BRIGHT_CYAN)
                    rFile = open("/root/credentials.txt", "w")
                    rFile.write("=== XTREAM CODES UI INSTALLATION COMPLETED ===\n\n")
                    rFile.write("🌐 Admin Panel: http://%s:25500\n" % getIP())
                    rFile.write("👤 Username: admin\n")
                    rFile.write("🔑 Password: admin\n")
                    rFile.write("🔐 MySQL Password: %s\n" % rPassword)
                    rFile.write("🗄️ Database: xtream_iptvpro\n")
                    rFile.write("🚀 ION Cube: 7.4 (pre-installed)\n")
                    rFile.write("🔔 Auto-Updates: Enabled (checks every 30 minutes)\n")
                    rFile.write("📅 Installed: %s\n" % os.popen("date").read().strip())
                    rFile.write("\n=== NOTES ===\n")
                    rFile.write("• No RTMP conflicts - clean installation\n")
                    rFile.write("• All services auto-configured\n")
                    rFile.write("• Auto-update notifications in admin panel\n")
                    rFile.write("• Ready for production use\n")
                    rFile.close()
                else:
                    printc("✅ Load Balancer installation completed!", col.GREEN, 2)
            else: printc("Installation cancelled", col.BRIGHT_RED)
        else: printc("Invalid entries", col.BRIGHT_RED)
    elif rType == "UPDATE":
        if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/wwwdir/api.php"):
            printc("Update Admin Panel? Y/N", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                if not update(rType): sys.exit(1)
                printc("Update completed successfully!", col.GREEN, 2)
                start(False)
            else: printc("Update cancelled", col.BRIGHT_RED)
        else: printc("Install Xtream Codes Main server first!", col.BRIGHT_RED)
    else: printc("Invalid installation type", col.BRIGHT_RED)
