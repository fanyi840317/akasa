import type { UserSettings } from '$lib/types/settings';
import { mockUsers } from './mock-users';

export const mockSettings: UserSettings[] = [
  {
    id: 'settings1',
    userId: mockUsers[0].id,
    interface: {
      theme: 'system',
      language: 'zh',
      fontSize: 'medium',
      compactMode: false
    },
    notification: {
      email: true,
      push: true,
      newInvestigation: true,
      newEvidence: true,
      newComment: true,
      mentionedMe: true,
      teamUpdates: true,
      dailyDigest: false
    },
    privacy: {
      profileVisibility: 'public',
      showEmail: false,
      showLocation: true,
      showActivity: true,
      allowMessaging: true
    },
    personalization: {
      defaultView: 'grid',
      defaultCategory: 'supernatural',
      defaultSort: 'latest',
      favoriteCategories: ['supernatural', 'unexplained', 'phenomena'],
      hiddenCategories: []
    },
    updatedAt: new Date('2024-04-25T10:00:00')
  },
  {
    id: 'settings2',
    userId: mockUsers[1].id,
    interface: {
      theme: 'dark',
      language: 'zh',
      fontSize: 'small',
      compactMode: true
    },
    notification: {
      email: true,
      push: false,
      newInvestigation: true,
      newEvidence: true,
      newComment: false,
      mentionedMe: true,
      teamUpdates: true,
      dailyDigest: true
    },
    privacy: {
      profileVisibility: 'team',
      showEmail: false,
      showLocation: false,
      showActivity: true,
      allowMessaging: false
    },
    personalization: {
      defaultView: 'list',
      defaultCategory: 'paranormal',
      defaultSort: 'popular',
      favoriteCategories: ['paranormal', 'mysterious'],
      hiddenCategories: ['urban']
    },
    updatedAt: new Date('2024-04-24T15:30:00')
  }
];