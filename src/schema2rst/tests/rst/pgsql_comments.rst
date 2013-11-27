
Schema: test
============


商品 (items)
------------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - 商品 ID
     - id
     - INTEGER
     - True
     - True
     - nextval('items_id_seq'::regclass)
     - 
   * - 商品名
     - name
     - VARCHAR(255)
     - True
     - False
     - None
     - 
   * - 種別
     - type
     - INTEGER
     - True
     - False
     - 1
     - 1:食品, 2:文具, 3:雑貨
   * - 説明文
     - description
     - TEXT
     - False
     - False
     - None
     - 

購入履歴 (order_history)
------------------------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - 履歴 ID
     - id
     - INTEGER
     - True
     - True
     - nextval('order_history_id_seq'::regclass)
     - 
   * - ユーザ ID
     - user_id
     - INTEGER
     - True
     - False
     - None
     - FK: users.id
   * - 商品 ID
     - item_id
     - INTEGER
     - True
     - False
     - None
     - FK: items.id
   * - 数量
     - amount
     - INTEGER
     - True
     - False
     - None
     - 
   * - 購入日
     - order_date
     - TIMESTAMP WITHOUT TIME ZONE
     - False
     - False
     - None
     - 

Keys
^^^^

* KEY: item_id_order_date_key (item_id, order_date)
* KEY: user_id_order_date_key (user_id, order_date)

ユーザ (users)
--------------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - ユーザ ID
     - id
     - INTEGER
     - True
     - True
     - nextval('users_id_seq'::regclass)
     - 
   * - ログイン ID
     - login_id
     - VARCHAR(16)
     - True
     - False
     - ''::character varying
     - 
   * - 氏名
     - fullname
     - VARCHAR(255)
     - True
     - False
     - ''::character varying
     - 
   * - メールアドレス
     - mailaddr
     - VARCHAR(255)
     - True
     - False
     - ''::character varying
     - 

Keys
^^^^

* KEY: mailaddr_key (mailaddr)
* UNIQUE KEY: users_mailaddr_key (mailaddr)
