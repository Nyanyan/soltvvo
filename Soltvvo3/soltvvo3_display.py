import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.connect('10.1.2.3', username='foo', password='bar')