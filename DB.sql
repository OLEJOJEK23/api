CREATE ROLE lab WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:ER7XiX6uUwb6Hwb7LOliVw==$rUbIiutu20ZfHr5iUxihb5BQydI7ODi9FnvnmfRHzs8=:YeLvBc7mmlo8YD3M89hSzxQNwGLuhj1XYsqTSqhPQYM=';

CREATE DATABASE "Graphs"
    WITH
    OWNER = lab
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


CREATE TABLE IF NOT EXISTS public.graphs
(
    "graphID" serial NOT NULL,
    "graphName" text COLLATE pg_catalog."default" NOT NULL,
    "ownerID" integer NOT NULL,
    CONSTRAINT graphs_pkey PRIMARY KEY ("graphID")
);

CREATE TABLE IF NOT EXISTS public.link
(
    linkid serial NOT NULL,
    source integer NOT NULL,
    target integer NOT NULL,
    value numeric NOT NULL,
    graphid integer NOT NULL,
    CONSTRAINT link_pkey PRIMARY KEY (linkid)
);

CREATE TABLE IF NOT EXISTS public.node
(
    "nodeId" serial NOT NULL,
    "graphID" integer NOT NULL,
    x numeric NOT NULL,
    y numeric NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Node_pkey" PRIMARY KEY ("nodeId"),
    CONSTRAINT dgd UNIQUE (name)
        INCLUDE(name)
);

CREATE TABLE IF NOT EXISTS public.session
(
    "sessionID" serial NOT NULL,
    token text COLLATE pg_catalog."default" NOT NULL,
    userid integer NOT NULL,
    CONSTRAINT "Session_pkey" PRIMARY KEY ("sessionID"),
    CONSTRAINT k UNIQUE (token)
);

CREATE TABLE IF NOT EXISTS public.users
(
    "userID" serial NOT NULL,
    login text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY ("userID"),
    CONSTRAINT uniq1 UNIQUE (login)
);

ALTER TABLE IF EXISTS public.graphs
    ADD CONSTRAINT br FOREIGN KEY ("ownerID")
    REFERENCES public.users ("userID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.link
    ADD CONSTRAINT kkd FOREIGN KEY (graphid)
    REFERENCES public.graphs ("graphID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.node
    ADD CONSTRAINT f FOREIGN KEY ("graphID")
    REFERENCES public.graphs ("graphID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.session
    ADD CONSTRAINT mm FOREIGN KEY (userid)
    REFERENCES public.users ("userID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

END;