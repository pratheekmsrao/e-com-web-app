DROP TABLE IF EXISTS products;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS cart;

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name character varying(255) NOT NULL,
    manufacturer character varying(255) NOT NULL,
    supplier character varying(255) NOT NULL,
    category character varying(255) NOT NULL,
    sub_category character varying(255) NOT NULL,
    country_of_origin character varying(255) NOT NULL,
    inventory_count int4 NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username character varying(255) NOT NULL UNIQUE,
    password character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS cart (
	id SERIAL NOT NULL,
	user_id int4 NULL,
	product_id int4 NULL,
	quantity int4 NOT NULL,
	CONSTRAINT cart_pkey PRIMARY KEY (id)
);


ALTER TABLE cart ADD CONSTRAINT cart_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE;
ALTER TABLE cart ADD CONSTRAINT cart_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

--TRUNCATE TABLE  products;
--
--TRUNCATE TABLE  users;

INSERT INTO products (name, manufacturer,supplier,category,sub_category,country_of_origin,inventory_count) VALUES
('iphone','apple','cloudtail','electronics','smart phone','usa',3),
('s22','samsung','aprila retail','electronics','smart phone','india',4),
('handy','dettol','more retail','sanitizer','hand sanitizer','india',10),
('lenovo e14','lenovo','lenovo retail','electronics','laptop','china',4),
('msi u5200','msi','flipkart','electronics','laptop','china',4),
('lg ml600u','lg','amazon','electronics','monitor','china',4),
('levis s512','levis','trendy cloths','clothes','jeans','india',4),
('wrangler 342','wrangler','fashon','clothes','jeans','japan',4),
('lee 212','lee','reliance trendz','clothes','t-shirts','india',4),
('nike 239','nike','nike trendz','clothes','t-shirts','taiwan',4),
('samsong flip z','samsung','samsung retails','electronics','flip phone','usa',4),
('string','nike','nike trendz','clothes','string','uk',2);

CREATE EXTENSION pgcrypto;

INSERT INTO users (username, password) VALUES
('admin', 'password'),
('pratheek', 'pratheek'),
('1',crypt('1', gen_salt('bf'))),
('invadmin',crypt('inventory', gen_salt('bf'))),
('user',crypt('pass', gen_salt('bf')));


--INSERT INTO cart
--(user_id, product_id, quantity)
--VALUES(0, 0, 0);
