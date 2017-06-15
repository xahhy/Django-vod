#ubuntu apt-get has errors
rm -rf /var/lib/dpkg/info

#remote connect mysql
1. vim /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address		= 0.0.0.0

2. mysql -uroot -p123
> GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY '123' WITH GRANT OPTION;
> flush privileges;
