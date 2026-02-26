import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../widgets/daily_overview_card.dart';
import '../widgets/quick_action_buttons.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  DateTime _selectedDate = DateTime.now();

  void _changeDate(int days) {
    setState(() {
      _selectedDate = _selectedDate.add(Duration(days: days));
    });
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2020),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() => _selectedDate = picked);
    }
  }

  @override
  Widget build(BuildContext context) {
    final dateStr = DateFormat('M月d日 EEEE', 'zh_CN').format(_selectedDate);
    final isToday = DateUtils.isSameDay(_selectedDate, DateTime.now());

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'GetStrong',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          // TODO: Refresh data
        },
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Date selector
              _buildDateSelector(dateStr, isToday),
              const SizedBox(height: 16),

              // Daily overview card
              DailyOverviewCard(date: _selectedDate),
              const SizedBox(height: 16),

              // Diet records section
              _buildSectionHeader('饮食记录', Icons.restaurant_rounded),
              const SizedBox(height: 8),
              _buildDietRecordsList(),
              const SizedBox(height: 16),

              // Exercise records section
              _buildSectionHeader('运动记录', Icons.fitness_center_rounded),
              const SizedBox(height: 8),
              _buildExerciseRecordsList(),
              const SizedBox(height: 16),

              // Sleep record section
              _buildSectionHeader('睡眠记录', Icons.bedtime_rounded),
              const SizedBox(height: 8),
              _buildSleepCard(),
              const SizedBox(height: 80),
            ],
          ),
        ),
      ),
      floatingActionButton: QuickActionButtons(date: _selectedDate),
    );
  }

  Widget _buildDateSelector(String dateStr, bool isToday) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
          icon: const Icon(Icons.chevron_left),
          onPressed: () => _changeDate(-1),
        ),
        GestureDetector(
          onTap: _pickDate,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primaryContainer,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.calendar_today, size: 16),
                const SizedBox(width: 8),
                Text(
                  isToday ? '今天 $dateStr' : dateStr,
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        ),
        IconButton(
          icon: const Icon(Icons.chevron_right),
          onPressed: isToday ? null : () => _changeDate(1),
        ),
      ],
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Theme.of(context).colorScheme.primary),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  Widget _buildDietRecordsList() {
    // TODO: Replace with actual data from provider
    return Column(
      children: [
        _buildMealCard(
          mealType: '早餐',
          mealIcon: '🌅',
          color: const Color(0xFFFFB74D),
          items: [
            _FoodItem('全麦面包 + 鸡蛋', 350, '蛋白质 18g', null),
          ],
        ),
        const SizedBox(height: 8),
        _buildMealCard(
          mealType: '午餐',
          mealIcon: '☀️',
          color: const Color(0xFF66BB6A),
          items: [
            _FoodItem('鸡胸肉沙拉', 520, '蛋白质 35g', null),
          ],
        ),
        const SizedBox(height: 8),
        _buildEmptyMealCard('晚餐', '🌙', const Color(0xFF42A5F5)),
      ],
    );
  }

  Widget _buildMealCard({
    required String mealType,
    required String mealIcon,
    required Color color,
    required List<_FoodItem> items,
  }) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(mealIcon, style: const TextStyle(fontSize: 16)),
                const SizedBox(width: 6),
                Text(
                  mealType,
                  style: TextStyle(
                    fontWeight: FontWeight.w600,
                    color: color,
                  ),
                ),
                const Spacer(),
                // Share / Download buttons
                IconButton(
                  icon: const Icon(Icons.share_outlined, size: 18),
                  onPressed: () {},
                  constraints: const BoxConstraints(),
                  padding: const EdgeInsets.all(4),
                ),
                IconButton(
                  icon: const Icon(Icons.download_outlined, size: 18),
                  onPressed: () {},
                  constraints: const BoxConstraints(),
                  padding: const EdgeInsets.all(4),
                ),
              ],
            ),
            const Divider(height: 16),
            ...items.map((item) => _buildFoodItemRow(item)),
          ],
        ),
      ),
    );
  }

  Widget _buildFoodItemRow(_FoodItem item) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          // Food photo thumbnail
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: Colors.grey.shade200,
              borderRadius: BorderRadius.circular(8),
            ),
            child: item.imageUrl != null
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(item.imageUrl!, fit: BoxFit.cover),
                  )
                : const Icon(Icons.photo_camera, color: Colors.grey),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(item.name, style: const TextStyle(fontWeight: FontWeight.w500)),
                Text(
                  item.nutrients,
                  style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                ),
              ],
            ),
          ),
          Text(
            '${item.calories} kcal',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyMealCard(String mealType, String emoji, Color color) {
    return Card(
      child: InkWell(
        onTap: () => context.push('/diet/add'),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Text(emoji, style: const TextStyle(fontSize: 16)),
              const SizedBox(width: 8),
              Text(mealType, style: TextStyle(color: color, fontWeight: FontWeight.w600)),
              const Spacer(),
              Icon(Icons.add_circle_outline, color: Colors.grey.shade400),
              const SizedBox(width: 4),
              Text('添加记录', style: TextStyle(color: Colors.grey.shade500, fontSize: 13)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildExerciseRecordsList() {
    // TODO: Replace with actual data
    return Card(
      child: InkWell(
        onTap: () => context.push('/exercise/add'),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              const Icon(Icons.directions_run, color: Colors.orange),
              const SizedBox(width: 12),
              const Text('暂无运动记录'),
              const Spacer(),
              Icon(Icons.add_circle_outline, color: Colors.grey.shade400),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSleepCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            const Icon(Icons.bedtime, color: Colors.indigo),
            const SizedBox(width: 12),
            const Text('暂无睡眠记录'),
            const Spacer(),
            Icon(Icons.add_circle_outline, color: Colors.grey.shade400),
          ],
        ),
      ),
    );
  }
}

class _FoodItem {
  final String name;
  final int calories;
  final String nutrients;
  final String? imageUrl;

  _FoodItem(this.name, this.calories, this.nutrients, this.imageUrl);
}
