-- FUNCTION: public.get_purchases_by_customers(text, text, bigint)

DROP FUNCTION IF EXISTS public.get_purchases_by_customers(text, text, bigint);

CREATE OR REPLACE FUNCTION public.get_purchases_by_customers(
	_start_date text,
	_end_date text,
	_destination_country_id bigint)
    RETURNS TABLE(customer_id bigint, customer_name text, count_tickets bigint, sum_purchases numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
		    return QUERY
			select * from
			(select
			cust.id customer_id,
			(cust.first_name || ' ' || cust.last_name) customer_name,
			count(tick.id) count_tickets,
			sum(tick.price) sum_purchases
			from
			flights fli
			join tickets tick on fli.id = tick.flight_id
			join customers cust on tick.customer_id = cust.id
			where fli.departure_time >= to_date(_start_date, 'DD/MM/YYYY') and
			fli.departure_time < to_date(_end_date, 'DD/MM/YYYY') and
			(fli.destination_country_id = _destination_country_id or _destination_country_id = -1)
			group by
			cust.id,
			cust.first_name || ' ' || cust.last_name) customers
			order by customers.sum_purchases desc
			limit 20;
		end;

$BODY$;

ALTER FUNCTION public.get_purchases_by_customers(text, text, bigint)
    OWNER TO postgres;
