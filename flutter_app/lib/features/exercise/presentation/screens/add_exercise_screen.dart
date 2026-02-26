import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AddExerciseScreen extends StatefulWidget {
  const AddExerciseScreen({super.key});

  @override
  State<AddExerciseScreen> createState() => _AddExerciseScreenState();
}

class _AddExerciseScreenState extends State<AddExerciseScreen> {
  final _nameController = TextEditingController();
  final _durationController = TextEditingController();
  final _caloriesController = TextEditingController();
  String _selectedType = 'running';
  String _intensity = 'medium';

  final _exerciseTypes = {
    'running': ('跑步', Icons.directions_run),
    'swimming': ('游泳', Icons.pool),
    'weight_training': ('力量训练', Icons.fitness_center),
    'yoga': ('瑜伽', Icons.self_improvement),
    'cycling': ('骑行', Icons.directions_bike),
    'other': ('其他', Icons.sports),
  };

  @override
  void dispose() {
    _nameController.dispose();
    _durationController.dispose();
    _caloriesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('添加运动记录'),
        actions: [
          TextButton(onPressed: _save, child: const Text('保存')),
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
                onTap: () => context.push('/recognize?type=exercise'),
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
                            Text('AI 截图识别', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                            Text('上传运动截图，AI 自动识别运动信息', style: TextStyle(fontSize: 13)),
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

            // Exercise type selector
            const Text('运动类型', style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _exerciseTypes.entries.map((entry) {
                final isSelected = _selectedType == entry.key;
                final (label, icon) = entry.value;
                return ChoiceChip(
                  avatar: Icon(icon, size: 18),
                  label: Text(label),
                  selected: isSelected,
                  onSelected: (_) => setState(() => _selectedType = entry.key),
                );
              }).toList(),
            ),
            const SizedBox(height: 20),

            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: '运动名称（选填）',
                hintText: '例如：5公里慢跑',
                prefixIcon: Icon(Icons.sports),
              ),
            ),
            const SizedBox(height: 16),

            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _durationController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: '时长（分钟）',
                      prefixIcon: Icon(Icons.timer),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: _caloriesController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: '消耗热量',
                      prefixIcon: Icon(Icons.local_fire_department),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Intensity selector
            const Text('运动强度', style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'low', label: Text('低'), icon: Icon(Icons.sentiment_satisfied)),
                ButtonSegment(value: 'medium', label: Text('中'), icon: Icon(Icons.sentiment_neutral)),
                ButtonSegment(value: 'high', label: Text('高'), icon: Icon(Icons.sentiment_very_dissatisfied)),
              ],
              selected: {_intensity},
              onSelectionChanged: (set) => setState(() => _intensity = set.first),
            ),
          ],
        ),
      ),
    );
  }

  void _save() {
    // TODO: Validate and save via API
    context.pop();
  }
}
