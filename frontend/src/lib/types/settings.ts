export interface UserSettings {
  id: string;
  userId: string;
  interface: {
    theme: 'light' | 'dark' | 'system';
    language: 'zh' | 'en';
    fontSize: 'small' | 'medium' | 'large';
    compactMode: boolean;
  };
  notification: {
    email: boolean;
    push: boolean;
    newInvestigation: boolean;
    newEvidence: boolean;
    newComment: boolean;
    mentionedMe: boolean;
    teamUpdates: boolean;
    dailyDigest: boolean;
  };
  privacy: {
    profileVisibility: 'public' | 'private' | 'team';
    showEmail: boolean;
    showLocation: boolean;
    showActivity: boolean;
    allowMessaging: boolean;
  };
  personalization: {
    defaultView: 'grid' | 'list';
    defaultCategory: string;
    defaultSort: 'latest' | 'popular' | 'nearby';
    favoriteCategories: string[];
    hiddenCategories: string[];
  };
  updatedAt: Date;
}