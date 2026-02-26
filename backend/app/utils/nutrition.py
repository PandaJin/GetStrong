"""营养和健康相关计算工具"""

from datetime import date


def calculate_age(birthday: date) -> int:
    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """计算 BMI"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: int) -> float:
    """计算基础代谢率 (BMR) - Mifflin-St Jeor 公式

    Args:
        gender: 1=male, 2=female
    """
    if gender == 1:  # male
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  # female
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """计算每日总热量消耗 (TDEE)"""
    multipliers = {
        "sedentary": 1.2,       # 久坐不动
        "light": 1.375,         # 轻度活动（每周1-3天运动）
        "moderate": 1.55,       # 中度活动（每周3-5天运动）
        "active": 1.725,        # 高度活动（每周6-7天运动）
        "very_active": 1.9,     # 极高活动量（体力劳动或每日高强度训练）
    }
    return bmr * multipliers.get(activity_level, 1.55)


def calculate_daily_target(
    tdee: float, goal: str
) -> dict:
    """根据目标计算每日热量和宏量素目标

    Returns:
        dict with keys: calories, protein_g, fat_g, carbs_g, deficit
    """
    if goal == "lose_weight":
        deficit = 500  # 每日缺口500千卡
        calories = tdee - deficit
    elif goal == "gain_muscle":
        deficit = -300  # 每日盈余300千卡
        calories = tdee + 300
    else:  # maintain / improve_health
        deficit = 0
        calories = tdee

    # 宏量素分配（蛋白质30%，脂肪25%，碳水45%）
    protein_g = round(calories * 0.30 / 4, 1)  # 1g蛋白质=4千卡
    fat_g = round(calories * 0.25 / 9, 1)       # 1g脂肪=9千卡
    carbs_g = round(calories * 0.45 / 4, 1)     # 1g碳水=4千卡

    return {
        "calories": round(calories),
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g,
        "deficit": deficit,
    }
