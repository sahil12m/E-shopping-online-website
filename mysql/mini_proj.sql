create database if not exists mini_proj;
use mini_proj;

show databases;
show tables; 
-- drop database mini_proj;

-- customer 
-- products
-- orders
-- cart
-- payment
-- feedback
-- Admin

create table login(
	cust_email int primary key,
    cust_pass varchar(30) not null
    check(cust_email like '%_@__%.__%' ));
    
create table zip(
	cust_addr_zip int primary key,
    cust_addr_city varchar(30)
    check(length(cust_addr_zip) = 6));
    
create table customer(
	cust_id int primary key, 
    cust_age int not null,
    cust_phno bigint not null unique, 
    cust_addr_zip int not null,
    check(length(cust_phno)=10),
    check(cust_age >=18),
    check(length(cust_addr_zip) = 6),
    Foreign Key(cust_addr_zip) references zip(cust_addr_zip)
    ); 
    
create table cust_order(
	cust_id int,
    cust_email varchar(50),
    order_placed date,
    order_status varchar(50),
    primary key(cust_id, cust_email),
    Foreign Key(cust_id) references customer(cust_id),
    Foreign Key(cust_email) references login(cust_email));
    
    
create table products(
	prod_id int primary key,
	prod_name varchar(100),
	prod_price int,
	prod_category varchar(30),
	prod_quantity int
	); 
    

create table orders(
	or_id int primary key,
	or_total_amt int,
	cust_id int,
	Foreign Key(cust_id) references customer(cust_id)
    );

    
create table feedback(
	feed_comment varchar(100),
	cust_id int,
	prod_id int,
    primary key(cust_id, prod_id),
	feed_stars int,
    check(feed_stars between 1 and 5) 
	);
    
create table payment(
	transaction_id int primary key,
    pay_method varchar(30),
	or_id int,
    Foreign Key(or_id) references orders(or_id)
	);
    
create table cart(
	cust_id int,
    prod_id int,
    added_qty int, -- its the quantity of items that the customer is about to buy ! 
    prod_price int,
    Primary Key(cust_id,prod_id),
    Foreign Key(cust_id) references customer(cust_id),
	Foreign Key(prod_id) references products(prod_id)
    );

show tables;

-- INSERTING THE DUMMY VALUES
insert into customer values(1,"Michael Scott",30,1234567890,"michael@gmail.com","pass1234","abc","pens",123456);
insert into customer values(2,"Jim Halpert",25,2134567890,"jim@gmail.com","pass1234","abc","pens",123456);
insert into customer values(3,"Pam Beasley",23,2143567890,"pam@gmail.com","pass1234","abc","pens",123456);
insert into customer values(4,"Dwight Shrute",26,2143576890,"dwight@gmail.com","pass1234","abc","pens",123456);
 
insert into orders value(1,"1000",1,"2020-08-22","recieved" );
insert into orders value(2,"1500",2,"2020-08-21","shipped" );
insert into orders value(3,"1800",1,"2020-08-20","out del" );
insert into orders value(4,"700",3,"2020-08-18","Done" );
insert into orders value(5,"12000",4,"2020-08-15","Done" );

insert into payment values(1,"Credit Card",1,1,1000);
insert into payment values(2,"Online Banking",2,2,1000);
insert into payment values(3,"Credit Card",3,1,2000);
insert into payment values(4,"Credit Card",4,3,3000);
insert into payment values(5,"Debit Card",5,4,3000);

insert into feedback values("nice quality",1,3,4);  
insert into feedback values("poor quality",2,2,1);
insert into feedback values("I like this product",3,1,5);
insert into feedback values("not bad",1,2,3);
insert into feedback values("must buy",1,5,4);
insert into feedback values("defective item",1,4,1);

insert into products values(1,'samsung m11',11000,'Mobiles',12);
insert into products values(2,'samsung m21',14000,'Mobiles',10);
insert into products values(3,'hp omen',110000,'Laptops',23);
insert into products values(4,'lenovo legion',169999,'Laptops',25);
insert into products values(5,'samsung m30',19000,'Mobiles',8);

select * from customer;
select * from orders;
select * from payment;
select * from feedback;
select * from products;

select cust_id from customer order by cust_id desc limit 1;

-- drop function login;
DELIMITER $$ 
 create function login_check(new_cust_email varchar(50), new_cust_pass varchar(50)) returns integer
    deterministic 
		begin
			declare flag integer;
            select cust_id into flag from customer where cust_email = new_cust_email and cust_pass = new_cust_pass;
			if flag > 0 then
				set flag = 1;
            else
				set flag = 0;
			end if;
			return (flag);
		end $$
DELIMITER ;

select login_check("michael@gmail.com","pass1234");

-- select cust_id from customer where cust_email = "miael@gmail.com" and cust_pass = "pass1234";

