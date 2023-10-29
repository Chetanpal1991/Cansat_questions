def send_signal_to_earth(Z):
    current_sum = 0
    received_value = Z

    while current_sum < received_value:
        next_number = find_next_number(current_sum, received_value)
        if next_number == -1:
            return False
        current_sum += next_number
        if current_sum > received_value:  # Check if the current sum exceeds the received value
            return False

    return current_sum == received_value

def find_next_number(current_sum, received_value):
    diff = received_value - current_sum
    num_digits = len(str(diff))

    if num_digits > 1 :
        return int('1' * num_digits)
    else:
        return -1


Z = int(input("Enter the signal that was received \n"))  # Example received value from the planet
can_send_signal = send_signal_to_earth(Z)
if can_send_signal:
    print("Signal successfully sent back to Earth!")
else:
    print("Unable to send signal back to Earth.")
