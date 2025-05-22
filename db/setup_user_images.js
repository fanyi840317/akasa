const { setupCollection } = require('./setup_utils');

async function setupUserImages() {
    const userImagesConfig = {
        collectionId: 'user_images',
        collectionName: 'user_images',
        attributes: [
            { name: "userId", type: "string", size: 100, required: true },
            { name: "provider", type: "string", size: 50, required: false }, // 图片提供者 (e.g., 'upload', 'unsplash', 'pexels')
            { name: "imageUrl", type: "string", size: 500, required: true }, // 原始图片URL
            { name: "thumbnailUrl", type: "string", size: 500, required: false }, // 缩略图URL
            { name: "extraData", type: "string", size: 5000, required: false }, // 存储额外数据，如API提供者的元数据
            { name: "created_at", type: "datetime", required: true },
            { name: "updated_at", type: "datetime", required: true }
        ]
    };

    try {
        await setupCollection(userImagesConfig);
        console.log("✅ 用户图片集合创建成功");
    } catch (error) {
        console.error("❌ 用户图片集合创建失败:", error.message || error);
    }
}

// 运行初始化
setupUserImages();