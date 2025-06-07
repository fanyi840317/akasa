const { setupCollection } = require('./setup_utils');

async function setupComments() {
    const commentsConfig = {
        collectionId: 'comments',
        collectionName: 'comment',
        attributes: [
            { name: "event_id", type: "string", size: 100, required: true },
            { name: "user_id", type: "string", size: 100, required: true },
            { name: "author_name", type: "string", size: 100, required: true },
            { name: "author_avatar", type: "string", size: 255, required: false },
            { name: "content", type: "string", size: 2000, required: true },
            { name: "parent_id", type: "string", size: 100, required: false }, // 用于回复功能
            { name: "likes", type: "integer", required: false, defaultValue: 0 },
            { name: "is_edited", type: "boolean", required: false, defaultValue: false },
            { name: "paid_amount", type: "string", size: 50, required: false }, // 付费评论金额
            { name: "status", type: "string", size: 20, required: false, defaultValue: "active" } // active, deleted, hidden
        ]
    };

    try {
        await setupCollection(commentsConfig);
        console.log('🎉 评论数据库初始化完成！');
    } catch (error) {
        console.error('❌ 评论数据库初始化失败:', error.message || error);
    }
}

// 运行初始化
setupComments();