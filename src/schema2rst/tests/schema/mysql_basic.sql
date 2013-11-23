CREATE TABLE posts(
    id int primary key auto_increment,
    title varchar(256),
    content text,
    created_at datetime
);
CREATE TABLE comments(
    id int primary key auto_increment,
    post_id int,
    name varchar(256),
    email varchar(256),
    content varchar(256),
    created_at datetime,
    foreign key (post_id) references posts(id)
);
