import type { RequestHandler } from '@sveltejs/kit';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import type { Event } from '$lib/types/event';

// 直接网页抓取并解析新闻数据，无需API Key
// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function fetchFromBaidu(startDate: string, endDate: string): Promise<unknown[]> {
  // 简单抓取百度新闻搜索结果页
  const query = encodeURIComponent('神秘事件|ufo');
  const url = `https://www.baidu.com/s?wd=${query}`;
  try {
    const res = await fetch(url);
    console.log(res);
    if (!res.ok) return [];
    const html = await res.text();
    // 简单正则提取新闻标题和链接（仅作演示，实际可用cheerio等库增强解析）
    const reg = /<h3 class="t">.*?<a.*?href="(.*?)".*?>(.*?)<\/a>/g;
    const events: unknown[] = [];
    let match;
    while ((match = reg.exec(html)) !== null) {
      events.push({
        title: match[2].replace(/<.*?>/g, ''),
        date: '',
        location: '',
        description: '',
        relatedPeople: [],
        timeline: [],
        summary: '',
        source: '百度新闻',
        sourceUrl: match[1]
      });
    }
    return events;
  } catch (e) {
    console.error('Baidu fetch error:', e);
    return [];
  }
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function fetchFromGoogle(startDate: string, endDate: string): Promise<unknown[]> {
  // 简单抓取Google新闻搜索结果页
  const query = encodeURIComponent('神秘事件');
  const url = `https://www.google.com/search?q=${query}&tbm=nws`;
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) return [];
    const html = await res.text();
    // 简单正则提取新闻标题和链接
    const reg = /<a href="(https?:\/\/news.google.com\/.*?)".*?>(.*?)<\/a>/g;
    const events: unknown[] = [];
    let match;
    while ((match = reg.exec(html)) !== null) {
      events.push({
        title: match[2].replace(/<.*?>/g, ''),
        date: '',
        location: '',
        description: '',
        relatedPeople: [],
        timeline: [],
        summary: '',
        source: 'Google News',
        sourceUrl: match[1]
      });
    }
    return events;
  } catch (e) {
    console.error('Google fetch error:', e);
    return [];
  }
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function fetchFromBing(startDate: string, endDate: string): Promise<unknown[]> {
  // 简单抓取Bing新闻搜索结果页
  const query = encodeURIComponent('神秘事件');
  const url = `https://www.bing.com/news/search?q=${query}`;
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) return [];
    const html = await res.text();
    // 简单正则提取新闻标题和链接
    const reg = /<a href="(https?:\/\/.*?)" h="ID=.*?".*?>(.*?)<\/a>/g;
    const events: unknown[] = [];
    let match;
    while ((match = reg.exec(html)) !== null) {
      events.push({
        title: match[2].replace(/<.*?>/g, ''),
        date: '',
        location: '',
        description: '',
        relatedPeople: [],
        timeline: [],
        summary: '',
        source: 'Bing News',
        sourceUrl: match[1]
      });
    }
    return events;
  } catch (e) {
    console.error('Bing fetch error:', e);
    return [];
  }
}

export const GET: RequestHandler = async ({ url }) => {
  const startDate = url.searchParams.get('startDate') || '';
  const endDate = url.searchParams.get('endDate') || '';

  // 并发聚合多站点
  const [baidu, google, bing] = await Promise.all([
    fetchFromBaidu(startDate, endDate),
    fetchFromGoogle(startDate, endDate),
    fetchFromBing(startDate, endDate)
  ]);

  // 合并去重（可根据实际需求优化）
  const events: unknown[] = [...baidu, ...google, ...bing];

  return new Response(JSON.stringify({ events }), {
    headers: { 'Content-Type': 'application/json' }
  });
};