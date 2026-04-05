import asyncio
import requests
from mcp import Tool
from mcp.server import Server
import mcp.types as types
from mcp.server.stdio import stdio_server
from typing import List
from mcp.types import CallToolResult, TextContent


server = Server("weather-travel-assistant")


async def get_weather(location: str) -> str:
    """查询指定地点的天气信息"""
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


async def generate_travel_plan(destination: str, weather_info: str) -> str:
    """基于天气信息生成出行计划建议"""
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


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="get_weather",
            description="查询指定地点的天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "地点名称，如北京、上海等"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="generate_travel_plan",
            description="基于天气信息生成出行计划建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "目的地名称"
                    },
                    "weather_info": {
                        "type": "string",
                        "description": "天气信息字符串"
                    }
                },
                "required": ["destination", "weather_info"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """调用工具"""
    if name == "get_weather":
        location = arguments.get("location", "")
        result = await get_weather(location)
        return CallToolResult(content=[TextContent(type="text", text=result)])
    elif name == "generate_travel_plan":
        destination = arguments.get("destination", "")
        weather_info = arguments.get("weather_info", "")
        result = await generate_travel_plan(destination, weather_info)
        return CallToolResult(content=[TextContent(type="text", text=result)])
    else:
        error_msg = f"未知工具: {name}"
        return CallToolResult(content=[TextContent(type="text", text=error_msg)])


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
