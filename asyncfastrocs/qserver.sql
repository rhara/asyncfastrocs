create table repo (
    oid text primary key,
    basename text,
    ext text,
    reportable int default 0,
    timestamp1 real default 0.0,
    timestamp2 real default 0.0,
    status int default 0,
--  status 0: queued, 1: under process, 2: done
    ip text default '0.0.0.0',
    dbname text default ''
);

create table db (
    name text primary key,
    path text,
    molcount int default -1,
    confcount int default -1
);

create table active_db (
    name text,
    pid int default -1,
    ready int default 0,
    loadtime real default -1.0,
    count int
);
