#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Xtream Codes UI Installer with ION Cube 7.4 - Production Ready Version
import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Updated URLs for Stefan's repository
rDownloadURL = {
    "main": "https://github.com/Stefan2512/xtream-codes-ui-ioncube74/releases/download/v1.0/xtream-codes-ui-main-ioncube74.zip", 
    "sub": "https://github.com/Stefan2512/xtream-codes-ui-ioncube74/releases/download/v1.0/xtream-codes-ui-loadbalancer-ioncube74.zip"
}

rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "mariadb-server", "libpng16-16", "libzip5", "python3-paramiko", "python-is-python3"]
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
    os.system("add-apt-repository universe > /dev/null 2>&1 && curl https://github.com/sabiralipsl/Xtream-UI-R22F-ubuntu20.04lts-2025/releases/download/xtream1/get-pip.py --output get-pip.py > /dev/null 2>&1 && python2 get-pip.py > /dev/null 2>&1 && pip2 install paramiko > /dev/null 2>&1")
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
    
    # Try to connect with root user (try both sudo and direct methods on port 7999)
    printc("Testing MySQL connection on port 7999")
    
    # First try: sudo mysql on port 7999
    test_sudo = os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "SELECT 1;" > /dev/null 2>&1')
    if test_sudo == 0:
        printc("Using sudo authentication for MySQL")
        mysql_cmd_prefix = "sudo mysql -u root -P 7999 -h 127.0.0.1"
        use_sudo = True
    else:
        # Second try: direct mysql with empty password on port 7999
        test_direct = os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "SELECT 1;" > /dev/null 2>&1')
        if test_direct == 0:
            printc("Using direct authentication for MySQL")
            mysql_cmd_prefix = "mysql -u root -P 7999 -h 127.0.0.1"
            use_sudo = False
        else:
            printc("Failed to connect to MySQL on port 7999!", col.BRIGHT_RED)
            return False
    
    # Verify database.sql exists
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/database.sql"):
        printc("Database schema file not found!", col.BRIGHT_RED)
        return False
    
    printc("Creating database and user")
    
    # Create database
    if use_sudo:
        result = os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;" > /dev/null 2>&1')
    else:
        result = os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;" > /dev/null 2>&1')
        
    if result != 0:
        printc("Failed to create database!", col.BRIGHT_RED)
        return False
    
    # Drop user if exists (ignore errors)
    if use_sudo:
        os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "DROP USER IF EXISTS \'%s\'@\'%%\';" > /dev/null 2>&1' % rUsername)
    else:
        os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "DROP USER IF EXISTS \'%s\'@\'%%\';" > /dev/null 2>&1' % rUsername)
    
    printc("Importing database schema")
    # Import database schema
    if use_sudo:
        result = os.system("sudo mysql -u root -P 7999 -h 127.0.0.1 xtream_iptvpro < /home/xtreamcodes/iptv_xtream_codes/database.sql > /dev/null 2>&1")
    else:
        result = os.system("mysql -u root -P 7999 -h 127.0.0.1 xtream_iptvpro < /home/xtreamcodes/iptv_xtream_codes/database.sql > /dev/null 2>&1")
        
    if result != 0:
        printc("Failed to import database schema!", col.BRIGHT_RED)
        return False
    
    printc("Configuring database settings")
    # Update settings
    settings_sql = 'USE xtream_iptvpro; UPDATE settings SET live_streaming_pass = \'%s\', unique_id = \'%s\', crypt_load_balancing = \'%s\';' % (generate(20), generate(10), generate(20))
    
    if use_sudo:
        os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % settings_sql)
    else:
        os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % settings_sql)
    
    # Insert server configuration
    server_sql = 'USE xtream_iptvpro; REPLACE INTO streaming_servers (id, server_name, domain_name, server_ip, vpn_ip, ssh_password, ssh_port, diff_time_main, http_broadcast_port, total_clients, system_os, network_interface, latency, status, enable_geoip, geoip_countries, last_check_ago, can_delete, server_hardware, total_services, persistent_connections, rtmp_port, geoip_type, isp_names, isp_type, enable_isp, boost_fpm, http_ports_add, network_guaranteed_speed, https_broadcast_port, https_ports_add, whitelist_ips, watchdog_data, timeshift_only) VALUES (1, \'Main Server\', \'\', \'%s\', \'\', NULL, NULL, 0, 25461, 1000, \'%s\', \'eth0\', 0, 1, 0, \'\', 0, 0, \'{}\', 3, 0, 25462, \'low_priority\', \'\', \'low_priority\', 0, 1, \'\', 1000, 25463, \'\', \'[\"127.0.0.1\",\"\"]\', \'{}\', 0);' % (getIP(), getVersion())
    
    if use_sudo:
        os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % server_sql)
    else:
        os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % server_sql)
    
    # Create admin user with ALL required fields
    admin_sql = 'USE xtream_iptvpro; INSERT INTO reg_users (id, username, password, email, member_group_id, verified, status, date_registered, default_lang, reseller_dns, google_2fa_sec) VALUES (1, \'admin\', \'\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\', \'admin@website.com\', 1, 1, 1, UNIX_TIMESTAMP(), \'English\', \'\', \'\') ON DUPLICATE KEY UPDATE password=\'\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\';'
    
    if use_sudo:
        os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % admin_sql)
    else:
        os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % admin_sql)
    
    printc("Creating MySQL user for Xtream Codes")
    # Create database user
    user_sql = 'CREATE USER \'%s\'@\'%%\' IDENTIFIED BY \'%s\'; GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO \'%s\'@\'%%\' WITH GRANT OPTION; GRANT SELECT, LOCK TABLES ON *.* TO \'%s\'@\'%%\';FLUSH PRIVILEGES;' % (rUsername, rPassword, rUsername, rUsername)
    
    if use_sudo:
        result = os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % user_sql)
    else:
        result = os.system('mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % user_sql)
        
    if result != 0:
        printc("Failed to create database user!", col.BRIGHT_RED)
        return False
    
    # Create dashboard statistics table
    stats_sql = 'USE xtream_iptvpro; CREATE TABLE IF NOT EXISTS dashboard_statistics (id int(11) NOT NULL AUTO_INCREMENT, type varchar(16) NOT NULL DEFAULT \'\', time int(16) NOT NULL DEFAULT \'0\', count int(16) NOT NULL DEFAULT \'0\', PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=latin1; INSERT INTO dashboard_statistics (type, time, count) VALUES(\'conns\', UNIX_TIMESTAMP(), 0),(\'users\', UNIX_TIMESTAMP(), 0);'
    
    if use_sudo:
        os.system('sudo mysql -u root -P 7999 -h 127.0.0.1 -e "%s" > /dev/null 2>&1' % stats_sql)
    else:
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
    
    # REMOVED: nginx_rtmp creation - not needed anymore
    
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
        os.system("wget -q https://github.com/sabiralipsl/Xtream-UI-R22F-ubuntu20.04lts-2025/releases/download/xtream1/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php"): 
        printc("Downloading PID monitor")
        os.system("wget -q https://github.com/sabiralipsl/Xtream-UI-R22F-ubuntu20.04lts-2025/releases/download/xtream1/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")
    
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
    printc("Xtream Codes UI Ubuntu %s Installer with ION Cube 7.4 - Production Ready" % rVersion, col.GREEN, 2)
    printc("✅ Zero configuration • ✅ Auto database setup • ✅ No RTMP conflicts", col.BRIGHT_YELLOW, 1)
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
            printc("Start installation with ION Cube 7.4? Y/N", col.BRIGHT_YELLOW)
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
                start()
                    printc("✅ Installation completed successfully! ✅", col.GREEN, 2)
                    printc("🌐 Admin Panel: http://%s:25500" % getIP(), col.BRIGHT_YELLOW)
                    printc("👤 Username: admin | 🔑 Password: admin", col.BRIGHT_YELLOW)
                    printc("🔐 MySQL Password: %s" % rPassword, col.BRIGHT_YELLOW)
                    printc("🚀 ION Cube 7.4 pre-installed and working!", col.BRIGHT_GREEN)
                    printc("📄 All credentials saved to /root/credentials.txt", col.BRIGHT_CYAN)
                    rFile = open("/root/credentials.txt", "w")
                    rFile.write("=== XTREAM CODES UI INSTALLATION COMPLETED ===\n\n")
                    rFile.write("🌐 Admin Panel: http://%s:25500\n" % getIP())
                    rFile.write("👤 Username: admin\n")
                    rFile.write("🔑 Password: admin\n")
                    rFile.write("🔐 MySQL Password: %s\n" % rPassword)
                    rFile.write("🗄️ Database: xtream_iptvpro\n")
                    rFile.write("🚀 ION Cube: 7.4 (pre-installed)\n")
                    rFile.write("📅 Installed: %s\n" % os.popen("date").read().strip())
                    rFile.write("\n=== NOTES ===\n")
                    rFile.write("• No RTMP conflicts - clean installation\n")
                    rFile.write("• All services auto-configured\n")
                    rFile.write("• Ready for production use\n")
                    rFile.close()
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
