CREATE TABLE users (
  id int primary key auto_increment comment 'ユーザ ID',
  login_id varchar(16) default '' not null comment 'ログイン ID',
  fullname varchar(255) default '' not null comment '氏名',
  sex int not null default 0 not null comment '性別	0:不明, 1:男性, 2:女性, 9:その他',
  mailaddr varchar(255) default '' not null unique comment 'メールアドレス',
  key (mailaddr)
) ENGINE='InnoDB' COMMENT 'ユーザ';

CREATE TABLE items (
  id int primary key auto_increment comment '商品 ID',
  name varchar(255) not null comment '商品名',
  type int not null default 1 comment '種別 (1:食品, 2:文具, 3:雑貨)',
  description text comment '説明文'
) ENGINE='InnoDB' COMMENT '商品';

CREATE TABLE order_history (
  id int primary key auto_increment comment '履歴 ID',
  user_id int not null comment 'ユーザ ID',
  item_id int not null comment '商品 ID',
  amount int not null comment '数量',
  order_date datetime comment '購入日',
  index (user_id, order_date),
  index (item_id, order_date),
  foreign key (user_id) references users(id),
  foreign key (item_id) references items(id)
) ENGINE='InnoDB' COMMENT '購入履歴';
