const sdk = require('node-appwrite');

const client = new sdk.Client();
const databases = new sdk.Databases(client);

client
    .setEndpoint('https://cloud.appwrite.io/v1')
    .setProject('67ac15990027bfb157f9')
    .setKey("standard_122aa6dfe96e880578a6b9857e10dabcddca60f320f38cecd393fdaaedc080f2639432ddab4dcd652c21da0d4b75168f531ab0949a530594d07679df049127ea91f2f22251cd8ca2155aa2847d2c626de7ffbc42f9b0a9b640b534f3daee6eb1f9c3fb46fdb2d84dec6aea8476ef6709b5548e36be9a68ac4f2290925997f96c")

const DATABASE_ID = '67d3a4480018e2e09b68';

/**
 * 获取所有集合
 * @returns {Promise<Array>} 集合列表
 */
async function listCollections() {
    try {
        const response = await databases.listCollections(DATABASE_ID);
        console.log("📑 现有集合列表:");
        response.collections.forEach(collection => {
            console.log(`- ${collection.$id}: ${collection.name}`);
        });
        return response.collections;
    } catch (error) {
        console.error("❌ 获取集合列表失败:", error.message || error);
        return [];
    }
}

/**
 * 获取集合的所有属性
 * @param {string} collectionId - 集合ID
 * @returns {Promise<Array>} 属性列表
 */
async function listAttributes(collectionId) {
    try {
        const response = await databases.listAttributes(DATABASE_ID, collectionId);
        console.log(`📝 集合 ${collectionId} 的属性列表:`);
        response.attributes.forEach(attr => {
            console.log(`- ${attr.key}: ${attr.type} (${attr.required ? '必填' : '可选'})`);
        });
        return response.attributes;
    } catch (error) {
        console.error(`❌ 获取集合 ${collectionId} 的属性列表失败:`, error.message || error);
        return [];
    }
}

/**
 * 检查并创建集合
 * @param {string} collectionId - 集合ID
 * @param {string} collectionName - 集合名称
 * @returns {Promise<void>}
 */
async function ensureCollection(collectionId, collectionName) {
    try {
        await databases.getCollection(DATABASE_ID, collectionId);
        console.log(`✅ ${collectionName}集合已存在，继续处理...`);
    } catch (error) {
        if (error.code === 404) {
            console.log(`⚠️ ${collectionName}集合不存在，创建新集合...`);
            await databases.createCollection(DATABASE_ID, collectionId, collectionName);
            console.log(`✅ ${collectionName}集合创建成功！`);
        } else {
            throw error;
        }
    }
}

/**
 * 检查并创建属性
 * @param {string} collectionId - 集合ID
 * @param {Object} attribute - 属性配置
 * @returns {Promise<void>}
 */
async function ensureAttribute(collectionId, attribute) {
    try {
        await databases.getAttribute(DATABASE_ID, collectionId, attribute.name);
        console.log(`ℹ️ ${attribute.name}字段已存在，跳过创建`);
    } catch (error) {
        if (error.code === 404) {
            console.log(`⚠️ 创建${attribute.name}字段...`);
            if (attribute.type === "string") {
                await databases.createStringAttribute(
                    DATABASE_ID,
                    collectionId,
                    attribute.name,
                    attribute.size,
                    attribute.required,
                    attribute.defaultValue
                );
            } else if (attribute.type === "datetime") {
                await databases.createDatetimeAttribute(
                    DATABASE_ID,
                    collectionId,
                    attribute.name,
                    attribute.required
                );
            }
            console.log(`✅ ${attribute.name}字段创建成功！`);
        } else {
            throw error;
        }
    }
}

/**
 * 初始化数据库集合
 * @param {Object} config - 数据库配置
 * @param {string} config.collectionId - 集合ID
 * @param {string} config.collectionName - 集合名称
 * @param {Array<Object>} config.attributes - 属性配置数组
 * @returns {Promise<void>}
 */
async function setupCollection(config) {
    try {
        const { collectionId, collectionName, attributes } = config;
        
        // 检查并创建集合
        await ensureCollection(collectionId, collectionName);

        // 检查并创建每个属性
        for (const attribute of attributes) {
            await ensureAttribute(collectionId, attribute);
        }

        console.log(`🎉 ${collectionName}数据库初始化完成！`);
    } catch (error) {
        console.error(`❌ ${config.collectionName}初始化过程中发生错误:`, error.message || error);
        throw error;
    }
}

module.exports = {
    setupCollection
};