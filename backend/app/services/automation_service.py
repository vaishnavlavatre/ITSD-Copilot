import subprocess
from typing import Dict, List, Optional

class AutomationService:
    def __init__(self):
        # Safe commands that can be executed
        self.safe_commands = {
            'disk_space': 'df -h',
            'memory_usage': 'free -h',
            'process_list': 'ps aux',
            'system_uptime': 'uptime',
            'logged_in_users': 'who'
        }

    def execute_safe_command(self, command_key: str) -> Dict[str, str]:
        """Execute predefined safe commands (simulated for now)"""
        if command_key not in self.safe_commands:
            return {"error": f"Command {command_key} not in safe commands list"}
        
        # For safety, we'll simulate command execution
        # In production, you might actually run these commands
        simulated_outputs = {
            'disk_space': "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        20G   15G  4.5G  77% /\n",
            'memory_usage': "              total        used        free      shared  buff/cache   available\nMem:           7.7G        2.1G        3.2G        256M        2.4G        5.1G\nSwap:          2.0G          0B        2.0G",
            'process_list': "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot         1  0.0  0.0 169316 13128 ?        Ss   10:00   0:01 /sbin/init",
            'system_uptime': "10:00:30 up 2 days,  3:15,  1 user,  load average: 0.05, 0.10, 0.15",
            'logged_in_users': "user1    pts/0        2023-12-01 09:30 (192.168.1.100)"
        }
        
        return {
            "output": simulated_outputs.get(command_key, "Command executed successfully"),
            "command": self.safe_commands[command_key]
        }

    def generate_command_sequence(self, intent: str, entities: Dict) -> Optional[List[Dict]]:
        """Generate step-by-step command sequences for common tasks"""
        sequences = {
            'restart_apache': [
                {
                    "command": "sudo systemctl status apache2", 
                    "description": "Check current Apache status"
                },
                {
                    "command": "sudo systemctl restart apache2", 
                    "description": "Restart Apache service"
                },
                {
                    "command": "sudo systemctl status apache2", 
                    "description": "Verify Apache is running"
                }
            ],
            'check_disk_usage': [
                {
                    "command": "df -h", 
                    "description": "Check disk space usage"
                },
                {
                    "command": "du -sh /var/log/*", 
                    "description": "Check log directory sizes"
                }
            ],
            'user_creation': [
                {
                    "command": "sudo useradd -m username", 
                    "description": "Create new user with home directory"
                },
                {
                    "command": "sudo passwd username", 
                    "description": "Set password for new user"
                },
                {
                    "command": "sudo usermod -aG groupname username", 
                    "description": "Add user to group (optional)"
                }
            ],
            'troubleshoot_permission': [
                {
                    "command": "ls -l /path/to/file", 
                    "description": "Check current file permissions"
                },
                {
                    "command": "chmod 755 /path/to/file", 
                    "description": "Set appropriate permissions"
                },
                {
                    "command": "chown user:group /path/to/file", 
                    "description": "Change ownership if needed"
                }
            ]
        }
        
        # Determine which sequence to use based on intent and entities
        if intent == 'troubleshooting' and 'error_code' in entities:
            if 'permission' in str(entities.get('error_code', [])).lower():
                return sequences['troubleshoot_permission']
        
        if 'software_name' in entities:
            software = entities['software_name'][0].lower()
            if software == 'apache':
                return sequences['restart_apache']
        
        if intent == 'user_management':
            return sequences['user_creation']
        
        if intent == 'status_check':
            return sequences['check_disk_usage']
        
        return None