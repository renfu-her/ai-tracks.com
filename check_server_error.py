#!/usr/bin/env python3
"""
诊断服务器 500 错误的脚本
在服务器上运行此脚本来检查常见问题
"""
import sys
import os

def check_imports():
    """检查所有必要的导入"""
    print("检查 Python 导入...")
    try:
        from flask import Flask
        print("✓ Flask 导入成功")
    except ImportError as e:
        print(f"✗ Flask 导入失败: {e}")
        return False
    
    try:
        from app import create_app, db
        print("✓ 应用模块导入成功")
    except Exception as e:
        print(f"✗ 应用模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def check_app_creation():
    """检查应用创建"""
    print("\n检查应用创建...")
    try:
        from app import create_app
        app = create_app('production')
        print("✓ 应用创建成功")
        return app
    except Exception as e:
        print(f"✗ 应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_routes(app):
    """检查路由注册"""
    print("\n检查路由注册...")
    try:
        with app.app_context():
            from flask import url_for
            # 测试主要路由
            routes_to_test = [
                'frontend.home',
                'frontend.cases',
                'frontend.news',
                'frontend.contact',
                'frontend.robots_txt',
                'frontend.sitemap_xml'
            ]
            
            for route in routes_to_test:
                try:
                    url = url_for(route)
                    print(f"✓ {route}: {url}")
                except Exception as e:
                    print(f"✗ {route}: {e}")
    except Exception as e:
        print(f"✗ 路由检查失败: {e}")
        import traceback
        traceback.print_exc()

def check_database():
    """检查数据库连接"""
    print("\n检查数据库连接...")
    try:
        from app import create_app, db
        app = create_app('production')
        with app.app_context():
            # 尝试简单查询
            from app.models import ProjectCase, News, ProductCategory
            case_count = ProjectCase.query.count()
            news_count = News.query.count()
            category_count = ProductCategory.query.count()
            print(f"✓ 数据库连接成功")
            print(f"  - Cases: {case_count}")
            print(f"  - News: {news_count}")
            print(f"  - Categories: {category_count}")
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()

def check_sitemap():
    """检查 sitemap 生成"""
    print("\n检查 sitemap 生成...")
    try:
        from app import create_app
        from app.controllers.frontend_controller import FrontendController
        from flask import Flask
        
        app = create_app('production')
        with app.test_request_context('https://blog.ai-tracks.com/'):
            sitemap = FrontendController.sitemap()
            if sitemap:
                print("✓ Sitemap 生成成功")
                print(f"  - Content length: {len(sitemap.data)} bytes")
            else:
                print("✗ Sitemap 生成返回 None")
    except Exception as e:
        print(f"✗ Sitemap 生成失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("=" * 60)
    print("服务器错误诊断工具")
    print("=" * 60)
    
    # 检查导入
    if not check_imports():
        print("\n❌ 基本导入检查失败，请检查 Python 环境和依赖")
        sys.exit(1)
    
    # 检查应用创建
    app = check_app_creation()
    if not app:
        print("\n❌ 应用创建失败")
        sys.exit(1)
    
    # 检查路由
    check_routes(app)
    
    # 检查数据库
    check_database()
    
    # 检查 sitemap
    check_sitemap()
    
    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)
    print("\n如果所有检查都通过，请检查：")
    print("1. uWSGI 日志: tail -f /var/log/uwsgi/ai-tracks.log")
    print("2. Nginx 错误日志: tail -f /var/log/nginx/error.log")
    print("3. 应用错误日志（如果配置了）")

if __name__ == '__main__':
    main()

