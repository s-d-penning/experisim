import numpy as np


def get_combinations(rows=0, cols=0, current_position=None) -> np.array:
    result = np.asarray([[(0, 0) for col in range(cols)] for row in range(rows)])
    if current_position is None:
        current_position = np.asarray([[row, 0] for row in range(rows)])

    for col in range(start=0, stop=cols, step=1):
        for row in range(start=rows, stop=0, step=-1):
            pass

    return None


if __name__ == '__main__':
    get_combinations(rows=3, cols=5)
    print('a')
