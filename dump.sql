--
-- PostgreSQL database dump
--

\restrict F5vTLxfbRqcDRqfYR5JhMoYKytuf4jxJXox4SB9WBifUcx2fDfdeHXSm0v9aWjY

-- Dumped from database version 14.20 (Homebrew)
-- Dumped by pg_dump version 14.20 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: fueltype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.fueltype AS ENUM (
    'PETROL',
    'DIESEL',
    'HYBRID',
    'PLUG_IN_HYBRID',
    'ELECTRIC',
    'LPG',
    'CNG'
);


--
-- Name: partcondition; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.partcondition AS ENUM (
    'NEW',
    'USED_GOOD',
    'USED_FAIR',
    'FOR_PARTS'
);


--
-- Name: partstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.partstatus AS ENUM (
    'AVAILABLE',
    'SOLD',
    'RESERVED'
);


--
-- Name: transmissiontype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.transmissiontype AS ENUM (
    'MANUAL',
    'AUTOMATIC',
    'SEMI_AUTOMATIC'
);


--
-- Name: userrole; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.userrole AS ENUM (
    'ADMIN'
);


--
-- Name: vehiclestatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.vehiclestatus AS ENUM (
    'AVAILABLE',
    'SOLD',
    'RESERVED'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: contactrequest; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contactrequest (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    phone character varying NOT NULL,
    subject character varying NOT NULL,
    message character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_read boolean NOT NULL
);


--
-- Name: contactrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.contactrequest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contactrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.contactrequest_id_seq OWNED BY public.contactrequest.id;


--
-- Name: part; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.part (
    id integer NOT NULL,
    title character varying NOT NULL,
    category character varying NOT NULL,
    brand character varying NOT NULL,
    compatible_models character varying NOT NULL,
    condition character varying NOT NULL,
    price integer NOT NULL,
    description character varying NOT NULL,
    status public.partstatus NOT NULL,
    is_featured boolean NOT NULL,
    is_published boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: part_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.part_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: part_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.part_id_seq OWNED BY public.part.id;


--
-- Name: partimage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.partimage (
    id integer NOT NULL,
    image_url character varying NOT NULL,
    is_cover boolean NOT NULL,
    display_order integer NOT NULL,
    alt_text character varying,
    created_at timestamp without time zone NOT NULL,
    part_id integer NOT NULL
);


--
-- Name: partimage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.partimage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partimage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.partimage_id_seq OWNED BY public.partimage.id;


--
-- Name: service; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.service (
    id integer NOT NULL,
    title character varying NOT NULL,
    short_description character varying NOT NULL,
    full_description character varying NOT NULL,
    display_order integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: service_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.service_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: service_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.service_id_seq OWNED BY public.service.id;


--
-- Name: tradeinrequest; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tradeinrequest (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    phone character varying NOT NULL,
    brand character varying NOT NULL,
    model character varying NOT NULL,
    year integer NOT NULL,
    mileage integer NOT NULL,
    condition_note character varying NOT NULL,
    message character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_read boolean NOT NULL
);


--
-- Name: tradeinrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tradeinrequest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tradeinrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tradeinrequest_id_seq OWNED BY public.tradeinrequest.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    role public.userrole NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: vehicle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle (
    id integer NOT NULL,
    title character varying NOT NULL,
    brand character varying NOT NULL,
    model character varying NOT NULL,
    year integer NOT NULL,
    mileage integer NOT NULL,
    fuel public.fueltype NOT NULL,
    transmission public.transmissiontype NOT NULL,
    price integer NOT NULL,
    description character varying NOT NULL,
    status public.vehiclestatus NOT NULL,
    is_featured boolean NOT NULL,
    is_published boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: vehicle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vehicle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vehicle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vehicle_id_seq OWNED BY public.vehicle.id;


--
-- Name: vehicleimage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicleimage (
    id integer NOT NULL,
    image_url character varying NOT NULL,
    is_cover boolean NOT NULL,
    display_order integer NOT NULL,
    alt_text character varying,
    created_at timestamp without time zone NOT NULL,
    vehicle_id integer NOT NULL
);


--
-- Name: vehicleimage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vehicleimage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vehicleimage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vehicleimage_id_seq OWNED BY public.vehicleimage.id;


--
-- Name: contactrequest id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactrequest ALTER COLUMN id SET DEFAULT nextval('public.contactrequest_id_seq'::regclass);


--
-- Name: part id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.part ALTER COLUMN id SET DEFAULT nextval('public.part_id_seq'::regclass);


--
-- Name: partimage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partimage ALTER COLUMN id SET DEFAULT nextval('public.partimage_id_seq'::regclass);


--
-- Name: service id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.service ALTER COLUMN id SET DEFAULT nextval('public.service_id_seq'::regclass);


--
-- Name: tradeinrequest id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tradeinrequest ALTER COLUMN id SET DEFAULT nextval('public.tradeinrequest_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: vehicle id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle ALTER COLUMN id SET DEFAULT nextval('public.vehicle_id_seq'::regclass);


--
-- Name: vehicleimage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicleimage ALTER COLUMN id SET DEFAULT nextval('public.vehicleimage_id_seq'::regclass);


--
-- Data for Name: contactrequest; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contactrequest (id, name, email, phone, subject, message, created_at, is_read) FROM stdin;
1	Kévin Fruchon	kevin.fruchon@gmail.com	0666671394	Demande de révision	Bonjour,\nJ'ai besoin d'une révision pour mon véhicule	2026-04-30 13:57:00.756963	t
2	Jean Dupont	test@exemple.fr	0666666666	Demande de renseignement	Bonjour, \nUn long message pour tester l'affichage.\nUn long message pour tester l'affichageUn long message pour tester l'affichageUn long message pour tester l'affichageUn long message pour tester l'affichageUn long message pour tester l'affichageUn long message pour tester l'affichage\nCordialement	2026-05-06 19:04:24.212516	t
\.


--
-- Data for Name: part; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.part (id, title, category, brand, compatible_models, condition, price, description, status, is_featured, is_published, created_at, updated_at) FROM stdin;
1	Gros joint de culasse	Joint	Bosh	Grosse voiture	NEW	100	Gros joint de culasse pour grosse voiture	AVAILABLE	t	t	2026-04-29 19:17:16.314369	2026-04-29 19:17:16.314388
2	Volant	Volant	Renault	Clio 3	USED_GOOD	20	Volant clio 3 bon état	AVAILABLE	t	t	2026-04-29 19:18:01.564669	2026-04-29 19:18:01.564688
3	Embrayage Peugeot 308	Embrayage	MARQUE	MODELES COMPATIBLES	USED_FAIR	130	DESCRIPTION	AVAILABLE	t	t	2026-05-05 16:23:49.475099	2026-05-05 17:32:08.174604
\.


--
-- Data for Name: partimage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.partimage (id, image_url, is_cover, display_order, alt_text, created_at, part_id) FROM stdin;
1	/uploads/parts/b38805c492e145879ff38da816c56b92.jpg	t	0	\N	2026-05-05 17:21:54.568821	3
\.


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.service (id, title, short_description, full_description, display_order, is_active, created_at, updated_at) FROM stdin;
1	Révisions	Révision auto	Comprenant le changement des fluides, filtres,...	0	t	2026-04-30 13:49:56.316452	2026-04-30 13:49:56.316479
2	Pneus	Changement des pneus	Comprenant le changement des pneus, équilibrage	0	t	2026-04-30 13:50:36.351629	2026-04-30 13:50:36.351647
4	test	test_short_description 	test_full_description	3	t	2026-05-05 19:04:45.974063	2026-05-05 19:23:56.401462
3	Entretien	Plaquettes, Disques,...	Equilibrage, changement des plaquettes, disques,...	1	t	2026-04-30 13:51:15.247354	2026-05-05 19:24:09.151402
\.


--
-- Data for Name: tradeinrequest; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tradeinrequest (id, name, email, phone, brand, model, year, mileage, condition_note, message, created_at, is_read) FROM stdin;
1	Kévin Fruchon	kevin.fruchon@gmail.com	0666671394	Renault	Clio	2007	200000	Bon état, quelques rayures	Bonjour,\nJ'en veut 2500 euros	2026-04-30 14:02:02.952087	t
2	Kévin Fruchon	kevin.fruchon@gmail.com	0666671394	MARQUE	Corsa D	1901	0	Bon état, quelques rayures	fef"f"f"fef"fef"f"	2026-05-06 19:47:34.845949	t
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (id, email, password_hash, role, is_active, created_at) FROM stdin;
1	admin@glf.fr	$2b$12$F5LADYhAUIubrAbpq/O0he9s05E01SntaD0ENQnqfa4uJcnOLp7Xq	ADMIN	t	2026-04-29 19:15:48.076928
\.


--
-- Data for Name: vehicle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.vehicle (id, title, brand, model, year, mileage, fuel, transmission, price, description, status, is_featured, is_published, created_at, updated_at) FROM stdin;
2	Megane RS	Renault	Megane RS	2012	145000	DIESEL	AUTOMATIC	9500	Va très vite	AVAILABLE	t	t	2026-05-05 14:09:48.800956	2026-05-05 14:09:48.800982
1	Peugeot 206	Peugeot	206	2000	200000	PETROL	MANUAL	3500	Peugeot 206, Contrôle technique OK	AVAILABLE	t	t	2026-04-29 19:19:07.454124	2026-05-05 14:13:02.470206
3	Opel Corsa D	Opel	Corsa D	2011	210000	DIESEL	MANUAL	3000	opel corsa D , description.......	AVAILABLE	t	t	2026-05-05 16:20:38.6804	2026-05-06 20:58:02.736396
\.


--
-- Data for Name: vehicleimage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.vehicleimage (id, image_url, is_cover, display_order, alt_text, created_at, vehicle_id) FROM stdin;
2	/uploads/vehicles/7872e738c0814afd9405de272639ea33.jpg	f	1	\N	2026-05-05 14:12:58.524093	1
1	/uploads/vehicles/5970d74be91447eea1cd1b2ce97cecdf.jpg	t	0	\N	2026-05-05 14:12:43.817313	1
4	/uploads/vehicles/4b0bfea1a1d74ef2a178cb8abe7d0dca.jpg	f	0	\N	2026-05-06 20:57:54.360554	3
\.


--
-- Name: contactrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contactrequest_id_seq', 2, true);


--
-- Name: part_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.part_id_seq', 3, true);


--
-- Name: partimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.partimage_id_seq', 1, true);


--
-- Name: service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.service_id_seq', 4, true);


--
-- Name: tradeinrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tradeinrequest_id_seq', 2, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: vehicle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.vehicle_id_seq', 3, true);


--
-- Name: vehicleimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.vehicleimage_id_seq', 4, true);


--
-- Name: contactrequest contactrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactrequest
    ADD CONSTRAINT contactrequest_pkey PRIMARY KEY (id);


--
-- Name: part part_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.part
    ADD CONSTRAINT part_pkey PRIMARY KEY (id);


--
-- Name: partimage partimage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partimage
    ADD CONSTRAINT partimage_pkey PRIMARY KEY (id);


--
-- Name: service service_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.service
    ADD CONSTRAINT service_pkey PRIMARY KEY (id);


--
-- Name: tradeinrequest tradeinrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tradeinrequest
    ADD CONSTRAINT tradeinrequest_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: vehicle vehicle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle
    ADD CONSTRAINT vehicle_pkey PRIMARY KEY (id);


--
-- Name: vehicleimage vehicleimage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicleimage
    ADD CONSTRAINT vehicleimage_pkey PRIMARY KEY (id);


--
-- Name: ix_partimage_part_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_partimage_part_id ON public.partimage USING btree (part_id);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_vehicleimage_vehicle_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_vehicleimage_vehicle_id ON public.vehicleimage USING btree (vehicle_id);


--
-- Name: partimage partimage_part_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partimage
    ADD CONSTRAINT partimage_part_id_fkey FOREIGN KEY (part_id) REFERENCES public.part(id);


--
-- Name: vehicleimage vehicleimage_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicleimage
    ADD CONSTRAINT vehicleimage_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicle(id);


--
-- PostgreSQL database dump complete
--

\unrestrict F5vTLxfbRqcDRqfYR5JhMoYKytuf4jxJXox4SB9WBifUcx2fDfdeHXSm0v9aWjY

