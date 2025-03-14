const sdk = require('node-appwrite');

const client = new sdk.Client();
const databases = new sdk.Databases(client);

client
    .setEndpoint('https://cloud.appwrite.io/v1') // Appwrite Cloud API 端点
    .setProject('67ac15990027bfb157f9')
    .setKey("standard_122aa6dfe96e880578a6b9857e10dabcddca60f320f38cecd393fdaaedc080f2639432ddab4dcd652c21da0d4b75168f531ab0949a530594d07679df049127ea91f2f22251cd8ca2155aa2847d2c626de7ffbc42f9b0a9b640b534f3daee6eb1f9c3fb46fdb2d84dec6aea8476ef6709b5548e36be9a68ac4f2290925997f96c") // 替换为你的 Appwrite 项目 ID

const DATABASE_ID = '67d3a4480018e2e09b68'; // 你的数据库 ID

async function setupDatabase() {
    try {
        
        // 创建集合（cases - 案件）
        const collectionId = "cases";
        await databases.createCollection(DATABASE_ID, collectionId, "case");
        await databases.createStringAttribute(DATABASE_ID, collectionId, "title", 255, true);
        await databases.createStringAttribute(DATABASE_ID, collectionId, "description", 1000, false);
        await databases.createStringAttribute(DATABASE_ID, collectionId, "content", 36000, false);
        await databases.createStringAttribute(DATABASE_ID, collectionId, "category", 100, true);
        await databases.createStringAttribute(DATABASE_ID, collectionId, "location", 255, false);
        await databases.createDatetimeAttribute(DATABASE_ID, collectionId, "date", true);
        await databases.createStringAttribute(DATABASE_ID, collectionId, "status", 50, false, "open");

        console.log("🎉 数据库初始化完成！");
    } catch (error) {
        console.error("❌ 发生错误:", error);
    }
}

// 运行初始化
setupDatabase();
