Load a backup

```
docker stop domserver
cat ~/sql-backup-files/bcpc-3-2.sql | docker exec -i dj-mariadb mariadb -u root -p1f7HO2d6Sn
docker start domserver
```

```
# docker cp ~/sql-backup-files/backup.sql dj-mariadb:/
# docker exec -it dj-mariadb bash
# mariadb -u root -p1f7HO2d6Sn < /backup.sql
```

Reset admin password
```
docker exec domserver /opt/domjudge/domserver/webapp/bin/console domjudge:reset-user-password admin
```
