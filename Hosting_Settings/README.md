*Step 2:

* **Connect to the server** (in Windows `cmd`): `ssh root@45.146.164.146`
* **Navigate to the project folder on the server**: `cd /root/my_project`
* **Replace local IP with server IP in HTML file**: `sed -i 's/127.0.0.1/45.146.164.146/g' frontend/main_cover.html`
* **Full restart and rebuild of Docker containers**: `docker compose down -v && docker compose up -d --build --force-recreate`
* **Check Python logs and backend errors**: `docker compose logs pcbang_backend`
* **IMPORTANT: Hard reload page in browser to clear cache**: Press `Ctrl + Shift + R` (or `Ctrl + F5`)
