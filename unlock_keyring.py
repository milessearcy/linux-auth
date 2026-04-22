
import os
import subprocess
import paramiko
import ssh_connect

import pwd



def decryptPassword():
        try:
                stdin,stdout, stderr = client.exec_command(
                        f"age -d -i ~/.ssh/phone_auth_key -"
                )

                with open(f"/home/{user}/.ssh/encrypted_password", "rb") as f:
                        enryptedPassword = f.read()

                stdin.write(enryptedPassword)
                stdin.channel.shutdown_write()

                password = stdout.read()

        except Exception as e:
                with open("/tmp/auth_debug.log", "w") as f:
                        f.write(str(e))
                exit(1)
        
        try:
                with open("/tmp/unlock_debug.log", "w") as f:
                        f.write("attempting unlock\n")


                command = subprocess.run(
                        ["sudo", "-E", "-u", user, "gnome-keyring-daemon", "--unlock"],
                        input=password,
                        capture_output=True,
                        timeout= 5,
                        env={
                                **os.environ,
                                "DBUS_SESSION_BUS_ADDRESS": f"unix:path=/run/user/{uid}/bus",
                                "XDG_RUNTIME_DIR": f"/run/user/{uid}",
                        }
                )

                with open("/tmp/unlock_debug.log", "a") as f:
                        f.write("unlock done\n")



        except Exception as e:
                with open("/tmp/auth_debug2.log", "w") as f:
                        f.write(str(e))
                exit(101)
        
        return command




user = os.environ.get("PAM_USER")
uid = pwd.getpwnam(user).pw_uid

try: 
        with open (f"/tmp/phone_auth_{user}", "r") as f:
                flag = f.read()
except:
        exit(102)

else:
        if flag.strip() == "good":
                client = ssh_connect.return_client(user)
                command = decryptPassword()
                client.close()
finally:
        for f in ["/tmp/auth_debug.log", f"/tmp/signature_{user}", f"/tmp/phone_auth_{user}"]:
                try:
                        os.remove(f)
                except:
                        pass