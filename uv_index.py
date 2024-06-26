import json, requests, ast, Constants


# Get the max UV index over the next day from openuv.io
# NOTE: Max 50 requests/day on free tier
def get_max_uv_index(lat: float, lng: float) -> float:
	response = requests.get(
		f"https://api.openuv.io/api/v1/forecast?lat={lat}&lng={lng}",
		headers={
			"Content-Type": "application/json",
			"x-access-token": f"{Constants.API_KEY}"
		},
		allow_redirects=True
	)

	if not response.ok:
		print("Failed to retreive valid response")
		print(response)
		print(response.content)
		raise response.raise_for_status()

	content = ast.literal_eval(response.content.decode('utf-8'))

	max_uv_index = max(time['uv'] for time in content['result'])
	return max_uv_index


# Time to burn in minutes according to Fitzpatrick scale
def time_to_burn(uv_index: float, skin_type: int) -> float:
	if skin_type < 1 or skin_type > 6:
		raise ValueError('skin_type should be 1-6 based on Fitzpatrick scale')
	
	skin_type_to_skin_factor = {1: 2.5, 2: 3, 3: 4, 4: 5, 5: 8, 6: 15}
	return (200*skin_type_to_skin_factor[skin_type])/(3*uv_index)


def main() -> None:
	uv_index = get_max_uv_index(lat=-37.75, lng=145.00)

	print(f"Max UV index: {uv_index:.2f}")
	print(f"Time to burn: {int(time_to_burn(uv_index, skin_type=2))} minutes")


if __name__ == '__main__':
	main()