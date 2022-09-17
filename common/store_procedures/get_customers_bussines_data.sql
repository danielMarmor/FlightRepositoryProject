-- FUNCTION: public.get_customers_bussines_data(character varying)

DROP FUNCTION IF EXISTS public.get_customers_bussines_data(character varying);

CREATE OR REPLACE FUNCTION public.get_customers_bussines_data(
	_search character varying)
    RETURNS TABLE(id bigint, first_name character varying, last_name character varying, image_url character varying, last_activity_date timestamp without time zone, email character varying, address character varying, phone_number character varying, num_tickets bigint, total_purchases numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		declare EMPTY_DATE timestamp without time zone:=TO_DATE('01/01/0001', 'DD/MM/YYYY');
		begin
		    return QUERY
			select
			cust.id,
		 	cust.first_name,
		 	cust.last_name,
		 	cust.image_url,
			max(coalesce(fli.departure_time, EMPTY_DATE)) last_activity_date,
		 	usr.email,
		 	cust.address,
		 	cust.phone_number,
			COUNT(coalesce(tick.id, 0)) num_tickets,
			SUM(coalesce(fli.price, 0)) total_purchases
			from customers cust
			join users usr on cust.user_id = usr.id
			left join tickets tick on cust.id = tick.customer_id
			left join flights fli on coalesce(tick.flight_id , 0) =fli.id
			where
			(_search is null
			or
			((lower(cust.first_name) || ' ' || lower(cust.last_name)) like ('%' || lower(_search) || '%')
		     or ((lower(cust.last_name) || ' ' || lower(cust.first_name)) like ('%' || lower(_search) || '%'))))
			group by
		 	cust.id,
		 	cust.first_name,
		 	cust.last_name,
		 	cust.image_url,
		 	usr.email,
		 	cust.address;
		end;

$BODY$;

ALTER FUNCTION public.get_customers_bussines_data(character varying)
    OWNER TO postgres;
