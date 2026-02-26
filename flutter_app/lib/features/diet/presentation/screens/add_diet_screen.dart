import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/theme/app_theme.dart';

class AddDietScreen extends StatefulWidget {
  const AddDietScreen({super.key});

  @override
  State<AddDietScreen> createState() => _AddDietScreenState();
}

class _AddDietScreenState extends State<AddDietScreen> {
  String _selectedMealType = 'lunch';
  final _foodNameController = TextEditingController();
  final _caloriesController = TextEditingController();
  final _proteinController = TextEditingController();
  final _fatController = TextEditingController();
  final _carbsController = TextEditingController();

  final _mealTypes = {
    'breakfast': ('早餐', '🌅', AppTheme.breakfastColor),
    'lunch': ('午餐', '☀️', AppTheme.lunchColor),
    'dinner': ('晚餐', '🌙', AppTheme.dinnerColor),
    'snack': ('加餐', '🍪', AppTheme.snackColor),
  };

  @override
  void dispose() {
    _foodNameController.dispose();
    _caloriesController.dispose();
    _proteinController.dispose();
    _fatController.dispose();
    _carbsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('添加饮食记录'),
        actions: [
          TextButton(
            onPressed: _save,
            child: const Text('保存'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // AI recognition shortcut
            Card(
              color: Theme.of(context).colorScheme.primaryContainer,
              child: InkWell(
                onTap: () => context.push('/recognize?type=food'),
                borderRadius: BorderRadius.circular(16),
                child: const Padding(
                  padding: EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Icon(Icons.camera_alt_rounded, size: 32),
                      SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('AI 拍照识别', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                            Text('拍一张食物照片，AI 自动识别热量', style: TextStyle(fontSize: 13)),
                          ],
                        ),
                      ),
                      Icon(Icons.arrow_forward_ios, size: 16),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Meal type selector
            const Text('餐次', style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Row(
              children: _mealTypes.entries.map((entry) {
                final isSelected = _selectedMealType == entry.key;
                final (label, emoji, color) = entry.value;
                return Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 4),
                    child: ChoiceChip(
                      label: Text('$emoji $label'),
                      selected: isSelected,
                      onSelected: (_) => setState(() => _selectedMealType = entry.key),
                      selectedColor: color.withValues(alpha: 0.2),
                    ),
                  ),
                );
              }).toList(),
            ),
            const SizedBox(height: 20),

            // Food name
            TextField(
              controller: _foodNameController,
              decoration: const InputDecoration(
                labelText: '食物名称',
                hintText: '例如：鸡胸肉沙拉',
                prefixIcon: Icon(Icons.restaurant),
              ),
            ),
            const SizedBox(height: 16),

            // Calories
            TextField(
              controller: _caloriesController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: '热量 (千卡)',
                hintText: '例如：520',
                prefixIcon: Icon(Icons.local_fire_department),
              ),
            ),
            const SizedBox(height: 16),

            // Macro nutrients
            const Text('营养素（选填）', style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _proteinController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(labelText: '蛋白质 (g)', isDense: true),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _fatController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(labelText: '脂肪 (g)', isDense: true),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _carbsController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(labelText: '碳水 (g)', isDense: true),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  void _save() {
    // TODO: Validate and save via API
    if (_foodNameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('请输入食物名称')),
      );
      return;
    }
    // TODO: Call diet service to save
    context.pop();
  }
}
