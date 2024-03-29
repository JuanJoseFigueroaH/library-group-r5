-- public.authors definition
-- Drop table
-- DROP TABLE public.authors;
CREATE TABLE public.authors (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT authors_pk PRIMARY KEY (id),
	CONSTRAINT authors_un UNIQUE (name)
);
-- public.categories definition
-- Drop table
-- DROP TABLE public.categories;
CREATE TABLE public.categories (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT categories_pk PRIMARY KEY (id),
	CONSTRAINT categories_un UNIQUE (name)
);
-- public.publishing definition
-- Drop table
-- DROP TABLE public.editors;
CREATE TABLE public.editors (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT publishing_pk PRIMARY KEY (id),
	CONSTRAINT publishing_un UNIQUE (name)
);
-- public.books definition
-- Drop table
-- DROP TABLE public.books;
CREATE TABLE public.books (
	id varchar NOT NULL,
	title varchar NOT NULL,
	subtitle varchar NULL,
	description text NULL,
	image varchar NULL,
	editor_id bigint NULL,
	editor_date varchar NULL,
	CONSTRAINT books_pk PRIMARY KEY (id)
);
-- public.books foreign keys
ALTER TABLE public.books ADD CONSTRAINT books_fk FOREIGN KEY (editor_id) REFERENCES public.editors(id) ON DELETE CASCADE; 
-- public.books_authors definition
-- Drop table
-- DROP TABLE public.books_authors;
CREATE TABLE public.books_authors (
	book_id varchar NOT NULL,
	author_id serial4 NOT NULL,
	CONSTRAINT books_authors_pk PRIMARY KEY (book_id, author_id)
);
-- public.books_authors foreign keys
ALTER TABLE public.books_authors ADD CONSTRAINT books_authors_fk FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;
ALTER TABLE public.books_authors ADD CONSTRAINT books_authors_fk_1 FOREIGN KEY (author_id) REFERENCES public.authors(id) ON DELETE CASCADE; 
-- public.books_categories definition
-- Drop table
-- DROP TABLE public.books_categories;
CREATE TABLE public.books_categories (
	book_id varchar NOT NULL,
	category_id serial4 NOT NULL,
	CONSTRAINT books_categories_pk PRIMARY KEY (book_id, category_id)
);
-- public.books_categories foreign keys
ALTER TABLE public.books_categories ADD CONSTRAINT books_categories_fk FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;
ALTER TABLE public.books_categories ADD CONSTRAINT books_categories_fk_1 FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;