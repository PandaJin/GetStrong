import 'dart:io';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';

class CameraRecognitionScreen extends StatefulWidget {
  final String type; // 'food' or 'exercise'
  const CameraRecognitionScreen({super.key, required this.type});

  @override
  State<CameraRecognitionScreen> createState() => _CameraRecognitionScreenState();
}

class _CameraRecognitionScreenState extends State<CameraRecognitionScreen> {
  XFile? _image;
  bool _isAnalyzing = false;
  Map<String, dynamic>? _result;

  final _picker = ImagePicker();

  @override
  void initState() {
    super.initState();
    _pickImage();
  }

  Future<void> _pickImage() async {
    final source = await _showSourceDialog();
    if (source == null) {
      if (mounted) context.pop();
      return;
    }

    final image = await _picker.pickImage(source: source);
    if (image == null) {
      if (mounted) context.pop();
      return;
    }

    setState(() {
      _image = image;
      _isAnalyzing = true;
    });

    // TODO: Upload to OSS and call AI recognition API
    await Future.delayed(const Duration(seconds: 2));

    if (mounted) {
      setState(() {
        _isAnalyzing = false;
        _result = widget.type == 'food'
            ? {
                'foods': [
                  {'name': '识别结果将显示在这里', 'calories': 0, 'protein_g': 0, 'fat_g': 0, 'carbs_g': 0},
                ],
                'total_calories': 0,
              }
            : {
                'exercise_type': '识别中...',
                'exercise_name': '运动识别结果',
                'calories_burned': 0,
              };
      });
    }
  }

  Future<ImageSource?> _showSourceDialog() async {
    return showModalBottomSheet<ImageSource>(
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
              const Text('选择图片来源', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              ListTile(
                leading: const Icon(Icons.camera_alt, color: Colors.green),
                title: const Text('拍照'),
                onTap: () => Navigator.pop(ctx, ImageSource.camera),
              ),
              ListTile(
                leading: const Icon(Icons.photo_library, color: Colors.blue),
                title: const Text('从相册选择'),
                onTap: () => Navigator.pop(ctx, ImageSource.gallery),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isFood = widget.type == 'food';

    return Scaffold(
      appBar: AppBar(
        title: Text(isFood ? 'AI 食物识别' : 'AI 运动识别'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Image preview
            if (_image != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.file(
                  File(_image!.path),
                  height: 250,
                  width: double.infinity,
                  fit: BoxFit.cover,
                ),
              ),
            const SizedBox(height: 16),

            // Analyzing indicator
            if (_isAnalyzing)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      const CircularProgressIndicator(),
                      const SizedBox(height: 16),
                      Text(
                        isFood ? 'AI 正在识别食物...' : 'AI 正在识别运动...',
                        style: const TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ),
              ),

            // Result card
            if (_result != null && !_isAnalyzing) ...[
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.check_circle,
                            color: Theme.of(context).colorScheme.primary,
                          ),
                          const SizedBox(width: 8),
                          const Text('识别结果', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      const Text(
                        '连接 AI 服务后，识别结果将在这里展示。\n包括食物名称、热量、营养素等详细信息。',
                        style: TextStyle(color: Colors.grey),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _pickImage,
                      child: const Text('重新拍照'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () {
                        // TODO: Save recognition result as record
                        context.pop();
                      },
                      child: const Text('保存记录'),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
