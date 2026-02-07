# Ansible Lab

This lab contains 4 playbooks and examples of `host_vars` and host files for Cisco Catalyst8k.

## Important

If this is your first SSH connection to the Catalyst8k, run the playbook `add_ssh_key.yaml` and make sure to update the IP address in the `vars` section of the playbook.

## Playbooks Included

- `add_ssh_key.yaml`: Add Catalyst8k SSH key to `known_hosts`
- `add_users.yaml`: Create users on Catalyst8k
- `add_ip_int.yaml`: Configure interfaces on Catalyst8k
- `sh_int_name.yaml`: Show interface information in JSON format

## Note on Secrets

Passwords and sensitive information are stored in Ansible Vault in your local environment.  
Example files (`*.example.yaml`) are provided in this repo for reference.

## Usage Example

Run the playbooks with:

```bash
ansible-playbook playbooks/add_ssh_key.yaml
ansible-playbook playbooks/add_users.yaml
ansible-playbook playbooks/add_ip_int.yaml
ansible-playbook playbooks/sh_int_name.yaml
