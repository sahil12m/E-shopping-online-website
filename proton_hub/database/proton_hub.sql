drop database if exists proton_hub_database;
create database proton_hub_database;
use proton_hub_database;

show tables;

DROP TABLE IF EXISTS  `admin` ;
CREATE TABLE IF NOT EXISTS  `admin`  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   firstName  varchar(125) NOT NULL,
   lastName  varchar(125) NOT NULL,
   email  varchar(100) NOT NULL,
   mobile  varchar(25) NOT NULL,
   address  text NOT NULL,
   `password`  varchar(100) NOT NULL,
   `type`  varchar(20) NOT NULL,
   confirmCode  varchar(10) NOT NULL,
  PRIMARY KEY ( id )
) AUTO_INCREMENT=5;
insert into `admin`(firstName, lastName, email, mobile, address, `password`, `type`, confirmCode) values('Admin', 'admin', 'admin@gmail.com', '1234567890', 'Pune', '1234', 'manager', '0');


DROP TABLE IF EXISTS  products ;
CREATE TABLE IF NOT EXISTS  products  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   pName  varchar(100) NOT NULL,
   price  int(11) NOT NULL,
    `description`   text NOT NULL,
   quantity  int(11) NOT NULL,
   category  varchar(100) NOT NULL,
   pCode  varchar(20) NOT NULL,
   picture  text NOT NULL,
    `date`   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ( id )
)AUTO_INCREMENT=22;


DROP TABLE IF EXISTS  orders ;
CREATE TABLE IF NOT EXISTS  orders  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   uid  int(11) DEFAULT NULL,
   ofname  text NOT NULL,
   pid  int(11) NOT NULL,
   quantity  int(11) NOT NULL,
   oplace  text NOT NULL,
   mobile  varchar(15) NOT NULL,
   dstatus  varchar(10) NOT NULL DEFAULT 'no',
   odate  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   ddate  date DEFAULT NULL,
  PRIMARY KEY ( id ),
  foreign key (pid) references products(id)
)AUTO_INCREMENT=11;



insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Apple MacBook Pro', 199900, 'Apple MacBook Pro (16-inch, 16GB RAM, 512GB Storage, 2.6GHz 9th Gen Intel Core i7, Space Grey)', 20, 'laptop', '11', 'l1.jpg', '2020-09-04 12:20:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('HP 15 Athlon Dual Core', 27870, 'HP 15 Athlon Dual Core 15.6 inch Laptop (4 GB/1 TB HDD/Windows 10 Home/Jet Black/1.7 kg/with MS Office)', 50, 'laptop', '12', 'l2.jpg', '2020-08-05 14:29:27');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('HP Spectre x360', 200000, 'HP Spectre x360 Core i5 10th Gen 13-inch FHD Touchscreen Laptop (8GB/512 GB SSD/Windows 10/MS Office 2019/Nightfall Black/1.27 kg)', 30, 'laptop', '13', 'l3.jpg', '2020-05-04 09:20:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Microsoft Surface Pro 7', 88985, 'Microsoft Surface Pro 7 12.3 inch Touchscreen 2-in-1 Laptop (10th Gen Intel Core i5/8GB/128GB SSD/Windows 10 Home/Intel Iris Plus Graphics)', 40, 'laptop', '14', 'l4.jpg', '2020-06-07 10:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Lenovo ThinkPad E14', 49000, 'Lenovo ThinkPad E14 Intel Core i3 10th Gen 14-inch Full HD Thin and Light Laptop (4GB RAM/ 1TB HDD/ Windows 10 Home/ Black/ 1.77 kg)', 25, 'laptop', '15', 'l5.jpg', '2019-06-07 10:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Nokia 5.3', 14000, 'Nokia 5.3 Android One Smartphone with Quad Camera, 4 GB RAM and 64 GB Storage - Charcoal', 50, 'mobile', '21', 'm1.jpg', '2020-02-07 11:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Apple iPhone 11', 63900, 'Apple iPhone 11 (64GB) - Black', 37, 'mobile', '22', 'm2.jpg', '2019-09-10 17:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Redmi Note 9', 11000, 'Redmi Note 9 (Arctic White, 4GB RAM, 64GB Storage) - 48MP Quad Camera & Full HD+ Display', 70, 'mobile', '23', 'm3.jpg', '2019-12-09 19:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Samsung Galaxy S20 Ultra', 97000, 'Samsung Galaxy S20 Ultra (Cosmic Gray, 12GB RAM, 128GB Storage)', 10, 'mobile', '24', 'm4.jpg', '2020-01-03 20:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('OnePlus 8', 41999, 'OnePlus 8 (Glacial Green 6GB RAM+128GB Storage)', 47, 'mobile', '25', 'm5.jpg', '2020-04-25 08:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Dell G7', 120000, 'DELL Gaming-G7 7590 15.6-inch Laptop (9th Gen Core i7-9750H/16GB/512GB SSD/Windows 10 with MS Office/6GB NVIDIA 1660 Graphics), Abyss Grey', 57, 'laptop', '26', 'l6.jpg', '2020-05-17 08:30:24');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('HP OMEN15', 85000, 'HP Omen 15.6-inch FHD Gaming Laptop (Ryzen 5-4600H/8GB/512GB SSD/Windows 10/NVIDIA GTX 1650ti 4GB/Shadow Black/2.36 kg), 15-en0001AX', 43, 'laptop', '27', 'l7.jpg', '2020-06-21 10:24:32');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Lenovo Ideapad S145', 40000, 'Lenovo Ideapad S145 AMD Ryzen 3 3200U 15.6 inch FHD Thin and Light Laptop (4GB/1TB HDD/Windows 10/Grey/1.85Kg), 81UT00KWIN', 45, 'laptop', '28', 'l8.jpg', '2020-08-22 09:20:31');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Apple Macbook Air', 120000, 'Apple MacBook Air (13-inch, 1.1GHz Quad-core 10th-Generation Intel Core i5 Processor, 8GB RAM, 512GB Storage) - Space Grey', 50, 'laptop', '29', 'l9.jpg', '2020-05-23 12:27:37');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Dell G3', 88000, 'Dell Gaming-G3 3590 15.6-inch FHD Laptop (9th Gen Core i7-9750H/8GB/512GB SSD/Windows 10 + MS Office/4GB NVIDIA 1650 Graphics), Black', 52, 'laptop', '30', 'l10.jpg', '2020-06-20 11:14:45');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Samsung Galaxy M21', 16000, 'Samsung Galaxy M21 (Midnight Blue, 6GB RAM, 128GB Storage)', 47, 'mobile', '31', 'm6.jpg', '2020-04-20 12:17:40');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('One Plus Nord', 28000, 'One Plus Nord(90 hz fluid amoled display, snapdragon 765g, 6GB RAM, 128GB storage)', 45, 'mobile', '32', 'm7.jpg', '2020-04-22 07:15:20');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Apple iPhone SE', 42500, 'Apple iPhone SE (Black, 64 GB)', 48, 'mobile', '33', 'm8.jpg', '2020-07-17 17:20:46');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Samsung Galaxy Note 20', 67000, 'Samsung Galaxy Note 20 Ultra 5G (Mystic Black, 12GB RAM, 256GB Storage)', 55, 'mobile', '34', 'm9.jpg', '2020-06-16 06:05:04');
insert into products(pName, price, `description`, quantity, category, pCode, picture, `date`) values('Asus ROG Phone 2', 33000, 'Asus ROG Phone 2 (Black, 128 GB),(8 GB RAM)', 58, 'mobile', '35', 'm10.jpg', '2020-06-13 13:12:35');


DROP TABLE IF EXISTS  product_view ;
CREATE TABLE IF NOT EXISTS  product_view  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   user_id  int(11) NOT NULL,
   product_id  int(11) NOT NULL,
   `date`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ( id ),
  FOREIGN KEY (product_id) REFERENCES products(id) ON UPDATE CASCADE
	) AUTO_INCREMENT=9;

insert into product_view(user_id, product_id,`date`) values (17, 23, '2020-08-05 14:29:27');
insert into product_view(user_id, product_id,`date`) values (18, 27, '2020-02-07 11:30:24');

DROP TABLE IF EXISTS  login ;
CREATE TABLE IF NOT EXISTS  login  (
	username  varchar(25) NOT NULL,
    `password`  varchar(100) NOT NULL,
    primary key (username)
);

DROP TABLE IF EXISTS  user_name ;
CREATE TABLE IF NOT EXISTS  user_name  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   `name`  varchar(50) NOT NULL,
  PRIMARY KEY ( id )
) AUTO_INCREMENT=1;

DROP TABLE IF EXISTS  zip ;
CREATE TABLE IF NOT EXISTS  zip  (
	cust_addr_zip varchar(6) not null,
    cust_addr_city varchar(30) not null,
    primary key(cust_addr_zip)
);


DROP TABLE IF EXISTS  user_details ;
CREATE TABLE IF NOT EXISTS  user_details  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   email  varchar(50) NOT NULL,
   username  varchar(25) NOT NULL,
   mobile  varchar(20) NOT NULL,
   reg_time  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   user_zip varchar(30),
   PRIMARY KEY ( id, user_zip ),
   FOREIGN KEY (id) references user_name(id),
   Foreign key (username) references login(username),
   Foreign key (user_zip) references zip(cust_addr_zip)
);




/*DROP TABLE IF EXISTS  users ;
CREATE TABLE IF NOT EXISTS  users  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   -- `name`  varchar(50) NOT NULL,
   email  varchar(50) NOT NULL,
   username  varchar(25) NOT NULL,
   -- `password`  varchar(100) NOT NULL,
   mobile  varchar(20) NOT NULL,
   -- reg_time  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    activation  varchar(3) NOT NULL DEFAULT 'yes',
   user_zip varchar(30),
  PRIMARY KEY ( id )
) AUTO_INCREMENT=16 ;*/
-- insert into users(`name`, email, username, `password`, mobile, reg_time, activation) values('Sahil Mondal', 'sm@gmail.com', 'sm12', '0123', '3333333333', '2020-05-20 10:40:21', 'yes');
-- insert into users(`name`, email, username, `password`, mobile, reg_time, activation) values('Vignesh Charan Raman Sharma', 'vcrs@gmail.com', 'vcrs', '000000', '2333333333', '2020-06-21 20:40:21', 'yes');
-- insert into users(`name`, email, username, `password`, mobile, reg_time, activation) values('Poojan Panchal', 'pp@gmail.com', 'pp20', '1111', '1333333333', '2020-01-05 04:10:21', 'yes');

-- select * from users;


DROP TABLE IF EXISTS user_log;
CREATE TABLE IF NOT EXISTS user_log (
	id int,
    email  varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
	mobile  varchar(20) NOT NULL, 
    `time`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	user_zip varchar(30),
    PRIMARY KEY ( id, `time`)
    );
    
DELIMITER $$
Create trigger update_log 
	after update on user_details
	for each row 
    begin 
    insert into user_log  
    set 
		id = old.id,
        email = new.email,
		username = new.username,
		mobile = new.mobile,
        `time` = curtime(),
        user_zip = new.user_zip;
    end$$
DELIMITER ;

delimiter &&
create function get_no_order() returns integer
deterministic
begin
declare num_order int;
select count(*) into num_order from orders;
return num_order;
end &&
delimiter ;


-- List of queries used in app.py [Main driver code in the program]
-- SELECT * FROM products WHERE category='laptop' ORDER BY RAND() LIMIT 4;
-- SELECT * FROM products WHERE category='mobile' ORDER BY RAND() LIMIT 4;
-- SELECT * FROM login WHERE username='user';
-- SELECT id FROM user_details WHERE username='user';
-- SELECT name FROM user_name WHERE id=1;
-- INSERT INTO user_name(name) VALUES('abs');
-- INSERT INTO zip VALUES('400602', 'Thane');
-- INSERT INTO login VALUES('user', '1234');
-- INSERT INTO user_details(email, username, mobile, user_zip) VALUES('user@gmail.com', 'user', '1234567890', '411045');
-- SELECT * FROM products WHERE category='laptop' ORDER BY id ASC;
-- INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) VALUES(1, 11, 'user', '1234567890', 'Pune', 2, '2020-09-18');
-- SELECT * FROM products WHERE id=21;
-- SELECT * FROM product_view WHERE user_id=1 AND product_id=13;
-- UPDATE product_view SET date='2020-08-05 14:29:27' WHERE user_id=2 AND product_id=22;
-- INSERT INTO product_view(user_id, product_id) VALUES(3, 23);
-- SELECT * FROM products WHERE id=23;
-- SELECT * FROM products WHERE category='mobile' ORDER BY id ASC;
-- INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) VALUES(2, 11, 'user', 'Asus ROG Phone 2', 'Pune', 3, '2020-09-18');
-- SELECT * FROM admin WHERE email='admin@gmail.com';
-- select get_no_order() as ord;
-- SELECT * FROM user_details;
-- select * from user_details inner join user_name on user_name.id = user_details.id;
-- INSERT INTO products(pName,price,description,quantity,category,pCode,picture) VALUES('s20', 60000, 'samsung smartphone', 29, 'mobile', 29, 'm11.jpg');

-- UPDATE products SET pName='s20', price=60000, description='samsung smartphone', quantity=24, category='mobile', pCode=29, picture='m11.jpg' WHERE id=26;
-- SELECT * FROM products WHERE pName LIKE 'substring_to_be_searched' ORDER BY id ASC;
-- select orders.*,products.pName from orders inner join products on orders.pid = products.id where uid=1 order by odate desc;
-- select * from user_details inner join user_name on user_name.id = user_details.id where user_Details.id =2;
-- select username from user_details where id = 2;
-- UPDATE login SET password ='1234' WHERE username='user';
-- UPDATE user_details SET email='user@gmail.com', mobile='1234567890' WHERE id=3;
-- UPDATE user_name SET name='user' WHERE id=3;
