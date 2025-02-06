show databases;
create database typingspeed;
use typingspeed;
show tables;

desc user_details;
desc user_stats;
desc games;


truncate user_details;
truncate user_stats;
truncate games;

drop table games;
drop table user_stats;
drop table user_details;
drop table word_list;


-- create table user_stats (userid int , foreign key (userid) references user_details(id) , wpm int);

insert into user_details values ('Joe Byjo', 18, 'joe', '1234') ;



update user_stats set highscore_nWPM=20,highscore_gWPM=23,highscore_time=2.3,average_WPM=52.5,average_accuracy=100.0,average_time=3.5 where userid = 1;



select * from user_details;
select * from user_stats;
select * from games;-- order by netWPM asc;	
select * from word_list;

ALTER TABLE user_details MODIFY id int primary key auto_increment,modify username varchar(15) unique;
ALTER TABLE user_stats MODIFY userid int,add foreign key(userid) references user_details(id);
ALTER TABLE games MODIFY gameid int primary key auto_increment, modify userid int,add foreign key(userid) references user_details(id);


select username,highscore_nWPM,highscore_gWPM,highscore_time,average_WPM, average_time,average_accuracy from user_stats as b, user_details as a where a.id = b.userid order by highscore_nWPM DESC ;
select id , username from user_details;
select * from user_stats as b,user_details as a where a.id = b.userid;
select name, username, highscore_nWPM as highscore from user_stats as a inner join user_details as b on a.userid = b.id;
select round(avg(timetaken),1) from games where userid =1;
select max(netWPM),max(grossWPM),min(timetaken),round(avg(netWPM)),round(avg(timetaken),1),round(avg(accuracy),1) from games where userid = 1;
select count(*) from games where userid =7;




