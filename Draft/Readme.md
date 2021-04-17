## SQL init codes <br>
create table reports(email varchar(30), dustbin_status varchar(20), photo longblob, date varchar(30), time varchar(30), loc varchar(30), dustbinID int);<br>
create table dustbinlist (dustbinID int not null primary key, area varchar(20), weight int, reports_number int, AvgWt float8);
create table workerlogin (BMC_ID int not null primary key, password varchar (20), area varchar (20), name varchar (20));
