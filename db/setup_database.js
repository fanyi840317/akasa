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
            { name: "folder_id", type: "string", size: 100, required: false },   // 关联的文件夹ID
            { name: "tags", type: "string", size: 500, required: false }
        ]
    };

    const eventsConfig = {
        collectionId: 'events',
        collectionName: 'event',
        attributes: [
            { name: "title", type: "string", size: 255, required: true },
            { name: "location", type: "string", size: 255, required: false },
            { name: "location_data", type: "string", size: 1000, required: false },
            { name: "date", type: "datetime", required: false },
            { name: "status", type: "string", size: 50, required: false, defaultValue: "pending" },
            { name: "content", type: "string", size: 36000, required: false },
            { name: "user_id", type: "string", size: 100, required: true },
            { name: "creator_name", type: "string", size: 100, required: false },
            { name: "creator_avatar", type: "string", size: 255, required: false },
            { name: "folder_id", type: "string", size: 100, required: false }
        ]
    };

    try {
        await Promise.all([
            setupCollection(config),
            setupCollection(eventsConfig)
        ]);
    } catch (error) {
        console.error("❌ 数据库初始化失败:", error.message || error);
    }
}

// 运行初始化
setupDatabase();
