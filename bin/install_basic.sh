#!/bin/bash
if [ $EUID -ne 0 ]; then
   echo "This script must be run as root" 
   exit 1
fi

if grep -qi ubuntu /etc/os-release; then
    apt-get -q update 
else
    echo 'WARN: Could not detect Ubuntu Distro'
    exit 1
fi 

if [ ! "$(which git)" ]; then
        apt-get -q --yes install git-all 
else
    echo "Git already installed"
fi 
if [ ! "$(which ansible-playbook)" ]; then
    apt install -q software-properties-common --yes
    apt-add-repository -q --yes --update ppa:ansible/ansible
    apt install -q ansible --yes
else
    echo "Ansible already installed"
fi

if [ d foo ]; then
    mkdir -p '/etc/pilink'
else
    echo "/etc/pilink already exists, deleting contents"
    rm -rf /etc/pilink/*
fi

git clone -q https://github.com/YouFoundKyle/Pi-LINk.git /etc/pilink/

#Install required collections
ansible-galaxy collection install -r /etc/pilink/playbooks/requirements.yml 

#Begin ansible run
ansible-playbook /etc/pilink/playbooks/main.yml