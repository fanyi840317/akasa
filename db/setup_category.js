const { setupCollection } = require('./setup_utils');

async function setupCategory() {
    const categoryConfig = {
        collectionId: 'categories',
        collectionName: 'category',
        attributes: [
            { name: "name", type: "string", size: 100, required: true },
            { name: "description", type: "string", size: 500, required: false },
            { name: "icon", type: "string", size: 50, required: false },
            { name: "color", type: "string", size: 20, required: false },
            { name: "parent_id", type: "string", size: 100, required: false },  // 父分类ID，用于构建分类树
            { name: "order", type: "integer", required: false, defaultValue: 0 },  // 排序顺序
            { name: "status", type: "string", size: 20, required: false, defaultValue: "active" },
            { name: "user_id", type: "string", size: 100, required: true },  // 创建者ID
            { name: "created_at", type: "datetime", required: true },
            { name: "updated_at", type: "datetime", required: true }
        ]
    };

    try {
        await setupCollection(categoryConfig);
        console.log("✅ 分类集合创建成功");
    } catch (error) {
        console.error("❌ 分类集合创建失败:", error.message || error);
    }
}

// 运行初始化
setupCategory(); 