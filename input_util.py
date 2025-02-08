def get_int(prompt) -> int:
    while True:
        maybe_number = input(prompt)
        try:
            return int(maybe_number)
        except:
            print(f"Try again. {maybe_number} is not an integer.")
