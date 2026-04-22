#!/usr/bin/python3

import os
import subprocess
import paramiko
import ssh_connect

user = os.environ.get("PAM_USER")

client = ssh_connect.return_client(user)

def badNotif():
        try:
                stdin,stdout, stderr = client.exec_command(
                        f"termux-notification -t 'Failed Linux Loggin Attempted' -c ' '"
                )
        except:
                pass

#sends challenge and receives sig
try:
        challenge = os.urandom(32).hex()

        stdin,stdout, stderr = client.exec_command(
                f"ssh-keygen -Y sign -f ~/.ssh/phone_auth_key -n challenge --"
        )


        stdin.write(challenge)
        stdin.channel.shutdown_write()

        signature = stdout.read()
except Exception as e:
        with open("/tmp/auth_debug.log", "w") as f:
                f.write(str(e))
        badNotif()
        exit(3)


#tries to save sig to file
try:
        with open(f"/tmp/signature_{user}", "wb") as f:
                f.write(signature)

except Exception as e:
        with open("/tmp/auth_debug.log", "w") as f:
                f.write(str(e))
        badNotif()
        exit(4)



#varify sig
try:
        command = ["ssh-keygen", "-Y", "verify", "-f",(f"/home/{user}/.ssh/allowed_signers"), "-I", "phone", "-n", "challenge", "-s", f"/tmp/signature_{user}"]

        verrication = subprocess.run(command, input=(challenge).encode(), capture_output=True)

        if verrication.returncode == 0:


                stdin,stdout, stderr = client.exec_command(
                        f"termux-notification -t 'Successful Linux Loggin Attempted' -c '{verrication.returncode}'"
                )
                
                with open(f"/tmp/phone_auth_{user}", "w") as f:
                        f.write("good")
        else:
                stdin,stdout, stderr = client.exec_command(
                        f"termux-notification -t 'Failed Linux Loggin Attempted' -c '{verrication.returncode}'"
                )

        client.close()


        

        exit(verrication.returncode)
except Exception as e:
        badNotif()
        exit(7)

