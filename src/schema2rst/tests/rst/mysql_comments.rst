
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
     - int(11)
     - True
     - True
     - None
     - auto_increment
   * - 商品名
     - name
     - varchar(255)
     - True
     - False
     - None
     - latin1_swedish_ci
   * - 種別
     - type
     - int(11)
     - True
     - False
     - '1'
     - 1:食品, 2:文具, 3:雑貨
   * - 説明文
     - description
     - text
     - False
     - False
     - None
     - latin1_swedish_ci

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
     - int(11)
     - True
     - True
     - None
     - auto_increment
   * - ユーザ ID
     - user_id
     - int(11)
     - True
     - False
     - None
     - FK: users.id
   * - 商品 ID
     - item_id
     - int(11)
     - True
     - False
     - None
     - FK: items.id
   * - 数量
     - amount
     - int(11)
     - True
     - False
     - None
     - 
   * - 購入日
     - order_date
     - datetime
     - False
     - False
     - None
     - 

Keys
^^^^

* KEY: item_id (item_id, order_date)
* KEY: user_id (user_id, order_date)

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
     - int(11)
     - True
     - True
     - None
     - auto_increment
   * - ログイン ID
     - login_id
     - varchar(16)
     - True
     - False
     - ''
     - latin1_swedish_ci
   * - 氏名
     - fullname
     - varchar(255)
     - True
     - False
     - ''
     - latin1_swedish_ci
   * - 性別
     - sex
     - int(11)
     - True
     - False
     - '0'
     - 0:不明, 1:男性, 2:女性, 9:その他
   * - メールアドレス
     - mailaddr
     - varchar(255)
     - True
     - False
     - ''
     - latin1_swedish_ci

Keys
^^^^

* UNIQUE KEY: mailaddr (mailaddr)
* KEY: mailaddr_2 (mailaddr)
