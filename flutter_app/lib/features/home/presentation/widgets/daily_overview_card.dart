import 'package:flutter/material.dart';

import '../../../../core/theme/app_theme.dart';

class DailyOverviewCard extends StatelessWidget {
  final DateTime date;
  const DailyOverviewCard({super.key, required this.date});

  @override
  Widget build(BuildContext context) {
    // TODO: Get actual data from provider
    const consumed = 1450.0;
    const target = 2100.0;
    const burned = 320.0;
    final progress = consumed / target;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Calorie ring
            Row(
              children: [
                SizedBox(
                  width: 100,
                  height: 100,
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      CircularProgressIndicator(
                        value: progress.clamp(0.0, 1.0),
                        strokeWidth: 10,
                        backgroundColor: Colors.grey.shade200,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          progress > 1.0 ? AppTheme.errorColor : AppTheme.primaryColor,
                        ),
                      ),
                      Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              '${consumed.toInt()}',
                              style: const TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              '/ ${target.toInt()}',
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey.shade600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 24),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '今日概览',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      _buildStatRow('摄入', '${consumed.toInt()} kcal', AppTheme.primaryColor),
                      _buildStatRow('消耗', '${burned.toInt()} kcal', AppTheme.accentColor),
                      _buildStatRow(
                        '差额',
                        '${(consumed - burned).toInt()} kcal',
                        AppTheme.secondaryColor,
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Divider(),
            const SizedBox(height: 12),
            // Macro nutrients bar
            Row(
              children: [
                _buildMacroChip('蛋白质', '65g', AppTheme.proteinColor),
                const SizedBox(width: 12),
                _buildMacroChip('脂肪', '48g', AppTheme.fatColor),
                const SizedBox(width: 12),
                _buildMacroChip('碳水', '180g', AppTheme.carbsColor),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatRow(String label, String value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
          ),
          const SizedBox(width: 8),
          Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
          const Spacer(),
          Text(value, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildMacroChip(String label, String value, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          children: [
            Text(value, style: TextStyle(fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 2),
            Text(label, style: TextStyle(fontSize: 11, color: color.withValues(alpha: 0.8))),
          ],
        ),
      ),
    );
  }
}
