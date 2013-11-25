
Schema: test
============


comments
--------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - int(11)
     - True
     - True
     - None
     - auto_increment
   * - post_id
     - post_id
     - int(11)
     - False
     - False
     - None
     - FK: posts.id
   * - name
     - name
     - varchar(256)
     - False
     - False
     - None
     - latin1_swedish_ci
   * - email
     - email
     - varchar(256)
     - False
     - False
     - None
     - latin1_swedish_ci
   * - content
     - content
     - varchar(256)
     - False
     - False
     - None
     - latin1_swedish_ci
   * - created_at
     - created_at
     - datetime
     - False
     - False
     - None
     - 

Keys
^^^^

* KEY: post_id (post_id)

posts
-----

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - int(11)
     - True
     - True
     - None
     - auto_increment
   * - title
     - title
     - varchar(256)
     - False
     - False
     - None
     - latin1_swedish_ci
   * - content
     - content
     - text
     - False
     - False
     - None
     - latin1_swedish_ci
   * - created_at
     - created_at
     - datetime
     - False
     - False
     - None
     - 
