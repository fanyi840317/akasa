import type { Event } from '../types/event';

// 真实请求后端 API，聚合多搜索网站数据
export async function fetchEventsByRange(startDate: string, endDate: string): Promise<Event[]> {
  const params = new URLSearchParams({ startDate, endDate });
  const resp = await fetch(`/api/events?${params.toString()}`);
  if (!resp.ok) {
    throw new Error('事件查询失败');
  }
  const data = await resp.json();
  // 假设后端返回的数据结构为 { events: Event[] }
  return data.events || [];
}