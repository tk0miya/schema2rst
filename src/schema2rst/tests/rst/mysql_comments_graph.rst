
Schema: test
============

.. graphviz::

   digraph {
      node [shape = box];
      items [label="items\n(商品)"];
      order_history [label="order_history\n(購入履歴)"];
      order_history -> users;
      order_history -> items;
      users [label="users\n(ユーザ)"];
   }
