# Ansible Node.js Deployment Examples

## Overview
This folder contains Ansible playbooks and roles for deploying a Node.js application to **multiple on-premises servers** with the following steps:
1. **Zip** - Archive the Node.js application
2. **Copy** - Transfer the zipped file to remote host(s)
3. **Unzip** - Extract the application on remote host
4. **Build** - Install dependencies and run build script
5. **Run** - Start the Node.js application

Supports parallel deployment to multiple on-premises machines with health checks and rolling updates.

## Files

### Main Playbooks

#### `deploy-nodejs.yml`
A standalone playbook that performs all deployment steps in one file. Best for simple single-server deployments.

**Usage:**
```bash
ansible-playbook deploy-nodejs.yml -i inventory.ini
```

#### `deploy-nodejs-roles.yml`
A playbook using Ansible roles for better organization and reusability. Best for simple multi-server setups.

**Usage:**
```bash
ansible-playbook deploy-nodejs-roles.yml -i inventory.ini
```

#### `deploy-nodejs-onprem.yml` ⭐ (Recommended for On-Premises)
Optimized playbook for deploying to **multiple on-premises servers** with:
- Parallel deployment support
- Health checks across all servers
- Deployment summary report
- Proper host grouping and orchestration

**Usage:**
```bash
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini -v
```

#### `update-nodejs-onprem.yml`
Rolling update playbook for on-premises servers with:
- One server at a time updates (zero downtime)
- Automatic backups before update
- Health verification after each update

**Usage:**
```bash
ansible-playbook update-nodejs-onprem.yml -i inventory-onprem.ini -v
```

### Inventory Files

#### `inventory-onprem.ini`
Pre-configured inventory for on-premises servers with:
- Multiple app servers group
- SSH configuration
- Sudo/become settings
- Optional load balancer group

Edit this file with your actual on-premises server IPs and hostnames.

### Configuration Files

#### `ansible.cfg`
Ansible configuration file optimized for on-premises deployment with:
- Optimized SSH settings
- Fact caching for performance
- Connection timeout settings
- Logging configuration

#### `deploy.sh`
Bash script wrapper for easy deployment with:
- Connectivity testing
- Dry-run (check mode) support
- Colored output
- Error handling

**Usage:**
```bash
chmod +x deploy.sh
./deploy.sh inventory-onprem.ini deploy-nodejs-onprem.yml
./deploy.sh inventory-onprem.ini deploy-nodejs-onprem.yml true  # dry-run
```

### Roles

#### `roles/deploy_app/`
- **Purpose**: Handles zipping, copying, and extracting the application
- **Tasks**: Archive creation, file transfer, extraction

#### `roles/build_app/`
- **Purpose**: Installs Node.js, npm packages, and runs build scripts
- **Tasks**: Node.js installation, npm install, build process

#### `roles/run_app/`
- **Purpose**: Starts the Node.js application and performs health checks
- **Tasks**: Application startup, port waiting, health verification

## Prerequisites

### On Control Machine (where Ansible runs)
- Ansible >= 2.9
- SSH access to target hosts
- Python 3

### On Target Hosts
- Python 2.7+ or Python 3.5+
- SSH server running
- Sudo privileges (for `become: yes`)

## Configuration

### Variables
All playbooks use the following variables (defined in `vars` section):

| Variable | Default | Description |
|----------|---------|-------------|
| `app_name` | `nodejs_app` | Application name |
| `app_source_path` | `../app` | Path to local app (relative to playbook) |
| `app_dest_path` | `/opt/nodejs_app` | Deployment path on remote |
| `nodejs_port` | `3000` | Port for Node.js app |

### Inventory File Examples

#### For Single/Few Servers (inventory.ini)
```ini
[nodejs_servers]
server1.example.com
server2.example.com

[nodejs_servers:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

#### For Multiple On-Premises Servers (inventory-onprem.ini)
```ini
[nodejs_app_servers]
app-server-1 ansible_host=192.168.1.10 ansible_user=ubuntu
app-server-2 ansible_host=192.168.1.11 ansible_user=ubuntu
app-server-3 ansible_host=192.168.1.12 ansible_user=ubuntu

[nodejs_app_servers:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_become=True
nodejs_port=3000
```

## Usage Examples

### On-Premises Multi-Server Deployment

#### Full deployment (recommended)
```bash
# Test connectivity first
ansible all -i inventory-onprem.ini -m ping

# Run deployment
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini -v
```

#### Using the deployment script
```bash
chmod +x deploy.sh
./deploy.sh inventory-onprem.ini deploy-nodejs-onprem.yml
```

#### Dry run (check mode)
```bash
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini --check -vv
./deploy.sh inventory-onprem.ini deploy-nodejs-onprem.yml true
```

#### Deploy to specific server group
```bash
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini -l nodejs_app_servers
```

### Rolling Update to Multiple Servers
```bash
# Updates one server at a time (zero downtime)
ansible-playbook update-nodejs-onprem.yml -i inventory-onprem.ini -v
```

### Single Server Deployment
```bash
ansible-playbook deploy-nodejs.yml -i inventory.ini -l server1.example.com
```

### Deploy with custom variables
```bash
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini \
  -e "nodejs_port=8080" \
  -e "app_source_path=/home/user/myapp"
```

### Deploy with verbose output
```bash
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini -vvv
```

## Application Requirements

Your Node.js application should have:
- `package.json` file with dependencies
- `npm start` script to run the application
- Optional: `npm run build` script for building

Example `package.json`:
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node app.js",
    "build": "echo 'Building...'"
  },
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

## Troubleshooting

### Connection Issues
```bash
# Test SSH connectivity to all hosts
ansible all -i inventory-onprem.ini -m ping

# Test with verbose SSH
ansible-playbook deploy-nodejs-onprem.yml -i inventory-onprem.ini -vvv

# Test SSH directly
ssh -i ~/.ssh/id_rsa ubuntu@192.168.1.10
```

### SSH Key Issues
```bash
# Fix permissions
chmod 600 ~/.ssh/id_rsa

# Add key to ssh-agent
ssh-add ~/.ssh/id_rsa

# Test key authentication
ssh -i ~/.ssh/id_rsa -v ubuntu@192.168.1.10
```

### View Application Logs on Remote Server
```bash
# SSH to remote host and check logs
ssh ubuntu@192.168.1.10 'tail -f /var/log/nodejs_app.log'

# Or using Ansible
ansible nodejs_app_servers -i inventory-onprem.ini -m command -a "tail -20 /var/log/nodejs_app.log"
```

### Health Check
```bash
# Check application on specific host
curl http://192.168.1.10:3000

# Check all servers
ansible nodejs_app_servers -i inventory-onprem.ini -m uri -a "url=http://localhost:3000 method=GET"
```

### Stop/Restart Application
```bash
# Restart on all servers
ansible nodejs_app_servers -i inventory-onprem.ini -m shell -a "pkill -f 'npm start' && sleep 2"

# Restart specific server
ansible app-server-1 -i inventory-onprem.ini -m shell -a "cd /opt/nodejs_app && nohup npm start > /var/log/nodejs_app.log 2>&1 &"
```

### Process Status
```bash
# Check if app is running on all servers
ansible nodejs_app_servers -i inventory-onprem.ini -m shell -a "ps aux | grep 'npm start' | grep -v grep"
```

## Notes
- The playbooks assume the application path exists locally
- Applications are run with `nohup` to ensure they continue running after SSH disconnect
- Logs are written to `/var/log/nodejs_app.log` on remote hosts
- The `become: yes` directive requires sudo privileges on remote hosts
- For on-premises deployment, use `deploy-nodejs-onprem.yml` with `inventory-onprem.ini`
- Serial deployment (default: 2 servers at a time) prevents all servers from being unavailable simultaneously
- Health checks verify the application is running after deployment
- Rolling updates deploy to one server at a time for zero downtime

## On-Premises Architecture

```
Control Machine (Ansible)
    |
    +--- SSH ---> App Server 1 (192.168.1.10)
    +--- SSH ---> App Server 2 (192.168.1.11)
    +--- SSH ---> App Server 3 (192.168.1.12)
    
Optional Load Balancer
    +--- App Server 1 (Port 3000)
    +--- App Server 2 (Port 3000)
    +--- App Server 3 (Port 3000)
```

## Performance Tuning

### Adjust parallel deployment speed
Edit `deploy-nodejs-onprem.yml` `serial` parameter:
```yaml
serial: 2  # Deploy to 2 servers at a time
```

### Adjust fact caching
Edit `ansible.cfg`:
```ini
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
```

### Increase SSH parallelism
Edit `ansible.cfg`:
```ini
forks = 10  # Default is 5, increase for faster parallel execution
```
