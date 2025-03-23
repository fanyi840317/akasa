const { setupCollection } = require('./setup_utils');

async function setupFoldersDatabase() {
    const config = {
        collectionId: 'folders',
        collectionName: 'folder',
        attributes: [
            { name: "name", type: "string", size: 255, required: true },      // 文件夹名称
            { name: "user_id", type: "string", size: 100, required: true },    // 所属用户ID
            { name: "parent_id", type: "string", size: 100, required: false }, // 父文件夹ID，顶级文件夹为null
            { name: "path", type: "string", size: 500, required: false },      // 文件夹路径，例如：/root/subfolder
            { name: "icon", type: "string", size: 50, required: false },       // 文件夹图标
            { name: "color", type: "string", size: 20, required: false },      // 文件夹颜色
            { name: "order", type: "integer", required: false },              // 排序顺序
            { name: "created_time", type: "datetime", required: true },       // 创建时间
            { name: "updated_time", type: "datetime", required: false },      // 更新时间
            { name: "description", type: "string", size: 500, required: false }, // 文件夹描述
            { name: "status", type: "string", size: 50, required: false, defaultValue: "active" } // 状态：active, archived, deleted
        ]
    };

    try {
        await setupCollection(config);
    } catch (error) {
        console.error("❌ 文件夹数据库初始化失败:", error.message || error);
    }
}

// 运行初始化
setupFoldersDatabase();