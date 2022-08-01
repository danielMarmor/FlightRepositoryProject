-- FUNCTION: public.get_tickets_by_customer(bigint)

DROP FUNCTION IF EXISTS public.get_tickets_by_customer(bigint);

CREATE OR REPLACE FUNCTION public.get_tickets_by_customer(
	_customer_id bigint)
    RETURNS TABLE(ticket_id bigint,
				  first_name character varying,
				  last_name character varying,
				  origin_country_name character varying,
				  origin_country_airport_abbr character varying,
				  destination_country_name character varying,
				  dest_country_airport_abbr character varying,
				  airline_company_id bigint,
				  airline_company_name character varying,
				  airline_company_img_url character varying,
				  departure_time text,
				  landing_time text)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select
			tick.id ticket_id,
			cust.first_name first_name,
			cust.last_name last_name,
			cor.name origin_country_name,
			cor.airport_abbr origin_country_airport_abbr,
			cde.name destination_country_name,
			cde.airport_abbr dest_country_airport_abbr,
			fli.airline_company_id airline_company_id,
			ac.name airline_company_name,
			ac.image_url airline_company_img_url,
			to_char(fli.departure_time, 'DD/MM/YYYY') departure_time,
			to_char(fli.landing_time, 'DD/MM/YYYY') landing_time
			from tickets tick
			join customers cust on tick.customer_id = cust.id
			join flights fli on tick.flight_id = fli.id
			join airine_companies ac on fli.airline_company_id =ac.id
			join countries cor on fli.origin_country_id = cor.id
			join countries cde on fli.destination_country_id = cde.id
			where tick.customer_id =_customer_id
			order by fli.departure_time asc;

		end;

$BODY$;

ALTER FUNCTION public.get_tickets_by_customer(bigint)
    OWNER TO postgres;
