import type { Event } from '$lib/types/event';

const IMAGE_BASE_PATH = '/images';

export const mockEvents: Event[] = [
  {
    id: '1',
    title: '神秘灯光事件',
    description: '多位目击者报告在成都市区上空看到不明飞行物发出的奇异光芒。',
    category: 'supernatural',
    status: 'unverified',
    image: `${IMAGE_BASE_PATH}/31.04_banner-373x373.jpg`,
    coverImage: `${IMAGE_BASE_PATH}/mantis-man.jpg`,
    location: {
      coordinates: [104.0633, 30.6516],
      address: '成都市锦江区中心商圈',
      name: '成都市中心'
    },
    occurredAt: new Date('2024-04-15T20:00:00'),
    reportedAt: new Date('2024-04-15T20:30:00'),
    lastUpdatedAt: new Date('2024-04-15T21:00:00'),
    createdBy: 'user123',
    witnesses: [
      {
        id: 'w1',
        name: '张三',
        credibilityScore: 85,
        testimony: '我在春熙路附近看到一个明亮的光球，它在空中停留了约4分钟，然后突然消失。',
        anonymous: false
      },
      {
        id: 'w2',
        name: '匿名目击者',
        credibilityScore: 75,
        testimony: '光球呈现出不规则的运动轨迹，并伴随着微弱的嗡嗡声。',
        anonymous: true
      }
    ],
    relatedPersons: [],
    credibilityScore: 70,
    evidenceStrength: 60,
    witnessCredibility: 75,
    timeline: [
      {
        id: 't1',
        timestamp: new Date('2024-04-15T20:00:00'),
        description: '首次目击到不明光球',
        evidenceIds: ['e1'],
        witnessIds: ['w1']
      },
      {
        id: 't2',
        timestamp: new Date('2024-04-15T20:02:00'),
        description: '光球开始呈现不规则运动',
        evidenceIds: ['e2'],
        witnessIds: ['w1', 'w2']
      }
    ],
    evidence: [
      {
        id: 'e1',
        type: 'image',
        url: `${IMAGE_BASE_PATH}/evidence/light-orb-1.jpg`,
        description: '光球初次出现时的图片',
        submittedBy: 'w1',
        submittedAt: new Date('2024-04-15T20:01:00'),
        verificationStatus: 'verified'
      },
      {
        id: 'e2',
        type: 'video',
        url: `${IMAGE_BASE_PATH}/evidence/light-orb-movement.mp4`,
        description: '光球不规则运动的视频记录',
        submittedBy: 'w2',
        submittedAt: new Date('2024-04-15T20:03:00'),
        verificationStatus: 'verified'
      }
    ],
    views: 800,
    follows: 25,
    comments: 12,
    relatedEventIds: [],
    tags: ['UFO', '灯光', '夜空'],
    investigators: [
      {
        id: 'user123',
        name: '陈天明',
        avatar: `${IMAGE_BASE_PATH}/user1.jpg`,
        role: '首席调查员',
        joinedAt: new Date('2024-04-15T21:00:00')
      },
      {
        id: 'user456',
        name: '林雨晴',
        avatar: `${IMAGE_BASE_PATH}/user2.jpg`,
        role: '数据分析员',
        joinedAt: new Date('2024-04-15T21:30:00')
      }
    ]
  },
  {
    id: '2',
    title: '古寺异响调查',
    description: '文殊院内多次传出神秘钟声，但寺内钟铃未曾敲响。',
    category: 'paranormal',
    status: 'unverified',
    location: {
      coordinates: [104.1444, 30.7348],
      address: '成都市青羊区文殊院街33号',
      name: '文殊院'
    },
    occurredAt: new Date('2024-04-20T03:15:00'),
    reportedAt: new Date('2024-04-20T06:00:00'),
    lastUpdatedAt: new Date('2024-04-20T10:00:00'),
    createdBy: 'user456',
    witnesses: [],
    relatedPersons: [],
    credibilityScore: 85,
    evidenceStrength: 70,
    witnessCredibility: 80,
    timeline: [],
    evidence: [],
    views: 650,
    follows: 35,
    comments: 18,
    relatedEventIds: [],
    tags: ['古寺', '钟声', '灵异'],
    image: `${IMAGE_BASE_PATH}/31.04_banner-373x373.jpg`,
    coverImage: `${IMAGE_BASE_PATH}/mantis-man.jpg`
  },
  {
    id: '3',
    title: '都江堰水文异象',
    description: '都江堰水系出现反常水流现象，专家无法解释。',
    category: 'unexplained',
    status: 'unverified',
    location: {
      coordinates: [103.6192, 30.9984],
      address: '四川省成都市都江堰市都江堰景区',
      name: '都江堰'
    },
    occurredAt: new Date('2024-05-01T14:00:00'),
    reportedAt: new Date('2024-05-01T14:30:00'),
    lastUpdatedAt: new Date('2024-05-01T16:00:00'),
    createdBy: 'user789',
    witnesses: [],
    relatedPersons: [],
    credibilityScore: 90,
    evidenceStrength: 85,
    witnessCredibility: 90,
    timeline: [],
    evidence: [],
    views: 450,
    follows: 28,
    comments: 15,
    relatedEventIds: [],
    tags: ['水文', '自然现象', '未解之谜'],
    image: `${IMAGE_BASE_PATH}/33.05_banner-373x373.jpg`,
    coverImage: `${IMAGE_BASE_PATH}/mantis-man.jpg`,
  },
  {
    id: '4',
    title: '神秘光球目击事件',
    description: '多名目击者报告在夜空中看到不明光球',
    category: 'unexplained',
    status: 'unverified',
    location: {
      coordinates: [104.0714, 30.6587],
      address: '四川省成都市锦江区春熙路',
      name: '春熙路商圈'
    },
    occurredAt: new Date('2024-01-15T20:30:00'),
    reportedAt: new Date('2024-01-15T21:00:00'),
    lastUpdatedAt: new Date('2024-01-16T10:00:00'),
    createdBy: 'user123',
    witnesses: [
      {
        id: 'w1',
        name: '张先生',
        credibilityScore: 85,
        testimony: '我在春熙路逛街时，突然看到天空中出现一个橙色的光球，大约持续了3分钟，然后突然消失了。光球没有发出声音，但光芒非常明亮。',
        anonymous: false
      },
      {
        id: 'w2',
        name: '',
        credibilityScore: 75,
        testimony: '当时我正在太古里附近等人，看到天空中有个发光体在缓慢移动，形状像个球体，发出脉冲般的光芒。我用手机拍了视频，但因为天太黑，画面不是很清晰。',
        anonymous: true
      },
      {
        id: 'w3',
        name: '李女士',
        credibilityScore: 90,
        testimony: '我和家人在IFS顶楼用餐，透过玻璃看到外面天空中有个奇怪的光球，起初以为是无人机，但它的运动轨迹很不寻常，而且光芒比普通无人机要强烈得多。',
        anonymous: false
      }
    ],
    relatedPersons: [],
    credibilityScore: 75,
    evidenceStrength: 65,
    witnessCredibility: 80,
    timeline: [
      {
        id: 't1',
        timestamp: new Date('2024-01-15T20:30:00'),
        description: '第一位目击者在春熙路首次发现不明光球',
        evidenceIds: [],
        witnessIds: ['w1']
      },
      {
        id: 't2',
        timestamp: new Date('2024-01-15T20:31:00'),
        description: '多位目击者在太古里和IFS附近同时观察到光球现象',
        evidenceIds: [],
        witnessIds: ['w2', 'w3']
      },
      {
        id: 't3',
        timestamp: new Date('2024-01-15T20:32:00'),
        description: '光球开始出现脉冲式闪烁',
        evidenceIds: ['e1'],
        witnessIds: ['w2']
      },
      {
        id: 't4',
        timestamp: new Date('2024-01-15T20:33:00'),
        description: '光球缓慢向东北方向移动',
        evidenceIds: ['e2', 'e3'],
        witnessIds: ['w3']
      },
      {
        id: 't5',
        timestamp: new Date('2024-01-15T20:34:00'),
        description: '光球突然加速并消失在夜空中',
        evidenceIds: [],
        witnessIds: ['w1', 'w2', 'w3']
      }
    ],
    evidence: [
      {
        id: 'e1',
        type: 'video',
        url: '/evidence/video1.mp4',
        description: '目击者手机拍摄的光球移动视频',
        submittedBy: 'anonymous',
        submittedAt: new Date('2024-01-15T20:35:00'),
        verificationStatus: 'pending'
      },
      {
        id: 'e2',
        type: 'image',
        url: '/evidence/photo1.jpg',
        description: 'IFS楼顶拍摄的光球清晰照片',
        submittedBy: '李女士',
        submittedAt: new Date('2024-01-15T20:33:00'),
        verificationStatus: 'verified'
      },
      {
        id: 'e3',
        type: 'video',
        url: '/evidence/cctv1.mp4',
        description: '街道监控摄像头捕捉到的光球画面',
        submittedBy: '春熙路商圈监控系统',
        submittedAt: new Date('2024-01-15T20:33:00'),
        verificationStatus: 'verified'
      },
      {
        id: 'e4',
        type: 'testimony',
        url: '/evidence/audio1.mp3',
        description: '目击者现场录制的环境声音',
        submittedBy: '张先生',
        submittedAt: new Date('2024-01-15T20:35:00'),
        verificationStatus: 'pending'
      }
    ],
    views: 1200,
    follows: 45,
    comments: 23,
    relatedEventIds: [],
    tags: ['UFO', '夜空', '光球'],
    image: `${IMAGE_BASE_PATH}/33.04_banner-373x373.jpg`,
    coverImage: `${IMAGE_BASE_PATH}/mantis-man.jpg`
  },
  {
    id: '5',
    title: '古寺异响调查',
    description: '文殊院内多次传出神秘钟声，但寺内钟铃未曾敲响。',
    category: 'paranormal',
    status: 'unverified',
    location: {
      coordinates: [104.0633, 30.6516],
      address: '成都市青羊区文殊院街66号',
      name: '文殊院'
    },
    occurredAt: new Date('2024-01-10T03:15:00'),
    reportedAt: new Date('2024-01-10T06:30:00'),
    lastUpdatedAt: new Date('2024-01-11T14:00:00'),
    createdBy: 'user456',
    witnesses: [],
    relatedPersons: [],
    credibilityScore: 80,
    evidenceStrength: 85,
    witnessCredibility: 85,
    timeline: [],
    evidence: [],
    views: 1200,
    follows: 88,
    comments: 45,
    relatedEventIds: [],
    tags: ['水文', '自然现象', '未解之谜'],
    image: `${IMAGE_BASE_PATH}/33.05_banner-373x373.jpg`,
    coverImage: `${IMAGE_BASE_PATH}/mantis-man.jpg`
  }
];