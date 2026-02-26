import 'package:flutter/material.dart';

class AppTheme {
  AppTheme._();

  // Brand colors
  static const Color primaryColor = Color(0xFF4CAF50);     // 健康绿
  static const Color secondaryColor = Color(0xFF2196F3);   // 活力蓝
  static const Color accentColor = Color(0xFFFF9800);      // 能量橙
  static const Color errorColor = Color(0xFFE53935);
  static const Color surfaceColor = Color(0xFFF5F5F5);

  // Meal type colors
  static const Color breakfastColor = Color(0xFFFFB74D);   // 早餐 - 温暖橙
  static const Color lunchColor = Color(0xFF66BB6A);       // 午餐 - 清新绿
  static const Color dinnerColor = Color(0xFF42A5F5);      // 晚餐 - 宁静蓝
  static const Color snackColor = Color(0xFFAB47BC);       // 加餐 - 浪漫紫

  // Macro nutrient colors
  static const Color proteinColor = Color(0xFFEF5350);     // 蛋白质 - 红
  static const Color fatColor = Color(0xFFFFCA28);         // 脂肪 - 黄
  static const Color carbsColor = Color(0xFF26C6DA);       // 碳水 - 青

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorSchemeSeed: primaryColor,
      scaffoldBackgroundColor: surfaceColor,
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
      ),
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        color: Colors.white,
      ),
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.grey.shade100,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
          minimumSize: const Size(double.infinity, 50),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        type: BottomNavigationBarType.fixed,
        selectedItemColor: primaryColor,
        unselectedItemColor: Colors.grey,
        showUnselectedLabels: true,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorSchemeSeed: primaryColor,
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
    );
  }
}
