import { Client, Account, Databases } from 'appwrite';

const client = new Client()
    .setEndpoint('https://cloud.appwrite.io/v1') // 设置你的Appwrite API端点
    .setProject('67ac15990027bfb157f9') // 设置你的项目ID
// 66c1b78a0024df3548a8
// 67ac15990027bfb157f9
export const account = new Account(client);
export const databases = new Databases(client);

export const appwriteConfig = {
    databaseId: '67ac15990027bfb157f9',
    usersCollectionId: 'users',
    eventsCollectionId: 'events'
};