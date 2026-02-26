import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../constants/api_constants.dart';

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(
    BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );

  dio.interceptors.add(AuthInterceptor(ref));
  dio.interceptors.add(LogInterceptor(requestBody: true, responseBody: true));

  return dio;
});

class AuthInterceptor extends Interceptor {
  final Ref ref;
  static const _storage = FlutterSecureStorage();

  AuthInterceptor(this.ref);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // Skip auth for login/register
    if (options.path.contains('/auth/login') ||
        options.path.contains('/auth/register')) {
      return handler.next(options);
    }

    final token = await _storage.read(key: 'access_token');
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      // Try to refresh token
      final refreshToken = await _storage.read(key: 'refresh_token');
      if (refreshToken != null) {
        try {
          final dio = Dio(BaseOptions(baseUrl: ApiConstants.baseUrl));
          final response = await dio.post(
            ApiConstants.refreshToken,
            data: {'refresh_token': refreshToken},
          );

          final newAccessToken = response.data['data']['access_token'];
          final newRefreshToken = response.data['data']['refresh_token'];
          await _storage.write(key: 'access_token', value: newAccessToken);
          await _storage.write(key: 'refresh_token', value: newRefreshToken);

          // Retry the original request
          err.requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';
          final retryResponse = await dio.fetch(err.requestOptions);
          return handler.resolve(retryResponse);
        } catch (_) {
          // Refresh failed, clear tokens
          await _storage.deleteAll();
        }
      }
    }
    handler.next(err);
  }
}
