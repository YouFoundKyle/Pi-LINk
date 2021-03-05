#Install required collections
ansible-galaxy collection install -r /etc/pilink/playbooks/requirements.yml 

#Begin ansible run
ansible-playbook /etc/pilink/playbooks/main.yml