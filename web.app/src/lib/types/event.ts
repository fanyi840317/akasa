export type EventStatus = 'unverified' | 'confirmed' | 'closed';
export type EventCategory = 'urban' | 'paranormal' | 'supernatural' | 'mysterious' | 'unexplained' | 'phenomena';

export interface Evidence {
  id: string;
  type: 'image' | 'video' | 'document' | 'testimony';
  url: string;
  description: string;
  submittedBy: string;
  submittedAt: Date;
  verificationStatus: 'pending' | 'verified' | 'rejected';
}

export interface Witness {
  id: string;
  name: string;
  credibilityScore: number;
  testimony: string;
  contactInfo?: string;
  anonymous: boolean;
}

export interface TimelineEvent {
  id: string;
  timestamp: Date;
  description: string;
  evidenceIds: string[];
  witnessIds: string[];
}

export interface RelatedPerson {
  id: string;
  name: string;
  role: string;
  description: string;
  anonymous: boolean;
}

export interface Event {
  id: string;
  title: string;
  description: string;
  category: EventCategory;
  status: EventStatus;
  image: string;
  location: {
    coordinates: [number, number];
    address: string;
    name: string;
  };
  // 时间信息
  occurredAt: Date;
  reportedAt: Date;
  lastUpdatedAt: Date;
  // 参与者信息
  createdBy: string;
  witnesses: Witness[];
  relatedPersons: RelatedPerson[];
  // 可信度评分
  credibilityScore: number;
  evidenceStrength: number;
  witnessCredibility: number;
  // 事件进展
  timeline: TimelineEvent[];
  evidence: Evidence[];
  // 社区互动
  views: number;
  follows: number;
  comments: number;
  // 关联事件
  relatedEventIds: string[];
  tags: string[];
  coverImage: string;
  investigators?: {
    id: string;
    name: string;
    avatar: string;
    role: string;
    joinedAt: Date;
  }[];
}