const { setupCollection } = require('./setup_utils');

async function setupDatabase() {
    const config = {
        collectionId: 'cases',
        collectionName: 'case',
        attributes: [
            { name: "cover", type: "string", size: 255, required: false },
            { name: "title", type: "string", size: 255, required: true },
            { name: "descrp", type: "string", size: 1000, required: true },
            { name: "content", type: "string", size: 36000, required: true },
            { name: "user_id", type: "string", size: 100, required: true },
            { name: "happend_time", type: "datetime", required: true },
            { name: "status", type: "string", size: 50, required: false, defaultValue: "pending" },
            { name: "priority", type: "string", size: 20, required: false, defaultValue: "normal" },
            { name: "category", type: "string", size: 100, required: false },
            { name: "tags", type: "string", size: 500, required: false }
        ]
    };

    try {
        await setupCollection(config);
    } catch (error) {
        console.error("❌ 数据库初始化失败:", error.message || error);
    }
}

// 运行初始化
setupDatabase();
