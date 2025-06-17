import { Client, Account, Databases, Storage } from 'appwrite';

const client = new Client()
    .setEndpoint('https://cloud.appwrite.io/v1') // 设置你的Appwrite API端点
    .setProject('67ac15990027bfb157f9') // 设置你的项目ID
export const account = new Account(client);
export const databases = new Databases(client);
export const storage = new Storage(client);

export const appwriteConfig = {
    databaseId: '67d3a4480018e2e09b68',
    usersCollectionId: 'users',
    eventsCollectionId: 'events',
    interactionsCollectionId: 'interactions',
    favoritesCollectionId: 'favorites',
    foldersCollectionId: 'folders',
};
export const DEFAULT_LOCATION = {
    coordinates: {
		lat: 31.2304,
		lng: 121.4737
	},
	address: '北京市海淀区',
    city: '北京市',
    district: '海淀区'
};