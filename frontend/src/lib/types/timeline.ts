// 时间线事件类型
export interface TimelineEvent {
  id: string;
  timestamp: Date;
  description: string;
  evidenceIds: string[];
  witnessIds: string[];
}

// 假说类型
export interface Hypothesis {
  id: string;
  title: string;
  description: string;
  evidence: string[];
  createdAt: Date;
}
