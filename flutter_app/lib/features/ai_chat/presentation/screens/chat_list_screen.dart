import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class ChatListScreen extends StatelessWidget {
  const ChatListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI 健康助手'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // New chat button
          Card(
            child: ListTile(
              leading: Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primaryContainer,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(
                  Icons.add_comment_rounded,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              title: const Text('新建对话', style: TextStyle(fontWeight: FontWeight.w600)),
              subtitle: const Text('与 AI 健康助手开始新的对话'),
              trailing: const Icon(Icons.arrow_forward_ios, size: 16),
              onTap: () {
                // TODO: Create new session and navigate
                context.push('/chat/new');
              },
            ),
          ),
          const SizedBox(height: 16),
          const Text(
            '历史对话',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 8),
          // TODO: Replace with actual session list from provider
          _buildSessionItem(
            context,
            title: '今天的饮食分析',
            lastMessage: '根据你今天的记录，蛋白质摄入略低...',
            time: '10:30',
          ),
          _buildSessionItem(
            context,
            title: '健身计划咨询',
            lastMessage: '建议你每周进行3次力量训练...',
            time: '昨天',
          ),
        ],
      ),
    );
  }

  Widget _buildSessionItem(
    BuildContext context, {
    required String title,
    required String lastMessage,
    required String time,
  }) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: Theme.of(context).colorScheme.secondaryContainer,
          child: const Icon(Icons.smart_toy_outlined),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w500)),
        subtitle: Text(
          lastMessage,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        trailing: Text(time, style: TextStyle(fontSize: 12, color: Colors.grey.shade500)),
        onTap: () {
          // TODO: Navigate with actual session ID
          context.push('/chat/session-id');
        },
      ),
    );
  }
}
