const sdk = require('node-appwrite');

const client = new sdk.Client();
const databases = new sdk.Databases(client);

client
    .setEndpoint('https://cloud.appwrite.io/v1') // Appwrite Cloud API 端点
    .setProject('67ac15990027bfb157f9')
    .setKey("") // 替换为你的 Appwrite 项目 ID

const DATABASE_ID = '67b344f2000500098ba6'; // 你的数据库 ID

async function setupDatabase() {
    try {
        // 创建集合（cases - 案件）
        await databases.createCollection(DATABASE_ID, "cases", "案件");
        await databases.createJsonAttribute(DATABASE_ID, "cases", "title", true);
        await databases.createJsonAttribute(DATABASE_ID, "cases", "description", false);
        await databases.createStringAttribute(DATABASE_ID, "cases", "category", 100, true);
        await databases.createStringAttribute(DATABASE_ID, "cases", "location", 255, false);
        await databases.createDatetimeAttribute(DATABASE_ID, "cases", "date", true);
        await databases.createStringAttribute(DATABASE_ID, "cases", "status", 50, true, "open");

        console.log("🎉 数据库初始化完成！");
    } catch (error) {
        console.error("❌ 发生错误:", error);
    }
}

// 运行初始化
setupDatabase();
