import os
import subprocess
import paramiko


#opens config file
def return_client(user):
    try:
            config = paramiko.SSHConfig()
            with open((f"/home/{user}/.ssh/config")) as f:
                    config.parse(f)
    except Exception as e:
            with open("/tmp/auth_debug.log", "w") as f:
                    f.write(str(e))
            exit(1)

    #phone connects
    try:
            host_config = config.lookup("phone-auth")

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(
                    hostname= host_config["hostname"],
                    username=host_config["user"],
                    key_filename=host_config["identityfile"][0],
                    port=host_config["port"],
                    timeout=5
            )
    except Exception as e:
            with open("/tmp/auth_debug.log", "w") as f:
                    f.write(str(e))
            exit(2)
    
    return client