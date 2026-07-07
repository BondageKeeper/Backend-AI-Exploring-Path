*Step 1:

* **Connect to the server (in Windows `cmd`):** `ssh root@WRITE HERE IP OF SERVER`  *(Password: `ALSO YOU HAVE PASSWORD OF THIS SERVER`)*
* **Navigate to the project folder on the server:** `cd /root/my_project`
* **Full restart and rebuild of Docker containers:** `docker compose down && docker compose up -d --build`
* **Check Python logs and backend errors:** `docker compose logs pcbang_backend`
