show databases;

use ytube_data;

show tables;

drop table if exists agg_trans;

create table agg_trans (id int);

select * from test2;

create database phonepe_data;

select count(*) from agg_trans;

select * from agg_trans limit 20;

create table agg_trans(
	states varchar(500),
    years varchar(20),
    quarters varchar(10),
    transaction_name varchar(500),
    transaction_count bigint,
    transaction_amount float
    );
    
create table if not exists agg_users(
	states varchar(500),
    years varchar(20),
    quarters varchar(10),
    brands varchar(500),
    transaction_count bigint,
    percentage float
    );    
    
create table if not exists map_trans(
	states varchar(500),
    years varchar(20),
    quarters varchar(10),
    districts varchar(500),
    transaction_count bigint,
    transaction_amount float
    );    
    
create table if not exists map_users(
	states varchar(500),
    years varchar(20),
    quarters varchar(10),
    districts varchar(500),
    registered_users bigint,
    app_opens bigint
    );      
    
select * from map_trans limit 20;   

select * from top_trans limit 20; 

select * from top_users limit 20;
    
drop table if exists map_trans;    

use phonepe_data;

show tables;

insert into test2 values(3);

show tables;

select distinct years from agg_trans order by years;

select transaction_name, sum(transaction_count) as transaction_count,  format(round(sum(transaction_amount), 2),2) as transaction_amount
from agg_trans 
where years in ('2019', '2020')
and states = 'andaman-&-nicobar-islands'
group by transaction_name;

show tables;

select * from questions;

truncate table questions;

insert into questions values (2, '2. Aggregated Transactions by states');

select distinct states from agg_trans;

select * from states;

select states, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from agg_trans 
                                group by states;
                                
select s.map_state as states, sum(a.transaction_count) as transaction_count,  round(sum(a.transaction_amount), 2) as transaction_amount
                                from agg_trans a
                                join states s
                                on a.states=s.existing_state
                                group by s.map_state;    

create view vw_agg_trans as
	select s.map_state, a.* from agg_trans a
    join states s
    on a.states = s.existing_state;

create view vw_agg_users as
	select s.map_state, a.* from agg_users a
    join states s
    on a.states = s.existing_state;

create view vw_map_trans as
	select s.map_state, a.* from map_trans a
    join states s
    on a.states = s.existing_state;

create view vw_map_users as
	select s.map_state, a.* from map_users a
    join states s
    on a.states = s.existing_state;

create view vw_top_trans as
	select s.map_state, a.* from top_trans a
    join states s
    on a.states = s.existing_state;

create view vw_top_users as
	select s.map_state, a.* from top_users a
    join states s
    on a.states = s.existing_state;

select map_state as states, brands, sum(transaction_count) as transaction_count,  round(avg(percentage), 2) as percentage
                                from vw_agg_users
                                #where years in ('{yr_selected}')
                                group by map_state, brands;

select * from vw_agg_users ;

show databases;

use phonepe_data;

select * from questions;
#delete from questions where question_id = 3;

insert into questions values (6, '6. Map Transactions and Users');

select * from vw_agg_trans;

select distinct years from vw_agg_trans;

select * from questions;

delete from questions where question_name = '6. Aggregated Transactions by Years';

insert into questions values (10, '10. Registered users by states');

update questions set question_name = '4. Transactions by Districts' where question_id = 4;

update questions set question_name = '5. Registered Users by Districts' where question_id = 5;

update questions set question_name = '6. Transactions and Users by districts' where question_id = 6;

select * from vw_map_users;

select * from questions;

with cte as (
	select map_state, years, transaction_name, sum(transaction_count) as transaction_count from vw_agg_trans
	group by map_state, years, transaction_name
)
select 
	map_state,
    transaction_name,
    sum(case years when '2018' then transaction_count end) as '2018',
    sum(case years when '2019' then transaction_count end) as '2019', 
    sum(case years when '2020' then transaction_count end) as '2020',
    sum(case years when '2021' then transaction_count end) as '2021',
    sum(case years when '2022' then transaction_count end) as '2022',
    sum(case years when '2023' then transaction_count end) as '2023'
 from cte
 group by 
 	map_state,
    transaction_name;
    
with cte as (
	select map_state, years, brands, sum(transaction_count) as transaction_count from vw_agg_users
	group by map_state, years, brands
)
select 
	map_state,
    brands,
    sum(case years when '2018' then transaction_count end) as '2018',
    sum(case years when '2019' then transaction_count end) as '2019', 
    sum(case years when '2020' then transaction_count end) as '2020',
    sum(case years when '2021' then transaction_count end) as '2021',
    sum(case years when '2022' then transaction_count end) as '2022',
    sum(case years when '2023' then transaction_count end) as '2023'
 from cte
 group by 
 	map_state,
    brands;    
    
select * from vw_top_users;
    
with cte as (
	select map_state, years, districts, sum(registered_users) as registered_users from vw_top_users
	group by map_state, years, districts
)
select 
	map_state,
    districts,
    sum(case years when '2018' then registered_users end) as '2018',
    sum(case years when '2019' then registered_users end) as '2019', 
    sum(case years when '2020' then registered_users end) as '2020',
    sum(case years when '2021' then registered_users end) as '2021',
    sum(case years when '2022' then registered_users end) as '2022',
    sum(case years when '2023' then registered_users end) as '2023'
 from cte
 group by 
 	map_state,
    districts;    

select * from vw_agg_users;
select * from vw_top_trans;

select s.map_state, a.* from agg_users a
    left join states s
    on a.states = s.existing_state
    where s.map_state is null;

select * from agg_users limit 10;