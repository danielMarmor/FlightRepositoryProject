from common.constants.enums import Actions

def test_api(requests):
    for i in range(10):
        payload = {'facade_name': 'anonym', 'action_id': Actions.GET_ALL_FLIGHTS, 'data': None}
        requests.send_request(payload, False)
        results = requests.get_response()
        print(i)
        print(results)






