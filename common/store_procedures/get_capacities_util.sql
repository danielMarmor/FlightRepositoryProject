-- FUNCTION: public.get_capacities_util(text, text, bigint)

DROP FUNCTION IF EXISTS public.get_capacities_util(text, text, bigint);

CREATE OR REPLACE FUNCTION public.get_capacities_util(
	_start_date text,
	_end_date text,
	_destination_country_id bigint)
    RETURNS TABLE(num_seats numeric, remaining_tickets numeric, sold_tickets numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
		    return QUERY
			select
			cast(sum(fli.num_seats) as numeric) num_seats,
			cast(sum(fli.remaining_tickets) as numeric) remaining_tickets,
			cast(sum(fli.num_seats - fli.remaining_tickets) as numeric) sold_tickets
			from
			flights fli
			where fli.departure_time >= to_date(_start_date, 'DD/MM/YYYY') and
			fli.departure_time < to_date(_end_date, 'DD/MM/YYYY') and
			(_destination_country_id = -1  or fli.destination_country_id = _destination_country_id);

		end;

$BODY$;

ALTER FUNCTION public.get_capacities_util(text, text, bigint)
    OWNER TO postgres;
