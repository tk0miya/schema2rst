
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
     - INTEGER
     - True
     - True
     - nextval('comments_id_seq'::regclass)
     - 
   * - post_id
     - post_id
     - INTEGER
     - False
     - False
     - None
     - FK: posts.id
   * - name
     - name
     - VARCHAR(256)
     - False
     - False
     - None
     - 
   * - email
     - email
     - VARCHAR(256)
     - False
     - False
     - None
     - 
   * - content
     - content
     - VARCHAR(256)
     - False
     - False
     - None
     - 
   * - created_at
     - created_at
     - TIMESTAMP WITHOUT TIME ZONE
     - False
     - False
     - None
     - 

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
     - INTEGER
     - True
     - True
     - nextval('posts_id_seq'::regclass)
     - 
   * - title
     - title
     - VARCHAR(256)
     - False
     - False
     - None
     - 
   * - content
     - content
     - TEXT
     - False
     - False
     - None
     - 
   * - created_at
     - created_at
     - TIMESTAMP WITHOUT TIME ZONE
     - False
     - False
     - None
     - 
