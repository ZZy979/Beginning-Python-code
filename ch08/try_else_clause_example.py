while True:
    try:
        x = input('Enter the first number: ')
        y = input('Enter the second number: ')
        print(eval(f'{x} / {y}'))
    except Exception as e:
        print('Invalid input:', e)
        print('Please try again.')
    else:
        break
