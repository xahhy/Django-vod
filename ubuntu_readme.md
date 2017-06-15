# ubuntu apt-get has errors
rm -rf /var/lib/dpkg/info

# remote connect mysql
1. vim /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address		= 0.0.0.0

2. mysql -uroot -p123
> GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY '123' WITH GRANT OPTION;
> flush privileges;

# add auto-start script in ubuntu
1. create a new service file:
new_service.sh

2. add permission to this file:
sudo chmod 755 new_service.sh

3. copy file to /etc/init.d/
sudo mv new_sercvice.sh /etc/init.d/

4. change script to auto-start
cd /etc/init.d/
sudo update-rc.d new_service.sh defaults 90

- remove script from auto-start
sudo update-rc.d -f new_service.sh remove

