from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DEPT_FILE = DATA_DIR / "department_specs.csv"
LAPTOP_FILE = DATA_DIR / "laptop_candidates.csv"
IMAGE_MAP_FILE = DATA_DIR / "laptop_image_mapping.csv"

PRIORITY_TO_LEGACY = {
    "price": "1",
    "performance": "2",
    "weight": "3",
}

OS_LABELS = {
    "windows": "Windows",
    "macos": "macOS",
    "freedos": "FreeDOS",
    "any": "상관없음",
}


def money(value: int | float) -> str:
    return f"{int(value):,}원"


def storage_label(gb: int | float | str) -> str:
    gb_int = int(float(gb))
    if gb_int >= 1024:
        return f"{gb_int / 1024:g}TB"
    return f"{gb_int}GB"


@lru_cache(maxsize=1)
def load_departments() -> pd.DataFrame:
    return pd.read_csv(DEPT_FILE, encoding="utf-8-sig")


@lru_cache(maxsize=1)
def load_laptops() -> pd.DataFrame:
    laptops = pd.read_csv(LAPTOP_FILE, encoding="utf-8-sig")
    image_map = pd.read_csv(IMAGE_MAP_FILE, encoding="utf-8-sig")
    image_lookup = {
        (str(row["brand"]).strip(), str(row["model"]).strip()): row["png"]
        for _, row in image_map.iterrows()
    }

    def image_path(row: pd.Series) -> str:
        file_name = image_lookup.get((str(row["brand"]).strip(), str(row["model"]).strip()))
        if not file_name:
            safe_model = str(row["model"]).lower().replace(" ", "-")
            file_name = f"fallback-{safe_model}.png"
        return f"/laptops/{file_name}"

    laptops = laptops.copy()
    laptops["image_path"] = laptops.apply(image_path, axis=1)
    return laptops


def get_department_by_name(department: str) -> pd.Series:
    departments = load_departments()
    match = departments[departments["department"] == department]
    if match.empty:
        raise ValueError(f"존재하지 않는 학과입니다: {department}")
    return match.iloc[0]


def os_filter(df: pd.DataFrame, os_choice: str, can_install_windows: bool) -> pd.DataFrame:
    if os_choice == "windows":
        if can_install_windows:
            return df[df["os_type"].isin(["Windows", "FreeDOS"])]
        return df[df["os_type"] == "Windows"]
    if os_choice == "macos":
        return df[df["os_type"] == "macOS"]
    if os_choice == "freedos":
        return df[df["os_type"] == "FreeDOS"]
    return df


def score_laptop(row: pd.Series, spec: pd.Series, selected: set[str], user_budget: int) -> tuple[int, list[str], dict[str, int]]:
    score = 0
    reasons: list[str] = []
    breakdown = {"spec": 0, "price": 0, "performance": 0, "weight": 0, "penalty": 0}

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

    if int(row["cpu_score"]) >= min_cpu:
        score += 25
        breakdown["spec"] += 25
        reasons.append("학과 권장 CPU 충족")
    if int(row["ram_gb"]) >= min_ram:
        score += 30
        breakdown["spec"] += 30
        reasons.append(f"RAM {int(row['ram_gb'])}GB로 권장 기준 충족")
    if int(row["storage_gb"]) >= min_storage:
        score += 20
        breakdown["spec"] += 20
        reasons.append(f"저장공간 {storage_label(row['storage_gb'])}로 권장 기준 충족")
    if int(row["gpu_score"]) >= min_gpu:
        score += 25
        breakdown["spec"] += 25
        reasons.append("학과 권장 GPU 기준 충족")

    if "1" in selected:
        if price_max <= user_budget:
            score += 45
            breakdown["price"] += 45
            reasons.append("사용자 예산 이내")
        elif price_min <= user_budget < price_max:
            score += 25
            breakdown["price"] += 25
            reasons.append("예산 경계 구간: 옵션/할인에 따라 가능")
        else:
            score -= 80
            breakdown["penalty"] -= 80
            reasons.append("사용자 예산 초과")
        if price_mid <= int(spec["value_budget_krw"]):
            score += 20
            breakdown["price"] += 20
            reasons.append("학과 가성비 예산 구간")

    if "2" in selected:
        perf_score = int(row["cpu_score"]) * 8 + int(row["gpu_score"]) * 8
        score += perf_score
        breakdown["performance"] += perf_score
        if int(row["ram_gb"]) >= min_ram * 2 and min_ram <= 16:
            score += 12
            breakdown["performance"] += 12
            reasons.append("권장 RAM보다 여유 있음")
        if price_mid <= perf_cap:
            score += 20
            breakdown["performance"] += 20
            reasons.append("성능 확장 예산 범위 이내")
        else:
            score -= 25
            breakdown["penalty"] -= 25
            reasons.append("성능 확장 예산 범위 초과")

    if "3" in selected:
        weight = float(row["weight_kg"])
        if weight <= preferred_weight:
            score += 45
            breakdown["weight"] += 45
            reasons.append("휴대성 우수")
        elif weight <= max_weight:
            score += 18
            breakdown["weight"] += 18
            reasons.append("휴대 가능 마지노선 이내")
        else:
            score -= 60
            breakdown["penalty"] -= 60
            reasons.append("학과 기준 대비 무거움")

    if int(row["storage_gb"]) > min_storage * 2:
        score -= 20
        breakdown["penalty"] -= 20
        reasons.append("권장보다 저장공간이 과해 가격이 올라갈 수 있음")

    if "1" not in selected and price_mid > user_budget * 1.35:
        score -= 35
        breakdown["penalty"] -= 35
        reasons.append("입력 예산보다 많이 높은 제품")

    return int(score), reasons, breakdown


def department_to_dict(row: pd.Series, index: int) -> dict[str, Any]:
    return {
        "id": int(index + 1),
        "department": row["department"],
        "mainUsage": row["main_usage"],
        "recommendedCpu": row["recommended_cpu"],
        "minCpuScore": int(row["min_cpu_score"]),
        "minRamGb": int(row["min_ram_gb"]),
        "minStorageGb": int(row["min_storage_gb"]),
        "recommendedGpu": row["recommended_gpu"],
        "minGpuScore": int(row["min_gpu_score"]),
        "avgBudgetKrw": int(row["avg_budget_krw"]),
        "valueBudgetKrw": int(row["value_budget_krw"]),
        "performanceMultiplier": float(row["performance_multiplier"]),
        "maxWeightPreferredKg": float(row["max_weight_preferred_kg"]),
        "maxWeightLimitKg": float(row["max_weight_limit_kg"]),
        "note": row["note"],
    }


def laptop_to_dict(row: pd.Series, rank: int | None = None) -> dict[str, Any]:
    price_min = int(row["expected_price_min_krw"])
    price_max = int(row["expected_price_max_krw"])
    result = {
        "rank": rank,
        "brand": row["brand"],
        "model": row["model"],
        "name": f"{row['brand']} {row['model']}",
        "cpu": row["cpu"],
        "cpuScore": int(row["cpu_score"]),
        "ramGb": int(row["ram_gb"]),
        "storageGb": int(row["storage_gb"]),
        "storageLabel": storage_label(row["storage_gb"]),
        "gpu": row["gpu"],
        "gpuScore": int(row["gpu_score"]),
        "priceMinKrw": price_min,
        "priceMaxKrw": price_max,
        "priceMidKrw": int((price_min + price_max) / 2),
        "priceLabel": f"{price_min // 10000:,}~{price_max // 10000:,}만원",
        "weightKg": float(row["weight_kg"]),
        "osType": row["os_type"],
        "display": row["display"],
        "suitableTags": str(row["suitable_tags"]).split("/"),
        "optionMatchedSearchQuery": row["option_matched_search_query"],
        "modelSearchLink": row["model_search_link"],
        "priceBasisNote": row["price_basis_note"],
        "mustCheckBeforeBuy": row["must_check_before_buy"],
        "imagePath": row.get("image_path", ""),
    }
    if "score" in row:
        result["score"] = int(row["score"])
    if "reasons" in row:
        result["reasons"] = str(row["reasons"]).split("; ") if str(row["reasons"]) else []
    if "scoreBreakdown" in row:
        result["scoreBreakdown"] = row["scoreBreakdown"]
    return result


def recommend(payload: dict[str, Any]) -> dict[str, Any]:
    department = payload["department"]
    budget = int(payload["budget"])
    priorities = payload.get("priorities") or ["price"]
    os_choice = payload.get("os") or "any"
    can_install_windows = bool(payload.get("canInstallWindows", False))
    limit = int(payload.get("limit", 5))

    spec = get_department_by_name(department)
    laptops = load_laptops()
    filtered = os_filter(laptops, os_choice, can_install_windows)

    dept_keyword = str(spec["department"]).split("/")[0]
    tag_filtered = filtered[filtered["suitable_tags"].astype(str).str.contains(dept_keyword, na=False)]
    if len(tag_filtered) >= 5:
        filtered = tag_filtered

    selected = {PRIORITY_TO_LEGACY[p] for p in priorities if p in PRIORITY_TO_LEGACY}
    if not selected:
        selected = {"1"}

    scored_rows = []
    for _, row in filtered.iterrows():
        score, reasons, breakdown = score_laptop(row, spec, selected, budget)
        new_row = row.copy()
        new_row["score"] = score
        new_row["reasons"] = "; ".join(reasons[:6])
        new_row["scoreBreakdown"] = breakdown
        scored_rows.append(new_row)

    if not scored_rows:
        return {
            "member": payload.get("member", {}),
            "departmentSpec": department_to_dict(spec, int(spec.name)),
            "requestSummary": make_request_summary(spec, budget, priorities, os_choice, can_install_windows),
            "recommendations": [],
            "warning": "조건에 맞는 노트북 후보가 없습니다. OS 조건 또는 예산을 넓혀주세요.",
        }

    result_df = pd.DataFrame(scored_rows)
    result_df = result_df.sort_values(by=["score", "expected_price_min_krw"], ascending=[False, True]).head(limit)
    recommendations = [laptop_to_dict(row, rank=i + 1) for i, (_, row) in enumerate(result_df.iterrows())]

    return {
        "member": payload.get("member", {}),
        "departmentSpec": department_to_dict(spec, int(spec.name)),
        "requestSummary": make_request_summary(spec, budget, priorities, os_choice, can_install_windows),
        "recommendations": recommendations,
        "notice": [
            "예상 구매가 범위는 실시간 최저가가 아닌 조사 기반 참고 범위입니다.",
            "구매 전 RAM, SSD, GPU, OS 옵션이 추천 결과와 같은지 확인해야 합니다.",
            "검색 링크는 모델 탐색용이며 쇼핑몰 재고와 옵션에 따라 다른 제품이 섞일 수 있습니다.",
        ],
    }


def make_request_summary(spec: pd.Series, budget: int, priorities: list[str], os_choice: str, can_install_windows: bool) -> dict[str, Any]:
    priority_labels = {"price": "가격", "performance": "성능", "weight": "휴대성"}
    return {
        "department": spec["department"],
        "mainUsage": spec["main_usage"],
        "budgetKrw": budget,
        "budgetLabel": money(budget),
        "priorities": [priority_labels.get(p, p) for p in priorities],
        "os": OS_LABELS.get(os_choice, os_choice),
        "canInstallWindows": can_install_windows,
        "recommendedCpu": spec["recommended_cpu"],
        "recommendedGpu": spec["recommended_gpu"],
        "minRamGb": int(spec["min_ram_gb"]),
        "minStorageLabel": storage_label(spec["min_storage_gb"]),
        "avgBudgetLabel": money(spec["avg_budget_krw"]),
        "valueBudgetLabel": money(spec["value_budget_krw"]),
        "performanceCapLabel": money(int(spec["avg_budget_krw"] * spec["performance_multiplier"])),
        "note": spec["note"],
    }
