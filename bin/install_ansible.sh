#!/bin/bash
if [ $EUID -ne 0 ]; then
   echo "This script must be run as root" 
   exit 1
fi

if grep -qi ubuntu /etc/os-release; then
    apt-get update -q
else
    echo 'WARN: Could not detect Ubuntu Distro'
    exit 1
fi 

if [! "$(which git)"]; then
        apt-get install git-all --yes
else
    echo "Git already installed"
fi 
if [ ! "$(which ansible-playbook)" ]; then
    apt install software-properties-common
    apt-add-repository --yes --update ppa:ansible/ansible
    apt install ansible --yes
else
    echo "Ansible already installed"
fi

mkdir -p '/etc/pilink'
git clone -q https://github.com/YouFoundKyle/Pi-LINk.git /etc/pilink/
ansible-playbook /etc/pilink/ansible/initial.yml