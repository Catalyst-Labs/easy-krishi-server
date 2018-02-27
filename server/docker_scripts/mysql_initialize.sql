#create user if not exists 'easykrishi' identified by 'easykrishi_pwd';
create user if not exists 'easykrishi'@'%' identified by 'easykrishi_pwd';
#create user if not exists 'easykrishi'@'localhost' identified by 'easykrishi_pwd';
select User,Host from mysql.user;

create database if not exists easykrishi;
grant all on easykrishi.* to 'easykrishi'@'%';
flush privileges;
commit;

