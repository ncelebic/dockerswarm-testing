# dockerswarm-testing

Running setupvenv.sh sets up the virtualenv, but does not leave your shell in the venv.  Use `source ./setupvenv.sh` to stay in the venv.

Manually go into Proxmox and install a master CentOS node called `testdkr-master`.  Use `ssh-copy-id` to copy your key to the root user.  Record the IP for the master in the inventory_master file.  Now run `ansible-playbook -i inventory_master setup_master.yml`  This will reboot the VM.  When it comes back up, you should see it's IP address in the Summary tab in Proxmox.  If you see it, you are done setting up the master.  Shut it down, and convert it to a template.

Copy creds.yml.example to creds.yml and fill in your proxmox details.

Run `ansible-playbook -i pveinventory setup-vms.yml` to bring up the node VMs.  If Proxmox is being slow and doesn't start them all, just run the playbook again.  Run `scripts/ipquery_pve.py`  This will generate an inventory file with the IPs of your VMs.  If you have a big environment, please double check `inventory`  

Run `ansible-playbook -i inventory bootstrap.yml` to setup the VMs.  Now run `ansible-playbook -i inventory start-nodes-nofacts.yml` to start the cluster.  You should now have a fully operational swarm cluster.  SSH to any node and run `docker node ls` to verify.

## Help, I screwed up the swarm!

Run `ansible-playbook -i inventory reset-swarm` and then re-run `ansible-playbook -i inventory start-nodes-nofacts.yml`

This will make all the nodes leave the swarm and then make a new one.
