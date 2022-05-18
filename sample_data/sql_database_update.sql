alter table users
(
    user_id           serial
        constraint users_pk
            primary key,
    username          varchar(15)  not null,
    email             varchar(30)  not null,
    password          varchar(100) not null,
    registration_date timestamp,
    reputation_number integer
);