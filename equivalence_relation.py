A = [1, 2, 3, 4, 5]
N = len(A)


# ──────────────────────────────────────────────
# 출력 유틸
# ──────────────────────────────────────────────
def print_line(ch="=", n=50):
    print(ch * n)


def print_matrix(M, title="관계행렬"):
    """관계행렬을 행/열 번호와 함께 출력"""
    print(f"[{title}]")
    print("     " + "  ".join(str(a) for a in A))
    print("   +" + "-" * (3 * N))
    for i in range(N):
        print(f" {A[i]} | " + "  ".join(str(v) for v in M[i]))
    print()


def copy_matrix(M):
    return [row[:] for row in M]


# ──────────────────────────────────────────────
# 조건 1. 관계행렬 입력 기능
# ──────────────────────────────────────────────
def input_matrix():
    """5x5 관계행렬을 행 단위로 입력받아 2차원 리스트로 저장"""
    print(f"집합 A = {{{', '.join(map(str, A))}}} 에 대한 {N}x{N} 관계행렬을 입력하세요.")
    print("각 행마다 0 또는 1을 공백으로 구분해 5개 입력 (예: 1 0 0 1 0)\n")
    M = []
    for i in range(N):
        row = [int(v) for v in input(f"{A[i]}행 입력: ").split()]
        M.append(row)
    print()
    return M


# ──────────────────────────────────────────────
# 조건 2. 동치 관계 판별 기능  (+ 추가기능: 반례 출력)
# ──────────────────────────────────────────────
def is_reflexive(M, verbose=False):
    """반사관계: 모든 a에 대해 (a,a) ∈ R"""
    for i in range(N):
        if M[i][i] != 1:
            if verbose:
                print(f"    └ 반례: ({A[i]},{A[i]}) ∉ R")
            return False
    return True


def is_symmetric(M, verbose=False):
    """대칭관계: (a,b) ∈ R 이면 (b,a) ∈ R"""
    for i in range(N):
        for j in range(N):
            if M[i][j] == 1 and M[j][i] != 1:
                if verbose:
                    print(f"    └ 반례: ({A[i]},{A[j]}) ∈ R 이지만 ({A[j]},{A[i]}) ∉ R")
                return False
    return True


def is_transitive(M, verbose=False):
    """추이관계: (a,b) ∈ R 이고 (b,c) ∈ R 이면 (a,c) ∈ R"""
    for i in range(N):
        for j in range(N):
            if M[i][j] == 1:
                for k in range(N):
                    if M[j][k] == 1 and M[i][k] != 1:
                        if verbose:
                            print(f"    └ 반례: ({A[i]},{A[j]}), ({A[j]},{A[k]}) ∈ R 이지만 "
                                  f"({A[i]},{A[k]}) ∉ R")
                        return False
    return True


def check_properties(M):
    """세 가지 성질 판별 결과를 출력(만족하지 않으면 반례도 출력)하고 (반사, 대칭, 추이) 반환"""
    mark = lambda b: "O" if b else "X"
    print("[관계의 성질 판별]")
    r = is_reflexive(M)
    print(f"  반사관계 : {mark(r)}")
    if not r:
        is_reflexive(M, verbose=True)
    s = is_symmetric(M)
    print(f"  대칭관계 : {mark(s)}")
    if not s:
        is_symmetric(M, verbose=True)
    t = is_transitive(M)
    print(f"  추이관계 : {mark(t)}")
    if not t:
        is_transitive(M, verbose=True)
    print()
    return r, s, t


def is_equivalence(M):
    return is_reflexive(M) and is_symmetric(M) and is_transitive(M)


def print_equivalence_result(M):
    if is_equivalence(M):
        print("▶ 반사, 대칭, 추이 관계를 모두 만족하므로 동치관계입니다.\n")
        return True
    print("▶ 반사, 대칭, 추이 관계 중 만족하지 않는 성질이 있으므로 동치관계가 아닙니다.\n")
    return False


# ──────────────────────────────────────────────
# 조건 3. 동치류 출력 기능
# ──────────────────────────────────────────────
def equivalence_class(M, a):
    """원소 a의 동치류 [a] = { x ∈ A | (a, x) ∈ R }"""
    i = A.index(a)
    return [A[j] for j in range(N) if M[i][j] == 1]


def print_equivalence_classes(M):
    """집합의 각 원소에 대한 동치류를 각각 출력"""
    print("[동치류]")
    for a in A:
        cls = equivalence_class(M, a)
        print(f"  [{a}] = {{{', '.join(map(str, cls))}}}")
    print()


# ──────────────────────────────────────────────
# 조건 4. 폐포 구현 기능
# ──────────────────────────────────────────────
def reflexive_closure(M):
    """반사폐포: R ∪ {(a,a) | a ∈ A}  → 대각 원소를 모두 1로"""
    S = copy_matrix(M)
    for i in range(N):
        S[i][i] = 1
    return S


def symmetric_closure(M):
    """대칭폐포: R ∪ R^-1  → M[i][j] = 1 이면 M[j][i] = 1"""
    S = copy_matrix(M)
    for i in range(N):
        for j in range(N):
            if M[i][j] == 1:
                S[j][i] = 1
    return S


def transitive_closure(M):
    """추이폐포: 와샬(Warshall) 알고리즘
    W_k[i][j] = W_(k-1)[i][j] OR (W_(k-1)[i][k] AND W_(k-1)[k][j])"""
    W = copy_matrix(M)
    for k in range(N):
        for i in range(N):
            for j in range(N):
                W[i][j] = W[i][j] or (W[i][k] and W[k][j])
    return W


def apply_closures(M, r, s):
    """만족하지 않는 성질에 대해 반사 → 대칭 → 추이 순서로 폐포 적용
    (추이폐포는 반사·대칭성을 유지하므로 마지막에 적용해야 동치관계가 보장됨)"""
    S = copy_matrix(M)

    if not r:
        print_line("-")
        print(" [반사폐포 변환]")
        print_line("-")
        print_matrix(S, "변환 전")
        S = reflexive_closure(S)
        print_matrix(S, "반사폐포 변환 후")

    if not s:
        print_line("-")
        print(" [대칭폐포 변환]  R ∪ R⁻¹")
        print_line("-")
        print_matrix(S, "변환 전")
        S = symmetric_closure(S)
        print_matrix(S, "대칭폐포 변환 후")

    # 반사·대칭폐포 적용 후 추이성이 새로 깨질 수 있으므로 다시 검사
    if not is_transitive(S):
        print_line("-")
        print(" [추이폐포 변환]  와샬 알고리즘")
        print_line("-")
        print_matrix(S, "변환 전")
        S = transitive_closure(S)
        print_matrix(S, "추이폐포 변환 후")

    return S


# ──────────────────────────────────────────────
# main
# ──────────────────────────────────────────────
def main():
    print_line()
    print(" 이산수학 Report 2 : 동치관계 판별 프로그램")
    print_line()
    M = input_matrix()

    print_line()
    print(" STEP 1. 입력된 관계")
    print_line()
    print_matrix(M, "입력된 관계행렬 R")

    print_line()
    print(" STEP 2. 동치관계 판별")
    print_line()
    r, s, t = check_properties(M)

    if print_equivalence_result(M):
        print_line()
        print(" STEP 3. 동치류 출력")
        print_line()
        print_equivalence_classes(M)
        return

    print_line()
    print(" STEP 3. 폐포 변환")
    print_line()
    S = apply_closures(M, r, s)

    print_line()
    print(" STEP 4. 폐포 변환 후 동치관계 재판별")
    print_line()
    print_matrix(S, "최종 관계행렬")
    check_properties(S)
    if print_equivalence_result(S):
        print_line()
        print(" STEP 5. 동치류 출력")
        print_line()
        print_equivalence_classes(S)


if __name__ == "__main__":
    main()