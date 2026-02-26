class ApiConstants {
  ApiConstants._();

  static const String baseUrl = 'http://localhost:8000';
  static const String apiPrefix = '/api/v1';

  // Auth
  static const String register = '$apiPrefix/auth/register';
  static const String login = '$apiPrefix/auth/login';
  static const String refreshToken = '$apiPrefix/auth/refresh';

  // Users
  static const String userProfile = '$apiPrefix/users/me';

  // Diet
  static const String dietRecords = '$apiPrefix/diet/records';
  static const String dietDailySummary = '$apiPrefix/diet/daily-summary';

  // Exercise
  static const String exerciseRecords = '$apiPrefix/exercise/records';

  // Sleep
  static const String sleepRecords = '$apiPrefix/sleep/records';

  // Body Metrics
  static const String bodyMetrics = '$apiPrefix/body/metrics';
  static const String bodyMetricsLatest = '$apiPrefix/body/metrics/latest';

  // AI
  static const String recognizeFood = '$apiPrefix/ai/recognize/food';
  static const String recognizeExercise = '$apiPrefix/ai/recognize/exercise';
  static const String chatSessions = '$apiPrefix/ai/chat/sessions';

  // Health Plans
  static const String plans = '$apiPrefix/plans';
  static const String generatePlan = '$apiPrefix/plans/generate';
  static const String activePlan = '$apiPrefix/plans/active';

  // Stats
  static const String dailyStats = '$apiPrefix/stats/daily';
  static const String weightTrend = '$apiPrefix/stats/weight-trend';
  static const String calorieTrend = '$apiPrefix/stats/calorie-trend';
}
