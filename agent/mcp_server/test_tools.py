#!/usr/bin/env python3
"""
测试天气出行助手工具的简单脚本
"""

import requests
import sys


def get_weather_sync(location: str) -> str:
    """同步版本的天气查询"""
    try:
        # 使用 wttr.in API (免费，无需API key)，添加中文语言参数
        url = f"https://wttr.in/{location}?format=j1&lang=zh"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 解析当前天气
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        # 使用中文天气描述
        weather_desc = current.get('lang_zh', [{}])[0].get('value', current['weatherDesc'][0]['value'])
        humidity = current['humidity']
        wind_speed = current['windspeedKmph']

        return f"地点: {location}\n温度: {temp_c}°C\n天气: {weather_desc}\n湿度: {humidity}%\n风速: {wind_speed} km/h"

    except Exception as e:
        return f"获取天气信息失败: {str(e)}"


def generate_travel_plan_sync(destination: str, weather_info: str) -> str:
    """同步版本的出行计划生成"""
    # 简单的基于天气的出行建议逻辑
    plan = f"出行目的地: {destination}\n\n天气情况: {weather_info}\n\n"

    # 解析天气信息来生成建议
    weather_lower = weather_info.lower()
    if any(word in weather_lower for word in ["雨", "雪", "rain", "snow", "shower", "drizzle"]):
        plan += "建议:\n- 带上雨伞或雨衣\n- 穿着防水鞋子\n- 考虑室内活动优先\n- 检查交通状况\n"
    elif any(word in weather_lower for word in ["晴", "clear", "sunny", "fair"]):
        plan += "建议:\n- 适合户外活动\n- 带上防晒霜和帽子\n- 多喝水保持水分\n- 可以安排长时间户外行程\n"
    elif any(word in weather_lower for word in ["云", "cloud", "overcast", "partly"]):
        plan += "建议:\n- 天气温和，适合各种活动\n- 带上轻便外套以防变化\n- 可以安排室内外结合的行程\n"
    elif any(word in weather_lower for word in ["雾", "fog", "mist", "haze"]):
        plan += "建议:\n- 注意能见度，谨慎驾驶\n- 带上口罩防护\n- 减少户外活动\n- 关注交通信息\n"
    else:
        plan += "建议:\n- 根据具体天气情况调整计划\n- 关注天气变化\n"

    # 添加通用建议
    plan += "\n通用出行提示:\n- 检查当地交通工具\n- 准备必要的证件和文件\n- 关注目的地最新信息\n- 保持通讯畅通"

    return plan


def main():
    print("=== 天气出行智能助手测试 ===\n")

    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # 自动测试模式
        print("1. 测试天气查询 (新疆):")
        weather = get_weather_sync("Xinjiang")
        print(weather)
        print()

        # 测试出行计划生成
        print("2. 测试出行计划生成:")
        plan = generate_travel_plan_sync("新疆", weather)
        print(plan)
        print()

        print("=== 测试完成 ===")
    else:
        # 交互模式
        print("🌤️ 欢迎使用天气出行智能助手！")
        print("今天想查询哪个城市的天气？")

        while True:
            try:
                city = input("\n请输入城市名称 (输入 'quit' 退出): ").strip()

                if city.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break

                if not city:
                    print("❌ 城市名称不能为空，请重新输入")
                    continue

                print(f"\n🔍 正在查询 {city} 的天气...")
                weather = get_weather_sync(city)
                print("✅ 查询成功！")
                print(weather)

                # 询问是否需要出行计划
                plan_choice = input(f"\n🤔 需要为 {city} 生成出行计划吗？(y/n): ").strip().lower()
                if plan_choice in ['y', 'yes', '是']:
                    print("\n📝 正在生成出行计划...")
                    plan = generate_travel_plan_sync(city, weather)
                    print("✅ 出行计划生成完成！")
                    print(plan)

                print("\n" + "="*50)

            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 查询失败: {e}")
                print("请检查网络连接或城市名称是否正确\n")


if __name__ == "__main__":
    main()