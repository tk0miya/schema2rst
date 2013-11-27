CREATE TABLE posts(
    id serial primary key,
    title varchar(256),
    content text,
    created_at timestamp
);
CREATE TABLE comments(
    id serial primary key,
    post_id int,
    name varchar(256),
    email varchar(256),
    content varchar(256),
    created_at timestamp,
    foreign key (post_id) references posts(id)
);
