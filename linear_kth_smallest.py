from typing import Sequence


def _kth_smallest_element(
    *,
    array: list[float],
    left: int,
    right: int,
    k: int,
) -> float:
    if k < 0 or k > right - left + 1:
        raise ValueError('k is out of range')

    if len(array) == 1:
        return array[0]

    n: int = right - left + 1
    medians: list[float] = []
    i: int = 0
    while i < n // 5:
        new_left: int = left + i * 5
        median: float = find_median(
            array=array,
            left=new_left,
            right=new_left + 4,
        )
        medians.append(median)
        i += 1
    if i * 5 < n:
        new_left = left + i * 5
        median = find_median(
            array=array,
            left=new_left,
            right=new_left + n % 5 - 1,
        )
        medians.append(median)

    if len(medians) == 1:
        return medians[0]

    median_of_medians = _kth_smallest_element(
        array=medians,
        left=0,
        right=i - 1,
        k=i // 2,
    )

    position: int = partition(
        array=array,
        left=left,
        right=right,
        around=median_of_medians,
    )
    if position - left == k - 1:
        return array[position]
    if position - left > k - 1:
        return _kth_smallest_element(
            array=array,
            left=left,
            right=position - 1,
            k=k,
        )
    return _kth_smallest_element(
        array=array,
        left=position + 1,
        right=right,
        k=k - position + left - 1,
    )


def swap(
    *,
    array: list[float],
    a: int,
    b: int,
) -> None:
    array[a], array[b] = array[b], array[a]


def partition(
    *,
	array: list[float],
	left: int,
	right: int,
	around: float,
) -> int:
    for i in range(left, right):
        if array[i] == around:
            swap(
                array=array,
                a=right,
                b=i,
            )
            break

    around = array[right]
    i = left
    for j in range(left, right):
        if (array[j] <= around):
            swap(
                array=array,
                a=i,
                b=j,
            )
            i += 1
    swap(
        array=array,
        a=i,
        b=right,
    )
    return i


def find_median(
    *,
    array: list[float],
    left: int,
    right: int,
) -> float:
    part: list[float] = []
    for i in range(left, right + 1):
        part.append(array[i])
    part.sort()
    return part[len(part) // 2]


def kth_smallest_element(
    array: Sequence[float],
    k: int,
) -> float:
    return _kth_smallest_element(
        array=list(array),
        left=0,
        right=len(array) - 1,
        k=k,
    )


# THIS IS NOT WORKING :(((((())))))
if __name__ == '__main__':
    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    k = 7
    print("K'th smallest element is",
        kth_smallest_element(
            array=array,
            k=k,
        )
    )
