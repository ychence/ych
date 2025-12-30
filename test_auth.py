#!/usr/bin/env python3
"""
认证功能测试脚本
用于测试注册和登录功能
"""
import requests
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_registration(base_url: str, test_email: str, test_password: str):
    """测试用户注册"""
    logger.info("=" * 50)
    logger.info("测试用户注册...")
    logger.info("=" * 50)

    url = f"{base_url}/api/auth/register"
    payload = {
        "username": "Test User",
        "email": test_email,
        "password": test_password,
    }

    try:
        response = requests.post(url, json=payload)
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应: {response.json()}")

        if response.status_code == 200:
            logger.info("✓ 注册成功")
            return True, response.json()
        elif response.status_code == 400:
            logger.warning("⚠ 用户已存在（这是正常的）")
            return False, None
        else:
            logger.error(f"✗ 注册失败: {response.json()}")
            return False, None
    except Exception as e:
        logger.error(f"✗ 注册请求失败: {e}")
        return False, None


def test_login(base_url: str, test_email: str, test_password: str):
    """测试用户登录"""
    logger.info("\n" + "=" * 50)
    logger.info("测试用户登录...")
    logger.info("=" * 50)

    url = f"{base_url}/api/auth/login"
    payload = {"email": test_email, "password": test_password}

    try:
        response = requests.post(url, json=payload)
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应: {response.json()}")

        if response.status_code == 200:
            result = response.json()
            logger.info("✓ 登录成功")
            logger.info(f"  Token: {result.get('token', '')[:50]}...")
            logger.info(f"  User: {result.get('user', {}).get('email')}")
            return True, result
        else:
            logger.error(f"✗ 登录失败: {response.json()}")
            return False, None
    except Exception as e:
        logger.error(f"✗ 登录请求失败: {e}")
        return False, None


def test_login_wrong_password(base_url: str, test_email: str):
    """测试错误密码登录"""
    logger.info("\n" + "=" * 50)
    logger.info("测试错误密码登录...")
    logger.info("=" * 50)

    url = f"{base_url}/api/auth/login"
    payload = {"email": test_email, "password": "wrong_password"}

    try:
        response = requests.post(url, json=payload)
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应: {response.json()}")

        if response.status_code == 401:
            logger.info("✓ 正确拒绝了错误密码")
            return True
        else:
            logger.error("✗ 应该返回 401 状态码")
            return False
    except Exception as e:
        logger.error(f"✗ 请求失败: {e}")
        return False


def test_health_check(base_url: str):
    """测试健康检查"""
    logger.info("=" * 50)
    logger.info("测试 API 健康检查...")
    logger.info("=" * 50)

    url = f"{base_url}/api/health"
    try:
        response = requests.get(url)
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应: {response.json()}")

        if response.status_code == 200:
            logger.info("✓ API 服务正常运行")
            return True
        else:
            logger.error("✗ API 服务异常")
            return False
    except Exception as e:
        logger.error(f"✗ 无法连接到 API: {e}")
        logger.error(f"请确保后端服务正在运行在 {base_url}")
        return False


def main():
    """运行所有测试"""
    # 配置
    base_url = "http://localhost:8000"
    test_email = "test@example.com"
    test_password = "Test123456!"

    logger.info("开始认证功能测试...\n")
    logger.info(f"API 地址: {base_url}")
    logger.info(f"测试邮箱: {test_email}\n")

    # 测试健康检查
    if not test_health_check(base_url):
        logger.error("\n❌ API 服务未运行，请先启动后端服务")
        return 1

    # 测试注册
    reg_success, reg_data = test_registration(base_url, test_email, test_password)

    # 测试登录
    login_success, login_data = test_login(base_url, test_email, test_password)

    # 测试错误密码
    wrong_pwd_success = test_login_wrong_password(base_url, test_email)

    # 结果汇总
    logger.info("\n" + "=" * 50)
    logger.info("测试结果汇总")
    logger.info("=" * 50)
    logger.info(f"注册功能: {'✓ 通过' if reg_success or login_success else '✗ 失败'}")
    logger.info(f"登录功能: {'✓ 通过' if login_success else '✗ 失败'}")
    logger.info(f"密码验证: {'✓ 通过' if wrong_pwd_success else '✗ 失败'}")

    if login_success:
        logger.info("\n🎉 认证功能测试通过！")
        return 0
    else:
        logger.error("\n❌ 认证功能测试失败，请查看上面的详细日志")
        return 1


if __name__ == "__main__":
    sys.exit(main())
