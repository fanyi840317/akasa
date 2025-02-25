import type { User, Team } from '$lib/types/user';

const AVATAR_BASE_PATH = '/images';
const TEAM_LOGO_BASE_PATH = '/images';

export const mockUsers: User[] = [
  {
    id: 'user123',
    name: '陈天明',
    avatar: `${AVATAR_BASE_PATH}/user1.jpg`,
    email: 'tianming@akasa.org',
    role: 'investigator',
    level: 15,
    experience: 2500,
    joinedAt: new Date('2023-01-15'),
    lastActiveAt: new Date('2024-04-25'),
    reputation: 850,
    badges: ['资深调查员', '现象专家', '优秀贡献者'],
    teamId: 'team1',
    bio: '专注于超自然现象调查，具有5年实地考察经验。',
    followers: 1250,
    investigations: 85,
    investigationSuccessRate: 92,
    skills: ['现场调查', '数据分析', '目击者访谈', '证据收集'],
    certifications: ['高级调查员认证', 'UFO分析专家认证'],
    socialLinks: {
      website: 'https://akasa.org/investigators/tianming',
      twitter: '@tianming_akasa',
      linkedin: 'tianming-chen'
    }
  },
  {
    id: 'user456',
    name: '林雨晴',
    avatar: `${AVATAR_BASE_PATH}/user2.jpg`,
    email: 'yuqing@akasa.org',
    role: 'investigator',
    level: 12,
    experience: 1800,
    joinedAt: new Date('2023-03-20'),
    lastActiveAt: new Date('2024-04-24'),
    reputation: 720,
    badges: ['灵异专家', '优秀记录员'],
    teamId: 'team2',
    bio: '擅长paranormal现象分析和数据收集。'
  }
];

export const mockTeams: Team[] = [
  {
    id: 'team1',
    name: '天眼调查组',
    description: '专注于不明飞行物和空中异象调查的精英团队',
    logo: `${TEAM_LOGO_BASE_PATH}/team1.jpg`,
    level: 20,
    rating: 4.8,
    foundedAt: new Date('2022-12-01'),
    memberIds: ['user123', 'user789'],
    leaderId: 'user123',
    specialties: ['UFO调查', '光学现象分析', '目击者访谈'],
    completedInvestigations: 45,
    status: 'active',
    verificationStatus: 'verified'
  },
  {
    id: 'team2',
    name: '灵异研究协会',
    description: '致力于paranormal现象研究和记录的专业团队',
    logo: `${TEAM_LOGO_BASE_PATH}/team2.jpg`,
    level: 18,
    rating: 4.6,
    foundedAt: new Date('2023-02-15'),
    memberIds: ['user456', 'user101'],
    leaderId: 'user456',
    specialties: ['灵异现象调查', '历史建筑考察', '声学分析'],
    completedInvestigations: 38,
    status: 'active',
    verificationStatus: 'verified'
  }
];