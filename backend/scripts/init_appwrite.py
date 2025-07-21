#!/usr/bin/env python3
"""
Appwrite 初始化脚本

此脚本帮助初始化 Appwrite 数据库和集合结构。
使用前请确保已正确配置环境变量。

使用方法:
    python scripts/init_appwrite.py
"""

import asyncio
import logging
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config.appwrite_config import AppwriteConfig
from appwrite import Client, Databases, ID
from appwrite.exception import AppwriteException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_database_and_collections():
    """创建数据库和集合"""
    try:
        # 初始化配置
        config = AppwriteConfig()
        if not config.validate():
            logger.error("Appwrite 配置无效，请检查环境变量")
            return False
        
        # 初始化客户端
        client = Client()
        client.set_endpoint(config.endpoint)
        client.set_project(config.project_id)
        client.set_key(config.api_key)
        
        databases = Databases(client)
        
        logger.info(f"连接到 Appwrite: {config.endpoint}")
        logger.info(f"项目 ID: {config.project_id}")
        
        # 创建数据库
        try:
            database = databases.create(
                database_id=config.database_id,
                name="Akasa Database"
            )
            logger.info(f"✅ 数据库创建成功: {config.database_id}")
        except AppwriteException as e:
            if "already exists" in str(e) or e.code == 409:
                logger.info(f"📋 数据库已存在: {config.database_id}")
            else:
                logger.error(f"❌ 创建数据库失败: {e}")
                return False
        
        # 创建 Users 集合
        try:
            users_collection = databases.create_collection(
                database_id=config.database_id,
                collection_id=config.users_collection_id,
                name="Users"
            )
            logger.info(f"✅ Users 集合创建成功: {config.users_collection_id}")
            
            # 创建 Users 集合属性
            attributes = [
                {"key": "user_id", "type": "string", "size": 255, "required": True},
                {"key": "email", "type": "string", "size": 255, "required": False},
                {"key": "name", "type": "string", "size": 255, "required": False},
            ]
            
            for attr in attributes:
                try:
                    if attr["type"] == "string":
                        databases.create_string_attribute(
                            database_id=config.database_id,
                            collection_id=config.users_collection_id,
                            key=attr["key"],
                            size=attr["size"],
                            required=attr["required"]
                        )
                    logger.info(f"  ✅ 属性创建成功: {attr['key']}")
                except AppwriteException as e:
                    if "already exists" in str(e) or e.code == 409:
                        logger.info(f"  📋 属性已存在: {attr['key']}")
                    else:
                        logger.warning(f"  ⚠️ 创建属性失败: {attr['key']} - {e}")
            
            # 创建唯一索引
            try:
                databases.create_index(
                    database_id=config.database_id,
                    collection_id=config.users_collection_id,
                    key="user_id_unique",
                    type="unique",
                    attributes=["user_id"]
                )
                logger.info("  ✅ 唯一索引创建成功: user_id_unique")
            except AppwriteException as e:
                if "already exists" in str(e) or e.code == 409:
                    logger.info("  📋 唯一索引已存在: user_id_unique")
                else:
                    logger.warning(f"  ⚠️ 创建唯一索引失败: {e}")
                    
        except AppwriteException as e:
            if "already exists" in str(e) or e.code == 409:
                logger.info(f"📋 Users 集合已存在: {config.users_collection_id}")
            else:
                logger.error(f"❌ 创建 Users 集合失败: {e}")
                return False
        
        # 创建 Configs 集合
        try:
            configs_collection = databases.create_collection(
                database_id=config.database_id,
                collection_id=config.configs_collection_id,
                name="Configs"
            )
            logger.info(f"✅ Configs 集合创建成功: {config.configs_collection_id}")
            
            # 创建 Configs 集合属性
            attributes = [
                {"key": "user_id", "type": "string", "size": 255, "required": True},
                {"key": "config_type", "type": "string", "size": 100, "required": True},
                {"key": "config_data", "type": "string", "size": 10000, "required": True},
            ]
            
            for attr in attributes:
                try:
                    if attr["type"] == "string":
                        databases.create_string_attribute(
                            database_id=config.database_id,
                            collection_id=config.configs_collection_id,
                            key=attr["key"],
                            size=attr["size"],
                            required=attr["required"]
                        )
                    logger.info(f"  ✅ 属性创建成功: {attr['key']}")
                except AppwriteException as e:
                    if "already exists" in str(e) or e.code == 409:
                        logger.info(f"  📋 属性已存在: {attr['key']}")
                    else:
                        logger.warning(f"  ⚠️ 创建属性失败: {attr['key']} - {e}")
            
            # 创建复合索引
            try:
                databases.create_index(
                    database_id=config.database_id,
                    collection_id=config.configs_collection_id,
                    key="user_config_type",
                    type="key",
                    attributes=["user_id", "config_type"]
                )
                logger.info("  ✅ 复合索引创建成功: user_config_type")
            except AppwriteException as e:
                if "already exists" in str(e) or e.code == 409:
                    logger.info("  📋 复合索引已存在: user_config_type")
                else:
                    logger.warning(f"  ⚠️ 创建复合索引失败: {e}")
                    
        except AppwriteException as e:
            if "already exists" in str(e) or e.code == 409:
                logger.info(f"📋 Configs 集合已存在: {config.configs_collection_id}")
            else:
                logger.error(f"❌ 创建 Configs 集合失败: {e}")
                return False
        
        logger.info("\n🎉 Appwrite 数据库初始化完成！")
        logger.info("\n📋 创建的结构:")
        logger.info(f"  📁 数据库: {config.database_id}")
        logger.info(f"  👥 Users 集合: {config.users_collection_id}")
        logger.info(f"    - user_id (string, unique)")
        logger.info(f"    - email (string, optional)")
        logger.info(f"    - name (string, optional)")
        logger.info(f"  ⚙️ Configs 集合: {config.configs_collection_id}")
        logger.info(f"    - user_id (string)")
        logger.info(f"    - config_type (string)")
        logger.info(f"    - config_data (string)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 初始化失败: {e}")
        return False


async def test_connection():
    """测试 Appwrite 连接"""
    try:
        from src.services.appwrite_service import appwrite_service
        
        logger.info("🔍 测试 Appwrite 连接...")
        is_available = await appwrite_service.check_health()
        
        if is_available:
            logger.info("✅ Appwrite 连接成功！")
            return True
        else:
            logger.error("❌ Appwrite 连接失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 连接测试失败: {e}")
        return False


async def main():
    """主函数"""
    logger.info("🚀 开始初始化 Appwrite...")
    
    # 测试连接
    if not await test_connection():
        logger.error("请检查 Appwrite 配置后重试")
        return
    
    # 创建数据库结构
    success = await create_database_and_collections()
    
    if success:
        logger.info("\n✅ 初始化完成！现在可以启动应用程序了。")
        logger.info("\n📖 下一步:")
        logger.info("  1. 启动后端服务: poetry run uvicorn server.app:app --reload")
        logger.info("  2. 测试 API: curl http://localhost:8000/api/users/health")
        logger.info("  3. 创建测试用户: curl -X POST http://localhost:8000/api/users -H 'Content-Type: application/json' -d '{\"user_id\": \"test_user\", \"name\": \"Test User\"}'")
    else:
        logger.error("❌ 初始化失败，请检查错误信息")


if __name__ == "__main__":
    asyncio.run(main())