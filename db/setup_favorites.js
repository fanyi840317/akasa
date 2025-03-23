const { setupCollection } = require('./setup_utils');

async function setupFavoritesDatabase() {
    const config = {
        collectionId: 'favorites',
        collectionName: 'favorite',
        attributes: [
            { name: "user_id", type: "string", size: 100, required: true },
            { name: "item_id", type: "string", size: 100, required: true },
            { name: "item_type", type: "string", size: 50, required: true },  // 例如：case, feedback等
            { name: "title", type: "string", size: 255, required: true },     // 收藏项目的标题
            { name: "description", type: "string", size: 1000, required: false }, // 收藏项目的简短描述
            { name: "favorite_time", type: "datetime", required: true },      // 收藏时间
            { name: "notes", type: "string", size: 1000, required: false },   // 用户添加的笔记
            { name: "folder_id", type: "string", size: 100, required: false },   // 关联的文件夹ID
            { name: "tags", type: "string", size: 500, required: false },     // 用户自定义标签
            { name: "status", type: "string", size: 50, required: false, defaultValue: "active" } // 收藏状态：active, archived, deleted
        ]
    };

    try {
        await setupCollection(config);
    } catch (error) {
        console.error("❌ 收藏数据库初始化失败:", error.message || error);
    }
}

// 运行初始化
setupFavoritesDatabase();