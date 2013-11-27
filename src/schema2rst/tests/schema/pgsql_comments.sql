CREATE TABLE users (
  id serial primary key,
  login_id varchar(16) default '' not null,
  fullname varchar(255) default '' not null,
  mailaddr varchar(255) default '' not null unique
);
CREATE INDEX mailaddr_key ON users(mailaddr);
COMMENT ON TABLE users IS 'ユーザ';
COMMENT ON COLUMN users.id IS 'ユーザ ID';
COMMENT ON COLUMN users.login_id IS 'ログイン ID';
COMMENT ON COLUMN users.fullname IS '氏名';
COMMENT ON COLUMN users.mailaddr IS 'メールアドレス';

CREATE TABLE items (
  id serial primary key,
  name varchar(255) not null,
  type int not null default 1,
  description text
);
COMMENT ON TABLE items IS '商品';
COMMENT ON COLUMN items.id IS '商品 ID';
COMMENT ON COLUMN items.name IS '商品名';
COMMENT ON COLUMN items.type IS '種別 (1:食品, 2:文具, 3:雑貨)';
COMMENT ON COLUMN items.description IS '説明文';

CREATE TABLE order_history (
  id serial primary key,
  user_id int not null,
  item_id int not null,
  amount int not null,
  order_date timestamp,
  foreign key (user_id) references users(id),
  foreign key (item_id) references items(id)
);
CREATE INDEX user_id_order_date_key ON order_history(user_id, order_date);
CREATE INDEX item_id_order_date_key ON order_history(item_id, order_date);
COMMENT ON TABLE order_history IS '購入履歴';
COMMENT ON COLUMN order_history.id IS '履歴 ID';
COMMENT ON COLUMN order_history.user_id IS 'ユーザ ID';
COMMENT ON COLUMN order_history.item_id IS '商品 ID';
COMMENT ON COLUMN order_history.amount IS '数量';
COMMENT ON COLUMN order_history.order_date IS '購入日';
