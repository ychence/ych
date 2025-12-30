#!/usr/bin/env python3
"""
Azure 连接测试脚本
用于诊断 Azure Cosmos DB 和 Blob Storage 连接问题
"""
import sys
import logging
from config import settings
from database import cosmos_db
from storage import blob_storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_config():
    """测试配置是否加载成功"""
    logger.info("=" * 50)
    logger.info("测试配置加载...")
    logger.info("=" * 50)

    try:
        logger.info(f"✓ Cosmos Endpoint: {settings.cosmos_endpoint[:50]}...")
        logger.info(f"✓ Cosmos Database: {settings.cosmos_database_name}")
        logger.info(f"✓ JWT Secret Key: {'*' * 20} (已配置)")
        logger.info(f"✓ API Host: {settings.api_host}:{settings.api_port}")
        logger.info(f"✓ Allowed Origins: {settings.allowed_origins}")
        return True
    except Exception as e:
        logger.error(f"✗ 配置加载失败: {e}")
        return False


def test_cosmos_db():
    """测试 Cosmos DB 连接"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 Cosmos DB 连接...")
    logger.info("=" * 50)

    try:
        cosmos_db.initialize()
        logger.info("✓ Cosmos DB 连接成功")
        logger.info(f"✓ Database: {settings.cosmos_database_name}")
        logger.info(f"✓ Users container: 已创建")
        logger.info(f"✓ Media container: 已创建")
        return True
    except Exception as e:
        logger.error(f"✗ Cosmos DB 连接失败: {e}")
        logger.error("请检查:")
        logger.error("  1. COSMOS_ENDPOINT 是否正确")
        logger.error("  2. COSMOS_KEY 是否正确")
        logger.error("  3. Azure 网络连接是否正常")
        return False


def test_blob_storage():
    """测试 Blob Storage 连接"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 Blob Storage 连接...")
    logger.info("=" * 50)

    try:
        blob_storage.initialize()
        logger.info("✓ Blob Storage 连接成功")
        logger.info(f"✓ Container: {settings.blob_container_name}")
        return True
    except Exception as e:
        logger.error(f"✗ Blob Storage 连接失败: {e}")
        logger.error("请检查:")
        logger.error("  1. AZURE_STORAGE_CONNECTION_STRING 是否正确")
        logger.error("  2. Storage Account 是否存在")
        logger.error("  3. Azure 网络连接是否正常")
        return False


def test_user_query():
    """测试用户查询"""
    logger.info("\n" + "=" * 50)
    logger.info("测试用户查询...")
    logger.info("=" * 50)

    try:
        # 尝试查询一个不存在的用户
        user = cosmos_db.get_user_by_email("test@example.com")
        if user:
            logger.info(f"✓ 找到测试用户: {user['email']}")
        else:
            logger.info("✓ 用户查询功能正常（未找到测试用户，这是正常的）")
        return True
    except Exception as e:
        logger.error(f"✗ 用户查询失败: {e}")
        return False


def main():
    """运行所有测试"""
    logger.info("开始 Azure 连接诊断...\n")

    results = {
        "配置加载": test_config(),
        "Cosmos DB": test_cosmos_db(),
        "Blob Storage": test_blob_storage(),
        "用户查询": test_user_query(),
    }

    logger.info("\n" + "=" * 50)
    logger.info("测试结果汇总")
    logger.info("=" * 50)

    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        logger.info(f"{test_name}: {status}")

    all_passed = all(results.values())
    if all_passed:
        logger.info("\n🎉 所有测试通过！Azure 配置正常。")
        return 0
    else:
        logger.error("\n❌ 部分测试失败，请根据上面的提示检查配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
