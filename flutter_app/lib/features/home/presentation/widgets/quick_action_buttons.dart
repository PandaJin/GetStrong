import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class QuickActionButtons extends StatelessWidget {
  final DateTime date;
  const QuickActionButtons({super.key, required this.date});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Camera recognition FAB
        FloatingActionButton.extended(
          heroTag: 'camera',
          onPressed: () => _showAddOptions(context),
          icon: const Icon(Icons.add_rounded),
          label: const Text('记录'),
        ),
      ],
    );
  }

  void _showAddOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                '添加记录',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildOption(
                    ctx,
                    icon: Icons.camera_alt_rounded,
                    label: '拍照识别',
                    color: Colors.green,
                    onTap: () {
                      Navigator.pop(ctx);
                      context.push('/recognize?type=food');
                    },
                  ),
                  _buildOption(
                    ctx,
                    icon: Icons.restaurant_rounded,
                    label: '饮食记录',
                    color: Colors.orange,
                    onTap: () {
                      Navigator.pop(ctx);
                      context.push('/diet/add');
                    },
                  ),
                  _buildOption(
                    ctx,
                    icon: Icons.fitness_center_rounded,
                    label: '运动记录',
                    color: Colors.blue,
                    onTap: () {
                      Navigator.pop(ctx);
                      context.push('/exercise/add');
                    },
                  ),
                  _buildOption(
                    ctx,
                    icon: Icons.bedtime_rounded,
                    label: '睡眠记录',
                    color: Colors.indigo,
                    onTap: () {
                      Navigator.pop(ctx);
                      // TODO: Navigate to sleep add
                    },
                  ),
                ],
              ),
              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildOption(
    BuildContext context, {
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 56,
            height: 56,
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Icon(icon, color: color, size: 28),
          ),
          const SizedBox(height: 8),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }
}
