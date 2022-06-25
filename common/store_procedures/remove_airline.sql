DROP PROCEDURE IF EXISTS public.remove_airline(bigint);
CREATE OR REPLACE PROCEDURE public.remove_airline(
	IN _airline_company_id bigint)
    LANGUAGE 'plpgsql'
AS $BODY$
	declare airline_user_id bigint;
	begin
		select ac.user_id into airline_user_id from
		airine_companies ac
		where ac.id =_airline_company_id;
		--TICKETS
		delete from tickets tick
		where tick.flight_id in
		(select fli.id from flights fli
		where fli.airline_company_id = _airline_company_id);
		--FLIGHTS
			delete from flights fli
		where fli.airline_company_id = _airline_company_id;
		   --AIRLINE COMPANY
		delete from airine_companies ac
		where ac.id = _airline_company_id;
		--USER
		delete from users usr
		where usr.id = airline_user_id;
	end;
$BODY$;

ALTER PROCEDURE public.remove_airline(bigint)
    OWNER TO postgres;