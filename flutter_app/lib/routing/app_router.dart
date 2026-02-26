import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../features/auth/presentation/screens/login_screen.dart';
import '../features/home/presentation/screens/home_screen.dart';
import '../features/ai_chat/presentation/screens/chat_list_screen.dart';
import '../features/ai_chat/presentation/screens/chat_screen.dart';
import '../features/stats/presentation/screens/stats_screen.dart';
import '../features/profile/presentation/screens/profile_screen.dart';
import '../features/diet/presentation/screens/add_diet_screen.dart';
import '../features/exercise/presentation/screens/add_exercise_screen.dart';
import '../features/ai_recognition/presentation/screens/camera_recognition_screen.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: '/home',
    routes: [
      // Login
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),

      // Main shell with bottom navigation
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) => MainShell(child: child),
        routes: [
          GoRoute(
            path: '/home',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: HomeScreen(),
            ),
          ),
          GoRoute(
            path: '/chat',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: ChatListScreen(),
            ),
          ),
          GoRoute(
            path: '/stats',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: StatsScreen(),
            ),
          ),
          GoRoute(
            path: '/profile',
            pageBuilder: (context, state) => const NoTransitionPage(
              child: ProfileScreen(),
            ),
          ),
        ],
      ),

      // Detail routes (outside shell)
      GoRoute(
        path: '/chat/:sessionId',
        builder: (context, state) => ChatScreen(
          sessionId: state.pathParameters['sessionId']!,
        ),
      ),
      GoRoute(
        path: '/diet/add',
        builder: (context, state) => const AddDietScreen(),
      ),
      GoRoute(
        path: '/exercise/add',
        builder: (context, state) => const AddExerciseScreen(),
      ),
      GoRoute(
        path: '/recognize',
        builder: (context, state) => CameraRecognitionScreen(
          type: state.uri.queryParameters['type'] ?? 'food',
        ),
      ),
    ],
  );
});

class MainShell extends StatefulWidget {
  final Widget child;
  const MainShell({super.key, required this.child});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _currentIndex = 0;

  static const _routes = ['/home', '/chat', '/stats', '/profile'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: widget.child,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
          context.go(_routes[index]);
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home_rounded), label: '首页'),
          BottomNavigationBarItem(icon: Icon(Icons.chat_rounded), label: '对话'),
          BottomNavigationBarItem(icon: Icon(Icons.bar_chart_rounded), label: '统计'),
          BottomNavigationBarItem(icon: Icon(Icons.person_rounded), label: '我的'),
        ],
      ),
    );
  }
}
