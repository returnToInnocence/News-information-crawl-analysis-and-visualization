use db1;

create table news_link(
	news_source char(20) primary key,
	news_source_link varchar(300) not null
);
create table user_info(
	user_id smallint primary key,
	user_name char(20) not null,
	user_password char(30) not null,
	user_permission tinyint not null
);
create table news_bs4(
	news_id smallint primary key,
	news_title varchar(200) not null,
	news_source char(20) not null,
	news_time date not null,
	news_content text not null,
	foreign key(news_source) references news_link(news_source) 
		on update cascade
		on delete cascade
);
create table news_classification(
	news_id smallint,
	news_classification CHAR(20) not null,
	foreign key(news_id) references news_bs4(news_id)
		on update cascade
		on delete cascade
);
create table news_hot(
	hot_news_id smallint primary key,
	news_fever INTEGER not null,
	pre12_count INTEGER not null,
	pre24_count INTEGER not null,
	pre48_count INTEGER not null,
	pre72_count INTEGER not null,
	pre96_count INTEGER not null,
	pre120_count INTEGER not null,
	foreign key(hot_news_id) references news_bs4(news_id)
		on update cascade
		on delete cascade
);
create table news_pretreatment(
	news_id SMALLINT primary key,
	news_source_pretreat text not null,
	user_id smallint,
	foreign key(news_id) references news_bs4(news_id)
		on update cascade
		on delete cascade,
    foreign key(user_id) references user_info(user_id)
		on update cascade
		on delete cascade
);
create table news_summary(
	news_id SMALLINT primary key,
	news_summ TEXT not null,
	foreign key(news_id) references news_bs4(news_id)
		on update cascade
		on delete cascade
); 
create table news_tag_hot(
	news_tags char(20) primary key,
	pre12_count INTEGER not null,
	pre24_count INTEGER not null,
	pre48_count INTEGER not null,
	pre72_count INTEGER not null,
	pre96_count INTEGER not null,
	pre120_count INTEGER not null
);
create table news_tag(
	news_id SMALLINT,
	news_tags char(20),
	foreign key(news_id) references news_bs4(news_id)
		on update cascade
		on delete cascade,
	foreign key(news_tags) references news_tag_hot(news_tags)
		on update cascade
		on delete cascade
);