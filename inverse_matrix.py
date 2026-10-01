from fractions import Fraction


def read_matrix() -> list[list[int]]:
    while True:
        try:
            n = int(input("정방행렬의 차수를 입력하세요: "))
            if n <= 0:
                raise ValueError
            break
        except ValueError:
            print("입력 오류: n은 1 이상의 정수여야 합니다.")

    print(f"각 행에 정수 {n}개를 공백으로 구분해 입력하세요.")
    matrix = []
    for i in range(n):
        while True:
            try:
                row = list(map(int, input(f"{i + 1}행: ").split()))
                if len(row) != n:
                    raise ValueError
                matrix.append(row)
                break
            except ValueError:
                print(f"입력 오류: 정수 {n}개를 공백으로 구분해 입력하세요.")
    return matrix


def minor_matrix(matrix, row, col):
    return [[value for j, value in enumerate(values) if j != col]
            for i, values in enumerate(matrix) if i != row]


def determinant(matrix):
    n = len(matrix)
    if n == 0:
        return 1  # 1×1 행렬의 여인수 계산용
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return sum((-1) ** j * matrix[0][j]
               * determinant(minor_matrix(matrix, 0, j)) for j in range(n))


def inverse_by_determinant(matrix):
    n = len(matrix)
    det = determinant(matrix)
    if det == 0:
        raise ValueError("행렬식이 0이므로 역행렬이 존재하지 않습니다.")

    cofactors = [[(-1) ** (i + j)
                 * determinant(minor_matrix(matrix, i, j))
                 for j in range(n)] for i in range(n)]
    # 여인수 행렬을 전치하고 행렬식으로 나눔
    return [[Fraction(cofactors[j][i], det)
             for j in range(n)] for i in range(n)]


def inverse_by_gauss_jordan(matrix):
    # [A | I]를 [I | A^-1]로 변환
    n = len(matrix)
    aug = [[Fraction(value) for value in row]
           + [Fraction(int(i == j)) for j in range(n)]
           for i, row in enumerate(matrix)]

    for col in range(n):
        pivot_row = col
        while pivot_row < n and aug[pivot_row][col] == 0:
            pivot_row += 1
        if pivot_row == n:
            raise ValueError("행렬식이 0이므로 역행렬이 존재하지 않습니다.")
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        pivot = aug[col][col]
        aug[col] = [value / pivot for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][j] - factor * aug[col][j]
                        for j in range(2 * n)]
    return [row[n:] for row in aug]


def print_matrix(matrix):
    text = [[str(value) for value in row] for row in matrix]
    width = max(len(value) for row in text for value in row)
    for row in text:
        print("[ " + "  ".join(value.rjust(width) for value in row) + " ]")


def compare_results(first, second):
    if first is None and second is None:
        return "두 방법 모두 역행렬이 없어 결과 비교를 생략합니다."
    if first is None or second is None:
        return "두 방법의 역행렬 존재 여부가 다릅니다."
    if first == second:
        return "두 방법의 결과가 동일합니다."
    return "두 방법의 결과가 다릅니다."


def main():
    matrix = read_matrix()
    print("\n[1] 입력한 행렬")
    print_matrix(matrix)
    first = second = None

    print("\n[2] 행렬식으로 구한 역행렬")
    print(f"det(A) = {determinant(matrix)}")
    try:
        first = inverse_by_determinant(matrix)
        print_matrix(first)
    except ValueError as error:
        print(f"오류: {error}")

    print("\n[3] 가우스-조던 소거법으로 구한 역행렬")
    try:
        second = inverse_by_gauss_jordan(matrix)
        print_matrix(second)
    except ValueError as error:
        print(f"오류: {error}")

    print("\n[4] 결과 비교")
    print(compare_results(first, second))


if __name__ == "__main__":
    main()
