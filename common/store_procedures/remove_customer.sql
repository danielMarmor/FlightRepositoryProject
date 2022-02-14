DROP PROCEDURE IF EXISTS public.remove_customer(bigint);

CREATE OR REPLACE PROCEDURE public.remove_customer(
	IN _customer_id bigint)
LANGUAGE 'plpgsql'
AS $BODY$
	declare customer_user_id bigint;
	begin
		select cust.user_id into customer_user_id
		from customers cust
		where cust.id =_customer_id;
		delete from customers cust
		where cust.id = _customer_id;
		--USER
		delete from users usr
		where usr.id = customer_user_id;
	end;
$BODY$;