import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('我的')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Profile header card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 32,
                    backgroundColor: Theme.of(context).colorScheme.primaryContainer,
                    child: const Icon(Icons.person, size: 36),
                  ),
                  const SizedBox(width: 16),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('用户', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('点击编辑个人资料', style: TextStyle(color: Colors.grey)),
                      ],
                    ),
                  ),
                  const Icon(Icons.chevron_right),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Body info card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('身体数据', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildBodyStat('身高', '--cm'),
                      _buildBodyStat('体重', '--kg'),
                      _buildBodyStat('BMI', '--'),
                      _buildBodyStat('目标', '--kg'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Settings items
          _buildSettingItem(Icons.track_changes, '健身目标', '未设置', () {}),
          _buildSettingItem(Icons.smart_toy_outlined, 'AI 服务', 'Kimi', () {}),
          _buildSettingItem(Icons.dark_mode_outlined, '深色模式', '跟随系统', () {}),
          _buildSettingItem(Icons.info_outline, '关于', 'v1.0.0', () {}),
          _buildSettingItem(Icons.logout, '退出登录', '', () {}, isDestructive: true),
        ],
      ),
    );
  }

  Widget _buildBodyStat(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
      ],
    );
  }

  Widget _buildSettingItem(
    IconData icon,
    String title,
    String value,
    VoidCallback onTap, {
    bool isDestructive = false,
  }) {
    return Card(
      child: ListTile(
        leading: Icon(icon, color: isDestructive ? Colors.red : null),
        title: Text(
          title,
          style: TextStyle(color: isDestructive ? Colors.red : null),
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (value.isNotEmpty) Text(value, style: const TextStyle(color: Colors.grey)),
            const SizedBox(width: 4),
            if (!isDestructive) const Icon(Icons.chevron_right, color: Colors.grey),
          ],
        ),
        onTap: onTap,
      ),
    );
  }
}
