import type { Comment } from '$lib/types/comment';
import { mockUsers } from './mock-users';

export const mockComments: Comment[] = [
  {
    id: '1',
    eventId: '1',
    userId: mockUsers[0].id,
    content: '这个事件太不可思议了，我也是当天晚上在附近，确实看到了奇怪的光！',
    createdAt: new Date('2024-01-15T20:30:00'),
    likes: 24,
    user: {
      name: mockUsers[0].name,
      avatar: mockUsers[0].avatar
    },
    replies: [
      {
        id: '1-1',
        userId: mockUsers[1].id,
        content: '我也看到了，那个光的颜色很特别，不像是普通的照明设备。',
        createdAt: new Date('2024-01-15T21:15:00'),
        likes: 8,
        user: {
          name: mockUsers[1].name,
          avatar: mockUsers[1].avatar
        }
      }
    ]
  },
  {
    id: '2',
    eventId: '1',
    userId: mockUsers[1].id,
    content: '作为一个天文爱好者，我觉得这可能是大气光学现象，但具体原因还需要更多证据。',
    createdAt: new Date('2024-01-16T10:45:00'),
    likes: 15,
    user: {
      name: mockUsers[1].name,
      avatar: mockUsers[1].avatar
    },
    replies: []
  },
  {
    id: '3',
    eventId: '2',
    userId: mockUsers[0].id,
    content: '我家附近经常有类似的声音，一直以为是地下管道的问题。',
    createdAt: new Date('2024-01-14T15:20:00'),
    likes: 12,
    user: {
      name: mockUsers[0].name,
      avatar: mockUsers[0].avatar
    },
    replies: [
      {
        id: '3-1',
        userId: mockUsers[0].id,
        content: '建议联系专业人士进行勘测，排除地质因素。',
        createdAt: new Date('2024-01-14T16:00:00'),
        likes: 6,
        user: {
          name: mockUsers[0].name,
          avatar: mockUsers[0].avatar
        }
      }
    ]
  },
  {
    id: '4',
    eventId: '3',
    userId: mockUsers[1].id,
    content: '这个现象我研究了很久，收集了大量相关资料和证据。',
    createdAt: new Date('2024-01-13T09:15:00'),
    likes: 31,
    user: {
      name: mockUsers[1].name,
      avatar: mockUsers[1].avatar
    },
    replies: [
      {
        id: '4-1',
        userId: mockUsers[0].id,
        content: '能分享一下你的发现吗？很感兴趣！',
        createdAt: new Date('2024-01-13T10:00:00'),
        likes: 9,
        user: {
          name: mockUsers[0].name,
          avatar: mockUsers[0].avatar
        }
      },
      {
        id: '4-2',
        userId: mockUsers[1].id,
        content: '当然可以，我整理一下资料，稍后发出来。',
        createdAt: new Date('2024-01-13T10:30:00'),
        likes: 5,
        user: {
          name: mockUsers[1].name,
          avatar: mockUsers[1].avatar
        }
      }
    ]
  }
];