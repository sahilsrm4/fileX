import time

def print_star_pattern(n=5):
    for i in range(1, n + 1):
        print('* ' * i)

if __name__ == '__main__':
    print('--- Star Pattern ---')
    print_star_pattern(5)
    print('Waiting 2 seconds to view output...')
    time.sleep(2)
    print('Done!')
