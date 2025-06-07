const sdk = require('node-appwrite');
require('dotenv').config();

const client = new sdk.Client();
const databases = new sdk.Databases(client);

client
    .setEndpoint('https://cloud.appwrite.io/v1')
    .setProject('67ac15990027bfb157f9')
    .setKey(process.env.APPWRITE_API_KEY)

const DATABASE_ID = '67d3a4480018e2e09b68';
const COLLECTION_ID = 'categories';

const categories = [
    {
        "name": JSON.stringify({
            "zh": "都市传说",
            "en": "Urban Legends"
        }),
        "description": JSON.stringify({
            "zh": "发生在现代都市中的神秘事件和传说",
            "en": "Mysterious events and legends occurring in modern cities"
        }),
        "icon": "city",
        "color": "#FF6B6B",
        "parent_id": null,
        "order": 1,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "超自然现象",
            "en": "Supernatural Phenomena"
        }),
        "description": JSON.stringify({
            "zh": "无法用科学解释的超自然事件",
            "en": "Events that cannot be explained by science"
        }),
        "icon": "ghost",
        "color": "#4ECDC4",
        "parent_id": null,
        "order": 2,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "平行宇宙",
            "en": "Parallel Universes"
        }),
        "description": JSON.stringify({
            "zh": "可能与平行宇宙或维度重叠相关的事件",
            "en": "Events possibly related to parallel universes or dimensional overlaps"
        }),
        "icon": "globe",
        "color": "#45B7D1",
        "parent_id": null,
        "order": 3,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "预知能力",
            "en": "Precognition"
        }),
        "description": JSON.stringify({
            "zh": "涉及预知、预言或时间异常的事件",
            "en": "Events involving precognition, prophecy, or temporal anomalies"
        }),
        "icon": "clock",
        "color": "#96CEB4",
        "parent_id": null,
        "order": 4,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "意识现象",
            "en": "Consciousness Phenomena"
        }),
        "description": JSON.stringify({
            "zh": "与意识、记忆或思维相关的神秘事件",
            "en": "Mysterious events related to consciousness, memory, or thought"
        }),
        "icon": "brain",
        "color": "#FFEEAD",
        "parent_id": null,
        "order": 5,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "灵异事件",
            "en": "Paranormal Events"
        }),
        "description": JSON.stringify({
            "zh": "与灵体、鬼魂或灵异现象相关的事件",
            "en": "Events related to spirits, ghosts, or paranormal phenomena"
        }),
        "icon": "spirit",
        "color": "#D4A5A5",
        "parent_id": null,
        "order": 6,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "神秘生物",
            "en": "Cryptids"
        }),
        "description": JSON.stringify({
            "zh": "关于未知生物或神秘物种的目击事件",
            "en": "Sightings of unknown creatures or mysterious species"
        }),
        "icon": "paw",
        "color": "#9B59B6",
        "parent_id": null,
        "order": 7,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    },
    {
        "name": JSON.stringify({
            "zh": "未解之谜",
            "en": "Unsolved Mysteries"
        }),
        "description": JSON.stringify({
            "zh": "其他无法解释的神秘事件和现象",
            "en": "Other unexplained mysterious events and phenomena"
        }),
        "icon": "question",
        "color": "#3498DB",
        "parent_id": null,
        "order": 8,
        "status": "active",
        "user_id": "system",
        "created_at": new Date().toISOString(),
        "updated_at": new Date().toISOString()
    }
];

async function initializeCategories() {
    try {
        console.log("🚀 开始初始化神秘事件分类数据...");
        
        for (const category of categories) {
            try {
                await databases.createDocument(
                    DATABASE_ID,
                    COLLECTION_ID,
                    sdk.ID.unique(),
                    category
                );
                const nameObj = JSON.parse(category["name"]);
                console.log(`✅ 成功添加分类: ${nameObj["zh"]} / ${nameObj["en"]}`);
            } catch (error) {
                const nameObj = JSON.parse(category["name"]);
                console.error(`❌ 添加分类 ${nameObj["zh"]} 失败:`, error.message || error);
            }
        }

        console.log("🎉 神秘事件分类数据初始化完成！");
    } catch (error) {
        console.error("❌ 初始化过程中发生错误:", error.message || error);
    }
}

// 运行初始化
initializeCategories(); 