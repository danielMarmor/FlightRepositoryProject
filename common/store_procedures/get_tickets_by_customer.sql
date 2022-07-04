-- FUNCTION: public.get_tickets_by_customer(bigint)

 DROP FUNCTION IF EXISTS public.get_tickets_by_customer(bigint);

CREATE OR REPLACE FUNCTION public.get_tickets_by_customer(
	_customer_id bigint)
    RETURNS TABLE(ticket_id bigint,
				  first_name character varying(50),
				  last_name character varying(50),
				  origin_country_name character varying(50),
				  destination_country_name character varying(50),
				  departure_time text)


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
			cde.name destination_country_name,
			to_char(fli.departure_time, 'DD/MM/YYYY') departure_time
			from tickets tick
			join customers cust on tick.customer_id = cust.id
			join flights fli on tick.flight_id = fli.id
			join countries cor on fli.origin_country_id = cor.id
			join countries cde on fli.destination_country_id = cde.id
			where tick.customer_id =_customer_id
			order by fli.departure_time asc;

		end;

$BODY$;

ALTER FUNCTION public.get_tickets_by_customer(bigint)
    OWNER TO postgres;
