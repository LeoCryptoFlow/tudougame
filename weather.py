#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单天气查询脚本
使用 wttr.in 免费 API 获取天气信息
"""

import requests
import json

def get_weather(city):
    """获取指定城市的天气信息"""
    url = f"http://wttr.in/{city}?format=j1&lang=zh"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

def get_advice(temp, weather_desc):
    """根据天气情况给出建议"""
    advice = []
    
    # 温度建议
    if temp <= 0:
        advice.append("🥶 天气很冷，注意保暖，穿厚羽绒服！")
    elif temp <= 10:
        advice.append("🧥 天气较冷，建议穿棉衣或厚外套。")
    elif temp <= 20:
        advice.append("👕 天气适中，穿长袖或薄外套即可。")
    elif temp <= 30:
        advice.append("🌤️ 天气温暖，穿短袖短裤很舒适。")
    else:
        advice.append("🥵 天气炎热，注意防暑降温，多喝水！")
    
    # 天气状况建议
    weather_lower = weather_desc.lower()
    if 'rain' in weather_lower or '雨' in weather_desc:
        advice.append("☔ 有雨，记得带伞！")
    elif 'snow' in weather_lower or '雪' in weather_desc:
        advice.append("❄️ 有雪，路滑注意安全！")
    elif 'cloud' in weather_lower or '阴' in weather_desc or '多云' in weather_desc:
        advice.append("☁️ 多云天气，适合外出活动。")
    elif 'clear' in weather_lower or 'sunny' in weather_lower or '晴' in weather_desc:
        advice.append("☀️ 天气晴朗，适合户外活动，注意防晒。")
    elif 'fog' in weather_lower or '雾' in weather_desc:
        advice.append("🌫️ 有雾，能见度低，出行注意安全。")
    elif 'thunder' in weather_lower or '雷' in weather_desc:
        advice.append("⛈️ 有雷雨，尽量待在室内！")
    
    return advice

def display_weather(city, data):
    """显示天气信息"""
    if not data:
        print(f"❌ 无法获取 '{city}' 的天气信息，请检查城市名是否正确。")
        return
    
    try:
        # 获取当前天气
        current = data['current_condition'][0]
        location = data['nearest_area'][0]
        
        # 基本信息
        city_name = location.get('areaName', [{}])[0].get('value', city)
        country = location.get('country', [{}])[0].get('value', '')
        
        temp = int(current['temp_C'])
        feels_like = int(current['FeelsLikeC'])
        humidity = current['humidity']
        weather_desc = current['weatherDesc'][0]['value']
        wind_speed = current['windspeedKmph']
        wind_dir = current['winddir16Point']
        
        # 显示天气信息
        print("\n" + "="*50)
        print(f"📍 城市: {city_name}, {country}")
        print("="*50)
        print(f"🌡️  当前温度: {temp}°C (体感温度: {feels_like}°C)")
        print(f"🌤️  天气状况: {weather_desc}")
        print(f"💧 湿度: {humidity}%")
        print(f"💨 风速: {wind_speed} km/h, 风向: {wind_dir}")
        print("="*50)
        
        # 获取建议
        advices = get_advice(temp, weather_desc)
        print("📝 今日建议:")
        for advice in advices:
            print(f"   {advice}")
        print("="*50 + "\n")
        
    except (KeyError, IndexError) as e:
        print(f"❌ 解析天气数据时出错: {e}")

def main():
    print("\n🌤️  欢迎使用天气查询工具!")
    print("   (输入 'q' 或 'quit' 退出程序)\n")
    
    while True:
        city = input("请输入城市名称: ").strip()
        
        if city.lower() in ['q', 'quit', 'exit']:
            print("\n👋 感谢使用，再见！\n")
            break
        
        if not city:
            print("❌ 请输入有效的城市名称！\n")
            continue
        
        print(f"\n🔍 正在查询 '{city}' 的天气...")
        data = get_weather(city)
        display_weather(city, data)

if __name__ == "__main__":
    main()