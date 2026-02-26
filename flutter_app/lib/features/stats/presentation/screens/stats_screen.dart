import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

import '../../../../core/theme/app_theme.dart';

class StatsScreen extends StatefulWidget {
  const StatsScreen({super.key});

  @override
  State<StatsScreen> createState() => _StatsScreenState();
}

class _StatsScreenState extends State<StatsScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('统计分析'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: '周'),
            Tab(text: '月'),
            Tab(text: '年'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildStatsContent('week'),
          _buildStatsContent('month'),
          _buildStatsContent('year'),
        ],
      ),
    );
  }

  Widget _buildStatsContent(String period) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Calorie trend chart
          _buildChartCard(
            title: '热量摄入趋势',
            child: SizedBox(
              height: 200,
              child: _buildCalorieChart(),
            ),
          ),
          const SizedBox(height: 16),

          // Weight trend chart
          _buildChartCard(
            title: '体重变化',
            child: SizedBox(
              height: 200,
              child: _buildWeightChart(),
            ),
          ),
          const SizedBox(height: 16),

          // Exercise distribution
          _buildChartCard(
            title: '运动类型分布',
            child: SizedBox(
              height: 200,
              child: _buildExercisePieChart(),
            ),
          ),
          const SizedBox(height: 16),

          // Weekly summary cards
          _buildSummaryCards(),
        ],
      ),
    );
  }

  Widget _buildChartCard({required String title, required Widget child}) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            child,
          ],
        ),
      ),
    );
  }

  Widget _buildCalorieChart() {
    // Sample data
    return BarChart(
      BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: 2500,
        barTouchData: BarTouchData(enabled: true),
        titlesData: FlTitlesData(
          leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              getTitlesWidget: (value, meta) {
                const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
                if (value.toInt() < days.length) {
                  return Text(days[value.toInt()], style: const TextStyle(fontSize: 10));
                }
                return const Text('');
              },
            ),
          ),
        ),
        borderData: FlBorderData(show: false),
        barGroups: [
          _makeBarGroup(0, 1800, 300),
          _makeBarGroup(1, 2100, 450),
          _makeBarGroup(2, 1650, 200),
          _makeBarGroup(3, 1900, 380),
          _makeBarGroup(4, 2200, 500),
          _makeBarGroup(5, 1750, 350),
          _makeBarGroup(6, 1450, 320),
        ],
        gridData: const FlGridData(show: false),
      ),
    );
  }

  BarChartGroupData _makeBarGroup(int x, double intake, double burned) {
    return BarChartGroupData(
      x: x,
      barRods: [
        BarChartRodData(
          toY: intake,
          color: AppTheme.primaryColor.withValues(alpha: 0.7),
          width: 12,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(4)),
        ),
        BarChartRodData(
          toY: burned,
          color: AppTheme.accentColor.withValues(alpha: 0.7),
          width: 12,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(4)),
        ),
      ],
    );
  }

  Widget _buildWeightChart() {
    return LineChart(
      LineChartData(
        gridData: FlGridData(
          show: true,
          drawVerticalLine: false,
          getDrawingHorizontalLine: (value) =>
              FlLine(color: Colors.grey.shade200, strokeWidth: 1),
        ),
        titlesData: FlTitlesData(
          leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 40,
              getTitlesWidget: (value, meta) =>
                  Text('${value.toInt()}kg', style: const TextStyle(fontSize: 10)),
            ),
          ),
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          bottomTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        ),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          LineChartBarData(
            spots: const [
              FlSpot(0, 75.5),
              FlSpot(1, 75.2),
              FlSpot(2, 74.8),
              FlSpot(3, 75.0),
              FlSpot(4, 74.5),
              FlSpot(5, 74.2),
              FlSpot(6, 73.8),
            ],
            isCurved: true,
            color: AppTheme.secondaryColor,
            barWidth: 3,
            dotData: const FlDotData(show: true),
            belowBarData: BarAreaData(
              show: true,
              color: AppTheme.secondaryColor.withValues(alpha: 0.1),
            ),
          ),
        ],
        minY: 72,
        maxY: 77,
      ),
    );
  }

  Widget _buildExercisePieChart() {
    return Row(
      children: [
        Expanded(
          child: PieChart(
            PieChartData(
              sectionsSpace: 2,
              centerSpaceRadius: 40,
              sections: [
                PieChartSectionData(
                  value: 40,
                  title: '跑步',
                  color: AppTheme.primaryColor,
                  radius: 50,
                  titleStyle: const TextStyle(fontSize: 11, color: Colors.white),
                ),
                PieChartSectionData(
                  value: 30,
                  title: '力量',
                  color: AppTheme.secondaryColor,
                  radius: 50,
                  titleStyle: const TextStyle(fontSize: 11, color: Colors.white),
                ),
                PieChartSectionData(
                  value: 20,
                  title: '瑜伽',
                  color: AppTheme.accentColor,
                  radius: 50,
                  titleStyle: const TextStyle(fontSize: 11, color: Colors.white),
                ),
                PieChartSectionData(
                  value: 10,
                  title: '其他',
                  color: Colors.grey,
                  radius: 50,
                  titleStyle: const TextStyle(fontSize: 11, color: Colors.white),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSummaryCards() {
    return Row(
      children: [
        Expanded(
          child: _buildMiniCard('平均摄入', '1,850 kcal', Icons.local_fire_department, AppTheme.primaryColor),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: _buildMiniCard('平均消耗', '350 kcal', Icons.fitness_center, AppTheme.accentColor),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: _buildMiniCard('平均睡眠', '7.2 h', Icons.bedtime, Colors.indigo),
        ),
      ],
    );
  }

  Widget _buildMiniCard(String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 8),
            Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
            const SizedBox(height: 4),
            Text(label, style: TextStyle(fontSize: 11, color: Colors.grey.shade600)),
          ],
        ),
      ),
    );
  }
}
