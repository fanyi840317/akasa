import { json } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    // 获取静态目录中的封面图片
    const coverDir = path.join(process.cwd(), 'static', 'images', 'cover');
    
    // 检查目录是否存在
    if (!fs.existsSync(coverDir)) {
      console.error('封面图片目录不存在:', coverDir);
      return json({ images: [] });
    }
    
    // 读取目录中的所有文件
    const files = fs.readdirSync(coverDir);
    
    // 过滤出图片文件
    const imageFiles = files.filter(file => {
      const ext = path.extname(file).toLowerCase();
      return ['.jpg', '.jpeg', '.png', '.gif', '.webp'].includes(ext);
    });
    
    // 构建图片 URL
    const images = imageFiles.map(file => `/images/cover/${file}`);
    
    return json({ images });
  } catch (error) {
    console.error('获取封面图片列表失败:', error);
    return json({ images: [] });
  }
} 