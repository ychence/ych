#!/usr/bin/env python3
"""
单次登录测试 - 使用新用户
"""
import requests
import sys
import logging
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_new_user():
    """测试新用户注册和登录"""
    base_url = "http://localhost:8000"

    # 使用随机邮箱
    random_id = str(uuid.uuid4())[:8]
    test_email = f"newuser{random_id}@example.com"
    test_password = "TestPassword123!"

    logger.info("=" * 60)
    logger.info(f"使用新用户测试: {test_email}")
    logger.info("=" * 60)

    # 1. 注册新用户
    logger.info("\n步骤 1: 注册新用户...")
    url = f"{base_url}/api/auth/register"
    payload = {
        "username": "Test User",
        "email": test_email,
        "password": test_password,
    }

    try:
        response = requests.post(url, json=payload)
        logger.info(f"注册状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.info("✓ 注册成功")
            logger.info(f"  用户ID: {result['user']['id']}")
            logger.info(f"  用户邮箱: {result['user']['email']}")
            logger.info(f"  Token: {result['token'][:50]}...")
        else:
            logger.error(f"✗ 注册失败: {response.json()}")
            return False
    except Exception as e:
        logger.error(f"✗ 注册请求失败: {e}")
        return False

    # 2. 登录刚注册的用户
    logger.info("\n步骤 2: 登录刚注册的用户...")
    url = f"{base_url}/api/auth/login"
    payload = {
        "email": test_email,
        "password": test_password,
    }

    try:
        response = requests.post(url, json=payload)
        logger.info(f"登录状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.info("✓ 登录成功")
            logger.info(f"  用户ID: {result['user']['id']}")
            logger.info(f"  用户邮箱: {result['user']['email']}")
            logger.info(f"  Token: {result['token'][:50]}...")

            logger.info("\n" + "=" * 60)
            logger.info("🎉 测试成功！认证功能正常工作。")
            logger.info("=" * 60)
            return True
        else:
            logger.error(f"✗ 登录失败: {response.json()}")
            logger.info("\n" + "=" * 60)
            logger.error("❌ 登录失败！虽然注册成功，但登录失败。")
            logger.info("=" * 60)
            return False
    except Exception as e:
        logger.error(f"✗ 登录请求失败: {e}")
        return False


if __name__ == "__main__":
    success = test_new_user()
    sys.exit(0 if success else 1)
