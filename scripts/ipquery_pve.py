#!/usr/bin/env python

from proxmoxer import ProxmoxAPI
from argparse import ArgumentParser
import yaml
import sys

def find_ip(proxmox_connection, node_name, vm_id):
    agent_status = proxmox_connection.nodes(node_name).qemu(vm_id).config.get()
    try:
        if (agent_status['agent']):
            ip = (proxmox.nodes(node_name).qemu(vm_id).agent.
                  create(command='network-get-interfaces'))
            for i in range(len(ip['result'])):
                for n in range(len(ip['result'][i]['ip-addresses'])):
                    if '192.' in (ip['result'][i]['ip-addresses']
                                  [n]['ip-address']):
                        return(ip['result'][i]['ip-addresses']
                               [n]['ip-address'])
    except:
        pass


if __name__ == '__main__':
    stream = open("../.cred/pve.yml").read()
    creds = yaml.safe_load(stream)
            
    proxmox = ProxmoxAPI(creds['pve_host'], user=creds['pve_user'],
                         password=creds['pve_password'], verify_ssl=False)
    parser = ArgumentParser(description='Find VM IP')
    parser.add_argument('-v', '--vmid', required=False,
                        help='VM id')
    args = parser.parse_args()
    
    node_inventory_dict = {}

    for vm in proxmox.cluster.resources.get(type='vm'):
        #print("{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status']))
        if str(vm['name']).startswith('testdkr') and not str(vm['name']).endswith('master'):
            node_inventory_dict[vm['name']] = find_ip(proxmox, creds['pve_node'], vm['vmid'])

    fh = open("inventory", "w") 
    fh.write("[nodes]\n")
    for k, v in node_inventory_dict.items():
        inv_line = "%s ansible_host=%s ansible_user=root ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n" % (k, v)
        fh.write(inv_line)

    fh.write("\n")
    fh.close()

#print(find_ip(proxmox, creds['pve_node'], args.vmid))

