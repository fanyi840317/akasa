const { setupCollection } = require('./setup_utils');

async function setupFeedbackDatabase() {
    const config = {
        collectionId: 'feedbacks',
        collectionName: 'feedback',
        attributes: [
            { name: "title", type: "string", size: 255, required: true },
            { name: "content", type: "string", size: 5000, required: true },
            { name: "type", type: "string", size: 50, required: true },
            { name: "user_id", type: "string", size: 100, required: true },
            { name: "user_email", type: "string", size: 255, required: true },
            { name: "submit_time", type: "datetime", required: true },
            { name: "status", type: "string", size: 50, required: false, defaultValue: "pending" },
            { name: "priority", type: "string", size: 20, required: false, defaultValue: "normal" },
            { name: "response", type: "string", size: 2000, required: false },
            { name: "response_time", type: "datetime", required: false }
        ]
    };

    try {
        await setupCollection(config);
    } catch (error) {
        console.error("❌ 反馈数据库初始化失败:", error.message || error);
    }
}

// 运行初始化
setupFeedbackDatabase();