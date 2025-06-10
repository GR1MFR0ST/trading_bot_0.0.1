import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Trading Bot Mobile",
      home: Scaffold(
        appBar: AppBar(title: Text("Trading Bot")),
        body: Center(child: Text("Mobile app under development")),
      ),
    );
  }
}