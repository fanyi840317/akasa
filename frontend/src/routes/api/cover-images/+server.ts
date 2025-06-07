import { json } from '@sveltejs/kit';

export async function GET() {
  const images = [
    '/images/cover/c1.webp',
    '/images/cover/c2.webp',
    '/images/cover/c3.webp',
  ];
  return json({ images });
}