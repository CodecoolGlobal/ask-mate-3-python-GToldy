create table if not exists tag
(
    id   serial
        constraint pk_tag_id
            primary key,
    name text
);

alter table tag
    owner to polandrea;

create table if not exists users
(
    user_id           serial
        constraint users_pk
            primary key,
    username          varchar(15)  not null,
    email             varchar(30)  not null,
    password          varchar(100) not null,
    registration_date timestamp,
    reputation_number int
);

alter table users
    owner to polandrea;

create table if not exists question
(
    id              serial
        constraint pk_question_id
            primary key,
    submission_time timestamp,
    view_number     integer,
    vote_number     integer,
    title           text,
    message         text,
    image           text,
    user_id         integer not null
        constraint question_users_user_id_fk
            references users
);

alter table question
    owner to polandrea;

create table if not exists answer
(
    id              serial
        constraint pk_answer_id
            primary key,
    submission_time timestamp,
    vote_number     integer,
    question_id     integer
        constraint fk_question_id
            references question
            on delete cascade,
    message         text,
    image           text,
    user_id         integer not null
        constraint answer_users_user_id_fk
            references users
);

alter table answer
    owner to polandrea;

create table if not exists comment
(
    id              serial
        constraint pk_comment_id
            primary key,
    question_id     integer
        constraint fk_question_id
            references question
            on delete cascade,
    answer_id       integer
        constraint fk_answer_id
            references answer
            on delete cascade,
    message         text,
    submission_time timestamp,
    edited_count    integer,
    user_id         integer not null
        constraint comment_users_user_id_fk
            references users
);

alter table comment
    owner to polandrea;

create table if not exists question_tag
(
    question_id integer not null
        constraint fk_question_id
            references question
            on delete cascade,
    tag_id      integer not null
        constraint fk_tag_id
            references tag,
    constraint pk_question_tag_id
        primary key (question_id, tag_id)
);

alter table question_tag
    owner to polandrea;

UPDATE public.answer SET submission_time = '2022-05-05 23:04:50.665110', vote_number = 0, question_id = 2, message = 'You shouldn''t hope for anything bad. Those dolls can be real evils.', image = '1651784690.6490138_doll.jpeg', user_id = 3 WHERE id = 4;
UPDATE public.answer SET submission_time = '2022-05-05 22:32:01.737203', vote_number = -2, question_id = 0, message = 'You got ghosted!', image = '1651782721.7217128_1651780868.2889256_Layer 1_sprite_2.png', user_id = 2 WHERE id = 3;
UPDATE public.answer SET submission_time = '2022-05-06 09:18:51.725370', vote_number = 2, question_id = 7, message = 'YES!!!', image = '', user_id = 3 WHERE id = 8;
UPDATE public.answer SET submission_time = '2022-05-06 07:32:43.533734', vote_number = -1, question_id = 4, message = 'You got ghosted! ', image = '1651815187.0665932_1651782721.7217128_1651780868.2889256_Layer 1_sprite_2.png', user_id = 2 WHERE id = 6;
UPDATE public.answer SET submission_time = '2022-05-06 07:56:29.438711', vote_number = 3, question_id = 6, message = 'Any pin is good ;)', image = '', user_id = 4 WHERE id = 7;
UPDATE public.answer SET submission_time = '2017-04-28 16:49:00.000000', vote_number = 4, question_id = 1, message = 'Ghostbusters!!', image = null, user_id = 4 WHERE id = 1;
UPDATE public.answer SET submission_time = '2022-05-05 23:15:15.265504', vote_number = 0, question_id = 0, message = 'Bro, you should move out immediately!!', image = '', user_id = 1 WHERE id = 5;
UPDATE public.answer SET submission_time = '2017-04-25 14:42:00.000000', vote_number = 35, question_id = 1, message = 'The Wincester brothers. There is Dean''s number: 1-245-4976285.', image = '', user_id = 1 WHERE id = 2;

UPDATE public.comment SET question_id = 0, answer_id = null, message = 'Please clarify the question as it is too vague!', submission_time = '2017-05-01 05:49:00.000000', edited_count = null, user_id = 2 WHERE id = 1;
UPDATE public.comment SET question_id = 6, answer_id = null, message = ' Oh no, why did you guys broke up?', submission_time = '2022-05-06 07:56:48.484878', edited_count = 0, user_id = 3 WHERE id = 5;
UPDATE public.comment SET question_id = null, answer_id = 1, message = 'There is the number: 3-452-8756942', submission_time = '2022-05-05 23:10:56.670200', edited_count = 1, user_id = 4 WHERE id = 2;

UPDATE public.tag SET name = 'ghost' WHERE id = 1;
UPDATE public.tag SET name = 'creepy' WHERE id = 18;
UPDATE public.tag SET name = 'haunted' WHERE id = 19;
UPDATE public.tag SET name = 'doll' WHERE id = 20;
UPDATE public.tag SET name = 'supernatural' WHERE id = 21;
UPDATE public.tag SET name = 'mirror' WHERE id = 22;
UPDATE public.tag SET name = 'cursed' WHERE id = 23;
UPDATE public.tag SET name = 'salt' WHERE id = 24;
UPDATE public.tag SET name = 'protection' WHERE id = 25;
UPDATE public.tag SET name = 'crucifix' WHERE id = 26;

UPDATE public.users SET username = 'Naldiln', email = 'georgina.toldy@gmail.com', password = 'asdf', registration_date = '2022-05-16 13:25:31.176471' WHERE user_id = 3;
UPDATE public.users SET username = 'Polandie', email = 'poley.andie@gmail.com', password = 'Boop', registration_date = '2022-05-16 13:42:56.000000' WHERE user_id = 4;
UPDATE public.users SET username = 'Zola', email = 'kurai.zoltan@gamil.com', password = 'Zolika', registration_date = '2022-05-17 17:03:00.000000' WHERE user_id = 1;
UPDATE public.users SET username = 'Gabszy', email = 'szilagyi.gabor@gmail.com', password = 'SexyZombie', registration_date = '2022-05-17 18:03:05.000000' WHERE user_id = 2;

UPDATE public.question SET submission_time = '2017-04-29 09:19:00.000000', view_number = 15, vote_number = 9, title = 'Who you gonna call?', message = 'But for real guys, who do you call when there are some supernatural stuff happening?', image = '', user_id = 2 WHERE id = 1;
UPDATE public.question SET submission_time = '2017-05-01 10:41:00.000000', view_number = 1364, vote_number = 57, title = 'I got a creepy looking doll at an antique store. Wouldn''t it be cool if that is possessed by a demon? ', message = 'It quiet worn out and missing an eye. I haven''t seen anything wierd yet but I am hoping.', image = null, user_id = 2 WHERE id = 2;
UPDATE public.question SET submission_time = '2022-05-06 07:55:20.474654', view_number = 0, vote_number = -2, title = 'What is needed for a woodoo doll?', message = 'My boyfriend broke up with me and I want to prank him. What metarials should I get? Any kind of pin is good? Thanks guy!!', image = '', user_id = 1 WHERE id = 6;
UPDATE public.question SET submission_time = '2022-05-06 07:27:45.466314', view_number = 0, vote_number = 0, title = 'Is salt good against ghosts?', message = 'I heard you can use salt to keep ghosts away. Is that true? Is sea salt good also, thats all I have home?', image = '1651814865.4395845_salt.jpeg', user_id = 3 WHERE id = 3;
UPDATE public.question SET submission_time = '2017-04-28 08:29:00.000000', view_number = 29, vote_number = 7, title = 'Is that mirror haunted?', message = 'I found a mirror in the hallway what shows the reflection of my basement. Do you guys think is that haunted?', image = '1651785232.5015306_spooky-mirror.png', user_id = 3 WHERE id = 0;
UPDATE public.question SET submission_time = '2022-05-06 07:38:10.725847', view_number = 0, vote_number = 0, title = 'Can I use any mirror for scrying or does it have to be cursed?', message = 'My wife have a big antique (and ugly) mirror it is propably not cursed but I kinda wanna get rid of it.', image = '', user_id = 1 WHERE id = 5;
UPDATE public.question SET submission_time = '2022-05-06 09:18:01.325382', view_number = 0, vote_number = 2, title = 'Is that true wrath can float?', message = 'I was always wondering about that.', image = '', user_id = 4 WHERE id = 7;
UPDATE public.question SET submission_time = '2022-05-06 07:32:20.715643', view_number = 0, vote_number = 2, title = 'Will crocheted crucifix protect me?', message = 'My grandma made me a crucifix. I was wondering if thats helps against ghostes. Any idea?', image = '1651815140.6870358_crucifix.jpg', user_id = 4 WHERE id = 4;
