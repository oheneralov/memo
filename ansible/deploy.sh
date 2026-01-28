#!/bin/bash
# Deployment script for on-premises Node.js servers
# This script runs the Ansible playbook with appropriate settings

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========== Node.js On-Premises Deployment ==========${NC}"

# Check prerequisites
if ! command -v ansible-playbook &> /dev/null; then
    echo -e "${RED}Error: ansible-playbook not found. Please install Ansible.${NC}"
    exit 1
fi

# Configuration
INVENTORY_FILE="${1:-inventory-onprem.ini}"
PLAYBOOK_FILE="${2:-deploy-nodejs-onprem.yml}"
DRY_RUN="${3:-false}"

# Validate files exist
if [ ! -f "$INVENTORY_FILE" ]; then
    echo -e "${RED}Error: Inventory file '$INVENTORY_FILE' not found${NC}"
    exit 1
fi

if [ ! -f "$PLAYBOOK_FILE" ]; then
    echo -e "${RED}Error: Playbook file '$PLAYBOOK_FILE' not found${NC}"
    exit 1
fi

echo -e "${YELLOW}Inventory: $INVENTORY_FILE${NC}"
echo -e "${YELLOW}Playbook: $PLAYBOOK_FILE${NC}"

# Test connectivity to all hosts
echo -e "\n${YELLOW}Testing connectivity to on-premises servers...${NC}"
ansible all -i "$INVENTORY_FILE" -m ping

if [ "$DRY_RUN" = "true" ]; then
    echo -e "\n${YELLOW}Running in CHECK MODE (dry run)...${NC}"
    ansible-playbook -i "$INVENTORY_FILE" "$PLAYBOOK_FILE" --check -vv
else
    echo -e "\n${YELLOW}Running deployment...${NC}"
    ansible-playbook -i "$INVENTORY_FILE" "$PLAYBOOK_FILE" -v
fi

echo -e "\n${GREEN}========== Deployment Script Complete ==========${NC}"
