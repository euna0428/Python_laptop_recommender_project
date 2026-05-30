import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEPT_FILE = BASE_DIR / "department_specs.csv"
LAPTOP_FILE = BASE_DIR / "laptop_candidates.csv"
RESULT_FILE = BASE_DIR / "recommend_result.txt"


def money(value):
    return f"{int(value):,}원"


def storage_label(gb):
    gb = int(gb)
    if gb >= 1024:
        tb = gb / 1024
        return f"{tb:g}TB"
    return f"{gb}GB"


def parse_multi_choice(text):
    result = set()
    for part in text.replace(" ", "").split(','):
        if part in {"1", "2", "3"}:
            result.add(part)
    return result


def ask_number(prompt, default=None):
    while True:
        raw = input(prompt).strip().replace(',', '')
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("숫자로 입력해주세요. 예: 1500000")


def ask_choice(prompt, allowed, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        if raw in allowed:
            return raw
        print(f"{', '.join(allowed)} 중에서 입력해주세요.")


def os_filter(df, os_choice, can_install_windows):
    if os_choice == "1":  # Windows
        if can_install_windows == "1":
            return df[df["os_type"].isin(["Windows", "FreeDOS"])]
        return df[df["os_type"] == "Windows"]
    if os_choice == "2":  # macOS
        return df[df["os_type"] == "macOS"]
    return df


def score_laptop(row, spec, selected, user_budget):
    score = 0
    reasons = []
    avg_budget = int(spec["avg_budget_krw"])
    perf_cap = int(avg_budget * float(spec["performance_multiplier"]))
    preferred_weight = float(spec["max_weight_preferred_kg"])
    max_weight = float(spec["max_weight_limit_kg"])
    min_ram = int(spec["min_ram_gb"])
    min_storage = int(spec["min_storage_gb"])
    min_cpu = int(spec["min_cpu_score"])
    min_gpu = int(spec["min_gpu_score"])
    price_min = int(row["expected_price_min_krw"])
    price_max = int(row["expected_price_max_krw"])
    price_mid = (price_min + price_max) / 2

    # 기본 학과 스펙 점수
    if int(row["cpu_score"]) >= min_cpu:
        score += 25
        reasons.append("학과 권장 CPU 충족")
    if int(row["ram_gb"]) >= min_ram:
        score += 30
        reasons.append(f"RAM {int(row['ram_gb'])}GB로 권장 기준 충족")
    if int(row["storage_gb"]) >= min_storage:
        score += 20
        reasons.append(f"저장공간 {storage_label(row['storage_gb'])}로 권장 기준 충족")
    if int(row["gpu_score"]) >= min_gpu:
        score += 25
        reasons.append("학과 권장 GPU 기준 충족")

    # 사용자가 선택한 기준별 가중치
    if "1" in selected:  # 가격
        if price_max <= user_budget:
            score += 45
            reasons.append("사용자 예산 이내")
        elif price_min <= user_budget < price_max:
            score += 25
            reasons.append("예산 경계 구간: 옵션/할인에 따라 가능")
        else:
            score -= 80
            reasons.append("사용자 예산 초과")
        if price_mid <= int(spec["value_budget_krw"]):
            score += 20
            reasons.append("학과 가성비 예산 구간")

    if "2" in selected:  # 성능
        score += int(row["cpu_score"]) * 8
        score += int(row["gpu_score"]) * 8
        if int(row["ram_gb"]) >= min_ram * 2 and min_ram <= 16:
            score += 12
            reasons.append("권장 RAM보다 여유 있음")
        if price_mid <= perf_cap:
            score += 20
            reasons.append("성능 확장 예산 범위 이내")
        else:
            score -= 25
            reasons.append("성능 확장 예산 범위 초과")

    if "3" in selected:  # 휴대성
        weight = float(row["weight_kg"])
        if weight <= preferred_weight:
            score += 45
            reasons.append("휴대성 우수")
        elif weight <= max_weight:
            score += 18
            reasons.append("휴대 가능 마지노선 이내")
        else:
            score -= 60
            reasons.append("학과 기준 대비 무거움")

    # 과도한 저장장치 옵션 방지: 추천 기준보다 너무 높은 SSD는 가격 왜곡 가능
    if int(row["storage_gb"]) > min_storage * 2:
        score -= 20
        reasons.append("권장보다 저장공간이 과해 가격이 올라갈 수 있음")

    # 전체적인 예산 제어: 가격을 선택하지 않아도 너무 높은 제품은 감점만, 완전 배제는 아님
    if "1" not in selected and price_mid > user_budget * 1.35:
        score -= 35
        reasons.append("입력 예산보다 많이 높은 제품")

    return score, reasons


def print_and_collect(lines, text=""):
    print(text)
    lines.append(text)


def main():
    departments = pd.read_csv(DEPT_FILE, encoding="utf-8-sig")
    laptops = pd.read_csv(LAPTOP_FILE, encoding="utf-8-sig")

    print("학과별 노트북 추천 프로그램 v4")
    print("- 가격은 실시간 최저가가 아닌 조사 기반 예상 구매가 범위입니다.")
    print("- 링크는 추천 스펙 옵션이 들어간 모델 검색 링크입니다. 구매 전 옵션 확인이 필요합니다.\n")

    print("학과 목록")
    for idx, row in departments.iterrows():
        print(f"{idx + 1}. {row['department']}")

    dept_no = ask_number("\n학과 번호를 선택하세요: ")
    while dept_no < 1 or dept_no > len(departments):
        dept_no = ask_number("목록에 있는 학과 번호를 다시 선택하세요: ")
    spec = departments.iloc[dept_no - 1]

    user_budget = ask_number("\n사용 가능한 최대 예산을 입력하세요. 예: 1500000 : ")

    print("\n중요하게 보는 기준을 선택하세요. 두 개 이상 선택 가능")
    print("1. 가격")
    print("2. 성능")
    print("3. 휴대성")
    print("예: 가격+성능은 1,2 / 전체는 1,2,3")
    selected = parse_multi_choice(input("선택: "))
    if not selected:
        selected = {"1"}
        print("선택값이 없어 기본값 '가격'으로 진행합니다.")

    print("\n사용할 운영체제를 선택하세요.")
    print("1. Windows")
    print("2. macOS")
    print("3. 상관없음")
    os_choice = ask_choice("선택: ", {"1", "2", "3"}, default="3")

    can_install_windows = "2"
    if os_choice == "1":
        print("\nFreeDOS 제품은 Windows가 미설치되어 더 저렴한 경우가 있습니다.")
        print("Windows를 직접 설치할 수 있나요?")
        print("1. 가능")
        print("2. 불가능")
        can_install_windows = ask_choice("선택: ", {"1", "2"}, default="2")

    filtered = os_filter(laptops, os_choice, can_install_windows)

    # 학과 태그 우선 필터. 후보가 너무 적으면 전체에서 평가.
    dept_name = spec["department"]
    tag_filtered = filtered[filtered["suitable_tags"].astype(str).str.contains(dept_name.split('/')[0], na=False)]
    if len(tag_filtered) >= 5:
        filtered = tag_filtered

    scores = []
    for _, row in filtered.iterrows():
        score, reasons = score_laptop(row, spec, selected, user_budget)
        scores.append((score, reasons))
    if len(scores) == 0:
        print("조건에 맞는 노트북 후보가 없습니다. OS 조건 또는 예산을 넓혀주세요.")
        return

    filtered = filtered.copy()
    filtered["score"] = [s[0] for s in scores]
    filtered["reasons"] = ["; ".join(s[1][:5]) for s in scores]
    filtered = filtered.sort_values(by=["score", "expected_price_min_krw"], ascending=[False, True]).head(5)

    lines = []
    print_and_collect(lines, "\n선택 학과 권장 스펙")
    print_and_collect(lines, f"- 학과: {spec['department']}")
    print_and_collect(lines, f"- 주요 사용 목적: {spec['main_usage']}")
    print_and_collect(lines, f"- 권장 CPU: {spec['recommended_cpu']}")
    print_and_collect(lines, f"- 최소 RAM: {int(spec['min_ram_gb'])}GB")
    print_and_collect(lines, f"- 최소 저장공간: {storage_label(spec['min_storage_gb'])}")
    print_and_collect(lines, f"- 권장 GPU: {spec['recommended_gpu']}")
    print_and_collect(lines, f"- 학과 평균 권장 예산: {money(spec['avg_budget_krw'])}")
    print_and_collect(lines, f"- 학과 가성비 예산 기준: {money(spec['value_budget_krw'])}")
    print_and_collect(lines, f"- 성능 확장 예산 상한: {money(int(spec['avg_budget_krw'] * spec['performance_multiplier']))}")
    print_and_collect(lines, f"- 사용자가 입력한 최대 예산: {money(user_budget)}")
    print_and_collect(lines, f"- 참고: {spec['note']}")

    selected_text = []
    if "1" in selected: selected_text.append("가격")
    if "2" in selected: selected_text.append("성능")
    if "3" in selected: selected_text.append("휴대성")
    print_and_collect(lines, f"\n선택 기준: {', '.join(selected_text)}")

    print_and_collect(lines, "\n추천 노트북 TOP 5")
    for i, (_, row) in enumerate(filtered.iterrows(), start=1):
        print_and_collect(lines, f"\n{i}. {row['brand']} {row['model']}")
        print_and_collect(lines, f"   추천 점수: {int(row['score'])}점")
        print_and_collect(lines, f"   CPU: {row['cpu']}")
        print_and_collect(lines, f"   RAM: {int(row['ram_gb'])}GB")
        print_and_collect(lines, f"   저장공간: {storage_label(row['storage_gb'])}")
        print_and_collect(lines, f"   GPU: {row['gpu']}")
        print_and_collect(lines, f"   OS: {row['os_type']}")
        print_and_collect(lines, f"   예상 구매가 범위: {money(row['expected_price_min_krw'])} ~ {money(row['expected_price_max_krw'])}")
        print_and_collect(lines, f"   무게: {row['weight_kg']}kg")
        print_and_collect(lines, f"   추천 이유: {row['reasons']}")
        print_and_collect(lines, f"   옵션 일치 검색어: {row['option_matched_search_query']}")
        print_and_collect(lines, f"   모델 검색 링크: {row['model_search_link']}")
        print_and_collect(lines, f"   가격 기준 메모: {row['price_basis_note']}")
        print_and_collect(lines, "   구매 전 확인: RAM/SSD/GPU/OS 옵션이 위 스펙과 같은지 확인")

    print_and_collect(lines, "\n주의")
    print_and_collect(lines, "- 예상 구매가 범위는 2026년 메모리/SSD 가격 상승과 국내 가격비교 검색 결과를 반영한 참고 범위입니다.")
    print_and_collect(lines, "- 링크는 정확한 옵션을 찾기 위한 검색 링크이며, 쇼핑몰 정렬/재고/옵션에 따라 다른 제품이 섞일 수 있습니다.")
    print_and_collect(lines, "- 실제 구매 전 Windows 포함 여부, FreeDOS 여부, RAM/SSD/GPU 옵션을 반드시 확인해야 합니다.")

    RESULT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n추천 결과가 {RESULT_FILE.name} 파일로 저장되었습니다.")


if __name__ == "__main__":
    main()
